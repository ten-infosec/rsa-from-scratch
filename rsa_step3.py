# 3단계: 확장 유클리드 호제법으로 모듈러 역원 구하기


def mod_inverse(e, phi):
    old_r, r = e, phi
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if old_r != 1:
        return None
    return old_s % phi


# def mod_inverse(e, phi): → e에 곱해서 phi로 나눈 나머지가 1이 되는 수(역원)를 찾는 함수를 만들겠다
# old_r, r = e, phi → 1단계처럼 나머지를 줄여갈 두 수를 준비하겠다
# old_s, s = 1, 0 → 각 나머지가 "e를 몇 개 써서" 만들어졌는지 적을 기록 칸을 준비하겠다 (e 자신은 1개, phi는 0개)
# while r != 0: → r이 0이 아닌 동안 계속 반복하겠다
# q = old_r // r → 이번 나눗셈의 몫을 구하겠다
# old_r, r = r, old_r - q * r → 1단계와 똑같이 나눈 수는 앞으로, 나머지는 뒤로 보내겠다 (old_r - q * r은 old_r % r과 같은 값)
# old_s, s = s, old_s - q * s → 나머지를 만든 것과 똑같은 계산을 기록 칸에도 적용하겠다
# if old_r != 1: return None → 최대공약수가 1이 아니면(서로소 아니면) 역원이 없으므로 None을 돌려주겠다
# return old_s % phi → 기록이 음수일 수 있으니 phi로 나머지를 구해 양수로 바꿔 돌려주겠다




# 3단계 가시화: 나머지 줄과 기록 줄이 함께 변하는 과정을 문장으로 보여주기


def mod_inverse_trace(e, phi):
    old_r, r = e, phi
    old_s, s = 1, 0
    print(f"시작: 나머지 ({old_r}, {r}) / 기록 ({old_s}, {s})")
    count = 1
    while r != 0:
        q = old_r // r
        new_r = old_r - q * r
        new_s = old_s - q * s
        print(f"{count}바퀴: {old_r} ÷ {r} = 몫 {q}, 나머지 {new_r} → 나머지 ({r}, {new_r})")
        print(f"       기록: {old_s} - {q}×({s}) = {new_s} → 기록 ({s}, {new_s}) / 검산: {new_s}×{e} mod {phi} = {new_s * e % phi}")
        old_r, r = r, new_r
        old_s, s = s, new_s
        count += 1
    print(f"나머지가 0이 됨 → 멈춤 / 최대공약수 = {old_r}")
    if old_r != 1:
        print("서로소가 아님 → 역원 없음")
        return None
    print(f"음수 정리: {old_s} % {phi} = {old_s % phi}")
    return old_s % phi


# print(f"시작: ...") → 반복 전의 나머지 쌍과 기록 쌍을 찍겠다
# new_r = old_r - q * r → 이번 나머지를 먼저 계산해두겠다 (화면에 보여주려고 따로 담음)
# new_s = old_s - q * s → 나머지와 똑같은 계산으로 이번 기록을 먼저 계산해두겠다
# print(f"{count}바퀴: ...") → 1단계 gcd_trace와 같은 형식으로 나눗셈과 새 나머지 쌍을 찍겠다
# print(f"       기록: ...") → 기록이 어떤 계산으로 바뀌었는지, 그리고 "기록 × e mod phi"가 방금 나머지와 같은지 검산해서 찍겠다
# old_r, r = r, new_r / old_s, s = s, new_s → 미리 계산해둔 값으로 실제로 다음 바퀴 상태로 넘어가겠다
# if old_r != 1: → 최대공약수가 1이 아니면 역원이 없다고 알리고 None을 돌려주겠다
# print(f"음수 정리: ...") → 기록이 음수면 phi를 더한 것과 같은 양수로 바꾸는 과정을 보여주겠다




# 확인: 여러 숫자로 과정과 결과 보기

if __name__ == "__main__":
    print("답:", mod_inverse_trace(3, 7))
    print()
    print("답:", mod_inverse_trace(17, 3120))
    print()
    print("답:", mod_inverse_trace(12, 3120))
    print()
    print("mod_inverse 결과:", mod_inverse(3, 7), mod_inverse(17, 3120), mod_inverse(12, 3120))
    print("pow 검산:", pow(3, -1, 7), pow(17, -1, 3120))
    print("17 × 2753 mod 3120 =", 17 * 2753 % 3120)
    print()
    print("2790을 개인키 2753으로 열면:", pow(2790, 2753, 3233))


# print("답:", mod_inverse_trace(3, 7)) → mod 7에서 3의 역원(5)이 나오는 짧은 과정을 보겠다
# print("답:", mod_inverse_trace(17, 3120)) → 실제 RSA 숫자로 개인키 2753이 나오는 과정을 보겠다
# print("답:", mod_inverse_trace(12, 3120)) → 서로소가 아닌 12는 역원이 없다는 걸 과정으로 보겠다
# print("mod_inverse 결과:", ...) → 원래 함수의 답 세 개를 한 줄에 찍겠다 (5, 2753, None)
# print("pow 검산:", ...) → 파이썬 내장 pow(지수 자리에 -1)로 역원을 구해 위 줄과 비교하겠다
# print("17 × 2753 mod 3120 =", ...) → 2753이 진짜로 17과 곱해 나머지 1을 만드는지 직접 확인하겠다
# print("2790을 개인키 2753으로 열면:", ...) → 4단계 예고: 2단계에서 잠근 2790이 65로 돌아오는지 보겠다


# step3: 모듈러 역원
#
# mod 세계에는 나눗셈이 없어서, "17에 곱하면 나머지 1이 되는 수"를 찾아 나눗셈 대신 써요.
# step1의 gcd 과정 옆에 "이 나머지는 17을 몇 개 써서 만들었나"라는 기록을 붙여서 같이 계산하고,
# 나머지가 1이 되는 순간의 기록(−367)을 양수로 바꾼 2753이 개인키예요.
# 서로소가 아니면 역원이 없어서 None이 나와요.


# 설명 글 전체 → 줄마다 #를 붙여 주석으로 만들겠다 (파이썬이 읽지 않으므로 실행에 영향 없음)