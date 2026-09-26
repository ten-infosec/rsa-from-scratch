# PQC 커리큘럼 목차 (Stage 1~9)

## 기초 구간

### Stage 1. 정수론
- 소수와 소인수분해
- 유클리드 호제법
- 모듈러 연산
- 모듈러 역원
- 페르마의 소정리 · 오일러 정리
- 실습: 작은 RSA 구현

### Stage 2. 전산학 기초
- 자료구조 (배열, 연결리스트, 트리, 해시테이블)
- 프로세스 · 스레드
- 가상 메모리 · 페이징
- OSI 7계층 vs TCP/IP 4계층
- TCP 3-way 핸드셰이크
- 실습: Wireshark 핸드셰이크 캡처 · 계층 구조 확인

### Stage 3. C/C++ · 리눅스
- 리눅스 환경, gcc · gdb
- 포인터와 메모리 주소
- malloc/free
- 컴파일 4단계
- 스택 vs 힙
- 버퍼 오버플로우 · use-after-free
- 실습: 버퍼 오버플로우 발생 · gdb 디버깅

### Stage 4. 네트워크 보안 · 암호학 기초
- 대칭키(AES) vs 공개키(RSA)
- 해시함수 (SHA-256, 눈사태 효과)
- HMAC
- 디지털 서명
- TLS 핸드셰이크
- IPsec (전송 모드 vs 터널 모드)
- 실습: TLS 핸드셰이크 캡처 · 해시 눈사태 실험

## 진입 구간

### Stage 5. PKI 실전
- X.509 인증서 구조
- CA와 인증서 체인
- CRL · OCSP
- HSM
- 실습: OpenSSL로 루트 CA · 서버 인증서 발급 · nginx 적용

### Stage 6. PQC
- 격자 기반 암호
- ML-KEM
- ML-DSA · SLH-DSA
- 하이브리드 방식
- 크립토 애자일리티
- 실습: liboqs 빌드 · OpenSSL 연동 · ML-KEM TLS 서버

## 확장 구간

### Stage 7. QKD · QRNG
- 측정-교란 원리, no-cloning
- BB84 프로토콜
- FPGA · HDL
- 실습: BB84 손 시뮬레이션

### Stage 8. Secure Enclave · TEE
- Intel SGX · ARM TrustZone · AMD SEV
- 격리 vs 증명
- 실습: SGX Hello Enclave

### Stage 9. 암호화 가속 · Root of Trust · SoC
- CUDA 기초
- Root of Trust · Secure Boot
- Attestation (DICE, SPDM, TPM)
- SoC 구조
- 실습: AES를 GPU로 병렬 처리 · CPU와 속도 비교