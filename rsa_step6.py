# 6단계 점검: 복호화가 원문을 돌려주는 이유를 숫자로 하나씩 짚기


from rsa_step1 import gcd
from rsa_step3 import mod_inverse


# from rsa_step1 import gcd → 서로소 검사에 쓸 gcd를 가져오겠다
# from rsa_step3 import mod_inverse → 개인키 d를 구할 mod_inverse를 가져오겠다
# (거듭제곱은 결과가 같은 파이썬 내장 pow를 쓰겠다)




# [0] 문제 정의: 우리가 증명하려는 것


print("[0] 문제 정의")
print("목표: 원문 m을 e번 곱해서 잠그고(암호화), 그 결과를 d번 곱해서 열면(복호화), 반드시 m이 돌아온다.")
print("조건: 모든 곱셈은 n으로 나눈 나머지 세계에서 한다.")
print("순서: [1] 예시 만들기 → [2] 도구 두 개 → [3] 오일러 정리 → [4] 조립 → [5] 전자서명 → [6] 안전성")
print()


# print("목표: ...") → 이 파일이 증명하려는 명제를 실행 결과 맨 위에 먼저 보여주겠다
# print("조건: ...") → 모든 계산이 mod n 세계에서 일어난다는 전제를 밝히겠다
# print("순서: ...") → 아래 섹션들이 목표를 향해 어떤 순서로 가는지 지도처럼 보여주겠다




# [1] 초미니 RSA 만들기
# 개념: 손으로 확인 가능한 작은 숫자(n=33)로 RSA를 만들어 증명의 재료로 쓴다. 핵심 재료는 e×d = phi의 배수 + 1


p, q = 3, 11
n = p * q
phi = (p - 1) * (q - 1)
e = 3
d = mod_inverse(e, phi)
m = 4
c = pow(m, e, n)

print("[1] 초미니 RSA 만들기")
print(f"n = {p}×{q} = {n}, phi = ({p}-1)×({q}-1) = {phi}")
print(f"gcd(e, phi) = gcd({e}, {phi}) = {gcd(e, phi)} → e = {e} 사용 가능")
print(f"d = {e}의 역원 (mod {phi}) = {d} → 검산: {e}×{d} = {e * d} = {phi}×{(e * d) // phi} + {(e * d) % phi}")
print(f"암호화: {m}^{e} mod {n} = {c}")
print(f"복호화: {c}^{d} mod {n} = {pow(c, d, n)}")
print()


# p, q = 3, 11 → 손으로 계산 가능한 작은 소수 두 개를 고르겠다
# n, phi → 4단계와 같은 공식으로 n = 33, phi = 20을 만들겠다
# d = mod_inverse(e, phi) → 3단계 함수로 개인키 7을 구하겠다
# c = pow(m, e, n) → 원문 4를 공개키로 잠가 31을 만들겠다
# print(f"d = ... 검산: ...") → e×d가 "phi × 몫 + 1" 모양인지 보여주겠다




# [2-ⓐ] 지수법칙: 곱하는 횟수는 쪼개고 묶을 수 있다
# 개념: 잠갔다 여는 것 = m을 e×d번 곱하는 것. 곱하는 횟수를 phi 묶음과 나머지로 쪼갤 수 있게 해준다


print("[2-ⓐ] 지수법칙")
print(f"2^5 = {2 ** 5} / 2^3 × 2^2 = {2 ** 3} × {2 ** 2} = {2 ** 3 * 2 ** 2}")
print(f"(2^3)^2 = {(2 ** 3) ** 2} / 2^6 = {2 ** 6}")
print(f"잠갔다 열기 ({m}^{e})^{d} mod {n} = {pow(pow(m, e, n), d, n)} / {m}^{e * d} mod {n} = {pow(m, e * d, n)}")
print()


# 2 ** 5 → 파이썬에서 **는 거듭제곱 기호: 2를 5번 곱하겠다
# 2 ** 3 * 2 ** 2 → 5번 곱하기를 3번과 2번으로 쪼개도 같은지 보겠다
# (2 ** 3) ** 2 → 3번 곱한 걸 2번 곱하면 6번 곱한 것과 같은지 보겠다
# pow(pow(m, e, n), d, n) vs pow(m, e * d, n) → "잠갔다 열기"가 "e×d번 곱하기"와 같은지 보겠다




# [2-ⓑ] mod 곱셈: 중간에 나머지로 바꿔도 결과가 같다
# 개념: 긴 곱셈 중 나머지가 1인 덩어리는 통째로 1로 바꿔도 된다


a, b, k = 13, 9, 5

print("[2-ⓑ] mod 곱셈")
print(f"{a}×{b} mod {k} = {a * b} mod {k} = {a * b % k}")
print(f"({a} mod {k})×({b} mod {k}) mod {k} = {a % k}×{b % k} mod {k} = {(a % k) * (b % k) % k}")
print()


# a, b, k = 13, 9, 5 → 예시 숫자 세 개를 한 번에 담겠다
# a * b % k → 먼저 곱하고 나중에 나머지를 구하겠다
# (a % k) * (b % k) % k → 먼저 각각 나머지로 바꾼 뒤 곱하고 다시 나머지를 구하겠다 (결과가 같아야 함)




# [3] 오일러 정리: 섞기 증명
# 개념: m이 n과 서로소면 m을 phi번 곱한 나머지는 1이다. 서로소 묶음에 m을 곱하면 순서만 섞이기 때문


def shuffle_proof(n, a):
    group = [x for x in range(1, n) if gcd(x, n) == 1]
    shuffled = [x * a % n for x in group]
    print(f"{n}과 서로소인 수 묶음: {group} → {len(group)}개")
    print(f"각각 ×{a} mod {n}: {shuffled}")
    print(f"정렬하면 같은 묶음인가? {sorted(shuffled) == group}")
    print(f"{a}^{len(group)} mod {n} = {pow(a, len(group), n)}")


print("[3] 오일러 정리: 섞기 증명")
shuffle_proof(10, 3)
print()
shuffle_proof(33, 4)
print()


# def shuffle_proof(n, a): → n 세계에서 a를 곱했을 때 서로소 묶음이 섞이기만 하는지 보여주는 함수를 만들겠다
# group = [x for x in range(1, n) if gcd(x, n) == 1] → 1부터 n-1 중 n과 서로소인 수만 골라 묶음을 만들겠다 (개수 = phi)
# shuffled = [x * a % n for x in group] → 묶음의 각 수에 a를 곱하고 n으로 나눈 나머지로 새 목록을 만들겠다
# sorted(shuffled) == group → 새 목록을 크기순으로 정렬하면 원래 묶음과 똑같은지 True/False로 확인하겠다
# pow(a, len(group), n) → 결론대로 a를 phi번 곱한 나머지가 1인지 확인하겠다
# shuffle_proof(33, 4) → 설명의 n=10 예시뿐 아니라 초미니 RSA의 n=33에서도 같은지 보겠다




# [4] 조립: 복호화가 원문을 돌려주는 과정
# 개념: m^(e×d) = m^(phi×t + 1) = (m^phi)^t × m = 1^t × m = m. phi 묶음은 사라지고 "+1"이 m 하나를 남긴다


t = (e * d) // phi

print("[4] 조립")
print(f"① {c}^{d} mod {n} = {pow(c, d, n)}")
print(f"② = {m}^({e}×{d}) = {m}^{e * d} mod {n} = {pow(m, e * d, n)}")
print(f"③ = {m}^({phi}×{t} + 1) mod {n} = {pow(m, phi * t + 1, n)}")
print(f"④ = ({m}^{phi})^{t} × {m} → {m}^{phi} mod {n} = {pow(m, phi, n)} 이므로 1^{t} × {m} = {pow(pow(m, phi, n), t, n) * m % n}")
print()

E, D, N, PHI, M = 17, 2753, 3233, 3120, 65
T = (E * D) // PHI

print(f"실제 숫자: {E}×{D} = {E * D} = {PHI}×{T} + {(E * D) % PHI}")
print(f"{M}^{PHI} mod {N} = {pow(M, PHI, N)} 이므로 1^{T} × {M} = {pow(pow(M, PHI, N), T, N) * M % N}")
print()


# t = (e * d) // phi → e×d 안에 phi가 몇 묶음 들어있는지(몫) 구하겠다
# ① → 실제 복호화 결과를 보겠다
# ② → 지수법칙으로 "e×d번 곱하기"로 바꿔도 같은지 보겠다
# ③ → e×d를 "phi×t + 1"로 바꿔 써도 같은지 보겠다
# ④ → phi번 곱한 덩어리가 1이 되어, 결국 m 하나만 남는 걸 보겠다
# E, D, N, PHI, M = ... → 대문자 변수로 실제 RSA 숫자(3233)를 따로 담아 같은 과정을 확인하겠다




# [5] 거꾸로: 전자서명
# 개념: e×d와 d×e는 같으므로 개인키로 먼저 잠가도 공개키로 풀린다. 열렸다는 사실이 주인의 서명이 된다


s = pow(m, d, n)

print("[5] 전자서명")
print(f"개인키로 잠금: {m}^{d} mod {n} = {s}")
print(f"공개키로 열림: {s}^{e} mod {n} = {pow(s, e, n)}")
print()


# s = pow(m, d, n) → 순서를 바꿔 개인키 d로 먼저 잠그겠다
# pow(s, e, n) → 그걸 누구나 가진 공개키 e로 열어 원문이 돌아오는지 보겠다




# [6] 안전성: 공격자는 n을 쪼개야만 d를 만든다
# 개념: 위 수학은 전부 공개돼 있다. 비밀은 p, q뿐이고, 방어선은 n의 소인수분해가 어렵다는 것 하나다


for x in range(2, n):
    if n % x == 0:
        fp, fq = x, n // x
        break

fphi = (fp - 1) * (fq - 1)

print("[6] 안전성")
print(f"{n} = {fp}×{fq} → phi = {fphi} → d = {mod_inverse(e, fphi)}")


# for x in range(2, n): → 2부터 n-1까지 하나씩 나눠보겠다
# if n % x == 0: → 딱 나누어떨어지는 수를 찾으면
# fp, fq = x, n // x → 그 수와 짝이 되는 수를 두 소수로 삼겠다
# break → 찾았으니 반복을 즉시 끝내겠다
# fphi, mod_inverse(e, fphi) → 공격자가 phi와 개인키를 계산해내는 걸 보겠다



# step6: 왜 되는지 증명
#
# 초미니 RSA(n = 33, e = 3, d = 7)로 한 줄도 건너뛰지 않고 따라갔어요.
#
# 31^7 = (4^3)^7 = 4^21 = 4^(20×1 + 1) = (4^20)^1 × 4 = 1 × 4 = 4
#
# 오일러 정리(서로소면 m을 phi번 곱한 나머지는 1)가 핵심이고, 그 이유는 서로소 묶음에 m을 곱하면
# 순서만 섞이기 때문이었어요. e × d를 d × e로 바꿔도 같으니 개인키로 잠그고 공개키로 여는 전자서명도 성립하고요.


# 설명 글 전체 → 줄마다 #를 붙여 주석으로 만들겠다 (파이썬이 읽지 않으므로 실행에 영향 없음)