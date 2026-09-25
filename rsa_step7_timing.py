# 7단계 실험: 소수를 키워가며 공격 시간 재기 (내가 만든 숫자로만 실습)


import time


# import time → 시간을 재는 도구가 들어 있는 파이썬 기본 모듈 time을 가져오겠다




# [0] 문제 정의


print("[0] 문제 정의")
print("질문: n의 자릿수가 커지면 소인수분해 공격 시간은 얼마나 늘어날까?")
print("방법: n을 2자리씩 키워가며 공격 시간을 재고, 그 속도로 실제 RSA(617자리)를 추정한다.")
print()


# print("질문: ...") → 이 실험이 답하려는 질문을 맨 위에 보여주겠다
# print("방법: ...") → 어떤 순서로 답을 찾을지 밝혀두겠다




# [1] 실험 도구
# 개념: 원하는 크기의 소수를 만드는 함수 2개 + step5의 공격 함수


def is_prime(x):
    if x < 2:
        return False
    k = 2
    while k * k <= x:
        if x % k == 0:
            return False
        k += 1
    return True


def next_prime(x):
    while not is_prime(x):
        x += 1
    return x


def factor(n):
    k = 2
    tries = 0
    while k * k <= n:
        tries += 1
        if n % k == 0:
            return k, n // k, tries
        k += 1
    return None


# def is_prime(x): → x가 소수인지 True/False로 알려주는 함수를 만들겠다
# if x < 2: return False → 0과 1은 소수가 아니므로 바로 False를 돌려주겠다
# while k * k <= x: → step5와 같은 요령으로 √x까지만 나눠보겠다
# if x % k == 0: return False → 하나라도 나누어떨어지면 소수가 아니므로 False를 돌려주겠다
# return True → 끝까지 안 나누어떨어지면 소수이므로 True를 돌려주겠다
# def next_prime(x): → x부터 1씩 올라가며 처음 만나는 소수를 찾는 함수를 만들겠다
# while not is_prime(x): → x가 소수가 아닌 동안 계속 1씩 늘리겠다
# def factor(n): → step5의 시도 나눗셈 공격 함수를 그대로 쓰겠다 (step5는 import하면 공격 출력이 같이 실행돼서 복사해 옴)




# [2] 실험: 자릿수를 키워가며 공격 시간 재기
# 개념: n이 2자리 커질 때마다 √n은 1자리(10배) 커지므로, 시도 횟수와 시간도 약 10배씩 늘어날 것이다


print("[2] 실험")

for digits in range(2, 9):
    p = next_prime(3 * 10 ** (digits - 1))
    q = next_prime(2 * p)
    n = p * q

    start = time.perf_counter()
    fp, fq, tries = factor(n)
    elapsed = time.perf_counter() - start

    print(f"n {len(str(n)):2}자리 | p = {p:>9} | q = {q:>9} | {tries:>9}번 시도 | {elapsed:.4f}초")

print()


# for digits in range(2, 9): → p의 자릿수를 2부터 8까지 하나씩 바꿔가며 실험하겠다
# p = next_prime(3 * 10 ** (digits - 1)) → 3, 30, 300, ... 처럼 원하는 자릿수에서 시작해 첫 소수를 p로 삼겠다
# q = next_prime(2 * p) → p의 약 2배 근처에서 다음 소수를 찾아 q로 삼겠다 (p와 다른 소수가 되도록)
# n = p * q → 공격 대상이 될 n을 만들겠다
# start = time.perf_counter() → 공격 직전의 시각을 스톱워치처럼 기록하겠다
# fp, fq, tries = factor(n) → n을 쪼개는 공격을 실행하겠다
# elapsed = time.perf_counter() - start → 공격 직후 시각에서 시작 시각을 빼서 걸린 시간을 구하겠다
# len(str(n)) → n을 글자로 바꿔 글자 수를 세면 자릿수가 되겠다
# {p:>9} → 오른쪽 정렬로 9칸에 맞춰 찍어서 표처럼 줄이 맞게 하겠다
# {elapsed:.4f} → 시간을 소수점 아래 4자리까지 찍겠다




# [3] 추정: 이 속도로 실제 RSA(617자리)를 공격하면?
# 개념: 617자리 n의 √n은 약 309자리, 즉 약 10^308번 시도가 필요하다


rate = tries / elapsed
rsa_tries = 10 ** 308
years = rsa_tries / rate / (60 * 60 * 24 * 365)
universe_years = 1.38e10

print("[3] 추정")
print(f"이 컴퓨터의 공격 속도: 1초에 약 {rate:,.0f}번 시도")
print("617자리 n에 필요한 시도: 약 10^308번")
print(f"예상 시간: 약 {years:.2e}년")
print(f"우주의 나이(약 {universe_years:.2e}년)의 약 {years / universe_years:.2e}배")


# rate = tries / elapsed → 마지막(가장 큰) 실험의 시도 횟수를 시간으로 나눠 1초당 시도 횟수를 구하겠다
# rsa_tries = 10 ** 308 → 617자리 n을 쪼개는 데 필요한 대략의 시도 횟수를 담겠다
# years = rsa_tries / rate / (60 * 60 * 24 * 365) → 필요한 초를 구한 뒤 1년의 초로 나눠 년 단위로 바꾸겠다
# universe_years = 1.38e10 → 우주의 나이 138억 년을 과학적 표기법으로 담겠다 (1.38 × 10^10)
# {rate:,.0f} → 천 단위마다 쉼표를 넣고 소수점 없이 찍겠다
# {years:.2e} → 아주 큰 수를 "2.86e+293"(2.86 × 10^293) 같은 과학적 표기법으로 찍겠다