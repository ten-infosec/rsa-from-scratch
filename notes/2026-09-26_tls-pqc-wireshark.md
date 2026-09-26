# Wireshark로 내 브라우저의 양자내성암호(ML-KEM) 확인하기

PQC 커리큘럼 2단계(네트워크) + 4단계(TLS) 실습 기록. (2026-09-25 캡처, 2026-09-26 분석)

> 집 Wi-Fi에서 **내 컴퓨터의 내 통신만** 캡처했다. 캡처 파일(.pcapng)과 기기 식별 정보(MAC 주소, 내부 IP)는 공개하지 않는다.

## 한 줄 결론

example.com 접속 시 크롬은 **X25519MLKEM768(기존 X25519 + 양자내성 ML-KEM 하이브리드)** 키 교환을 1순위로 제안했고, 서버는 이를 **수락**했다. 내 브라우저는 이미 양자내성암호로 세션 키를 나누고 있다.

## 1. TCP 3-way 핸드셰이크 (복습)

| 패킷 | 플래그 | Seq | Ack | 의미 |
|---|---|---|---|---|
| 1 | SYN | 0 | – | 연결하자 |
| 2 | SYN, ACK | 0 | 1 | 나도 연결하자 + 네 0번 받음 |
| 3 | ACK | 1 | 1 | 확인, 시작 |

- 다음 Seq = 지금 Seq + Len (예: Seq 1에서 282바이트 전송 → 다음 Seq 283)
- Len = 패킷 전체 길이 − 헤더(Ethernet 14 + IP 20 + TCP 20 = 54)

## 2. TLS Client Hello (크롬 → example.com)

**supported_groups** (쓸 수 있는 키 교환 목록, 16진수 `7a 7a 11 ec 00 1d 00 17 00 18`)

| 순서 | 그룹 | 번호 |
|---|---|---|
| 0 | GREASE (가짜 값) | 0x7a7a |
| **1** | **X25519MLKEM768** | **0x11ec** |
| 2 | x25519 | 0x001d |
| 3 | secp256r1 | 0x0017 |
| 4 | secp384r1 | 0x0018 |

**key_share** (실제로 보낸 열쇠 재료)

| 항목 | 크기 |
|---|---|
| key_share 전체 | 1,267바이트 |
| X25519MLKEM768 | 1,220바이트 (열쇠 재료 1,216 = ML-KEM768 1,184 + X25519 32) |
| x25519 | 36바이트 (열쇠 재료 32) |

→ 크롬의 Client Hello가 약 2,000바이트로 커진 이유. 다른 프로그램의 Client Hello는 593바이트였다.

**signature_algorithms**에는 **ML-DSA(mldsa44/65/87)**와 **RSA(rsa_pss_rsae_sha256 등)**가 나란히 들어 있었다. 양자내성 서명도 받을 수 있다는 뜻.

## 3. TLS Server Hello (example.com → 크롬)

| 항목 | 서버의 선택 |
|---|---|
| 키 교환 | **X25519MLKEM768** (열쇠 재료 **1,120바이트**) |
| 데이터 암호 | TLS_AES_128_GCM_SHA256 |
| TLS 버전 | 1.3 |

Client Hello 이후 약 28ms 만에 응답. Server Hello 뒤부터는 인증서까지 전부 암호화되어 보이지 않았다.

## 4. 왜 1,216과 1,120으로 크기가 다른가: KEM

1. 크롬: **열린 자물쇠**(ML-KEM 공개키 1,184바이트)를 보냄
2. 서버: 비밀 값을 넣고 그 자물쇠로 **잠근 상자**(암호문 1,088바이트)를 보냄
3. 크롬: 개인키로 열어 같은 비밀 값을 얻음

각자 X25519 재료 32바이트가 붙어 1,216 / 1,120. 두 방식의 비밀을 섞어 최종 키를 만들기 때문에 **둘 중 하나만 안전해도 전체가 안전**하다.

"공개키로 잠그고 개인키로 연다"는 발상은 [RSA 실습](../README.md)과 같지만, RSA는 소인수분해(양자컴퓨터에 약함), ML-KEM은 격자 문제(양자컴퓨터로도 어려움)에 기반한다.

## 5. 부수 관찰

- **Cipher Suites**: 공개키 암호로 열쇠만 나누고, 데이터는 AES로 잠근다
- **encrypted_client_hello**: 사이트 이름(SNI)을 숨기는 ECH. 이번엔 겉 SNI가 그대로 보여 크롬의 가짜(GREASE) ECH로 추정. ECH 자체는 아직 X25519 기반
- **TSO**: Client Hello가 1,500바이트(MTU)를 넘어 IP 전체 길이 칸이 0으로 기록됨. 네트워크 카드가 나갈 때 두 조각으로 자름
- **JA3 / JA4**: Client Hello 구성으로 만든 프로그램 지문. JA3 문자열에서 4588 = X25519MLKEM768

## 사용한 필터

| 목적 | 필터 |
|---|---|
| 연결 시작 패킷 | `tcp.flags.syn == 1` |
| 특정 연결 전체 | `tcp.stream eq N` |
| Client Hello | `tls.handshake.type == 1` |
| Server Hello | `tls.handshake.type == 2` |
| PQC 하이브리드를 제안한 Client Hello | `tls.handshake.extensions_supported_group == 0x11ec` |