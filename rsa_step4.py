# 4단계: 1~3단계 도구를 불러와 작은 RSA 완성하기


from rsa_step1 import gcd
from rsa_step2 import mod_pow
from rsa_step3 import mod_inverse


# from rsa_step1 import gcd → rsa_step1.py 파일에서 gcd 함수만 골라 가져오겠다
# from rsa_step2 import mod_pow → rsa_step2.py 파일에서 mod_pow 함수만 골라 가져오겠다
# from rsa_step3 import mod_inverse → rsa_step3.py 파일에서 mod_inverse 함수만 골라 가져오겠다




# 4단계-1: 키 만들기


p = 61
q = 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17
d = mod_inverse(e, phi)

print(f"소수 p = {p}, q = {q}")
print(f"n = p × q = {n}")
print(f"phi = (p-1) × (q-1) = {phi}")
print(f"gcd(e, phi) = gcd({e}, {phi}) = {gcd(e, phi)} → 1이므로 e = {e} 사용 가능")
print(f"d = e의 역원 = {d}")
print(f"공개키 (e, n) = ({e}, {n})")
print(f"개인키 (d, n) = ({d}, {n})")


# p = 61, q = 53 → 비밀로 간직할 두 소수를 고르겠다
# n = p * q → 두 소수를 곱해 공개할 모듈러스 n을 만들겠다
# phi = (p - 1) * (q - 1) → p와 q를 아는 사람만 계산할 수 있는 비밀값 phi를 만들겠다
# e = 17 → 공개키로 쓸 수를 고르겠다
# d = mod_inverse(e, phi) → 3단계 함수로 e의 역원을 구해 개인키 d로 삼겠다
# print(f"gcd(e, phi) ...") → 1단계 함수로 e가 phi와 서로소인지 검사한 결과를 보여주겠다




# 4단계-2: 암호화와 복호화


def encrypt(m, e, n):
    return mod_pow(m, e, n)


def decrypt(c, d, n):
    return mod_pow(c, d, n)


m = 65
c = encrypt(m, e, n)
m2 = decrypt(c, d, n)

print()
print(f"원문 m = {m}")
print(f"암호화: {m}^{e} mod {n} = {c}")
print(f"복호화: {c}^{d} mod {n} = {m2}")
print("원문과 같은가?", m == m2)


# def encrypt(m, e, n): → 원문 m을 공개키 (e, n)으로 잠그는 함수를 만들겠다 (m을 e번 곱하고 n으로 나눈 나머지)
# def decrypt(c, d, n): → 암호문 c를 개인키 (d, n)으로 여는 함수를 만들겠다 (c를 d번 곱하고 n으로 나눈 나머지)
# m = 65 → 보낼 메시지를 숫자 65로 정하겠다 (n보다 작아야 함)
# c = encrypt(m, e, n) → 65를 공개키로 잠가 암호문을 만들겠다
# m2 = decrypt(c, d, n) → 암호문을 개인키로 열어 되돌리겠다
# print("원문과 같은가?", m == m2) → 원문과 복호문이 같은지 True/False로 확인하겠다




# 확인: 여러 메시지로 잠갔다 열어보기


print()
for msg in [0, 1, 42, 65, 1234, 3232]:
    enc = encrypt(msg, e, n)
    dec = decrypt(enc, d, n)
    print(f"원문 {msg:4} → 암호문 {enc:4} → 복호문 {dec:4}")


# for msg in [0, 1, 42, 65, 1234, 3232]: → 리스트 안의 숫자를 하나씩 msg에 담아가며 아래를 반복하겠다
# enc = encrypt(msg, e, n) → 이번 숫자를 공개키로 잠그겠다
# dec = decrypt(enc, d, n) → 잠근 걸 개인키로 다시 열겠다
# print(f"원문 {msg:4} ...") → 원문, 암호문, 복호문을 네 칸 너비로 맞춰 한 줄에 찍겠다


# step4: RSA 완성
#
# p = 61, q = 53 → n = 3233(공개) → phi = 3120(비밀) → e = 17(공개, gcd 검사 통과) → d = 2753(비밀, 역원).
# 65를 공개키로 잠그면 2790, 개인키로 열면 65.
# 그리고 0, 1, 3232는 암호화해도 그대로 나오는 걸 보면서, 실제 RSA에 패딩이 필요한 이유도 확인했어요.


# 설명 글 전체 → 줄마다 #를 붙여 주석으로 만들겠다 (파이썬이 읽지 않으므로 실행에 영향 없음)