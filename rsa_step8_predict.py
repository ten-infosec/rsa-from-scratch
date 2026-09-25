# 8단계 실험: 7단계에서 찾은 "10배 법칙"으로 18자리 공격 시간을 예측하고 검증하기


import time


# import time → 시간을 재는 도구가 들어 있는 파이썬 기본 모듈 time을 가져오겠다




# [0] 문제 정의


print("[0] 문제 정의")
print("관찰(7단계): n이 2자리 커질 때마다 공격 시간이 약 10배 늘었다. (16자리: 약 4초)")
print("예측: 18자리는 약 3억 번 시도, 약 40초가 걸릴 것이다.")
print("검증: 실제로 18자리까지 공격해서 예측과 비교한다.")
print()


# print("관찰 ...") → 7단계에서 발견한 법칙과 기준 숫자를 적어두겠다
# print("예측 ...") → 실행 전에 예측값을 먼저 못 박아두겠다 (결과를 보고 끼워 맞추지 않도록)
# print("검증 ...") → 이 파일이 할 일을 밝히겠다




# [1] 실험 도구
# 개념: 7단계와 같은 도구 (소수 만들기 2개 + 공격 함수)


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


# is_prime, next_prime, factor → 7단계와 똑같은 함수를 그대로 쓰겠다 (7단계 파일은 import하면 실험 전체가 실행돼서 복사해 옴)




# [2] 실험: 18자리까지 공격 시간 재기
# 개념: 7단계와 같은 실험을 한 칸(18자리) 더 가서, 결과를 목록에 모아 둔다


print("[2] 실험 (18자리는 약 40초 걸릴 수 있으니 기다려주세요)")

results = []

for digits in range(2, 10):
    p = next_prime(3 * 10 ** (digits - 1))
    q = next_prime(2 * p)
    n = p * q

    start = time.perf_counter()
    fp, fq, tries = factor(n)
    elapsed = time.perf_counter() - start

    results.append((len(str(n)), tries, elapsed))
    print(f"n {len(str(n)):2}자리 | p = {p:>9} | q = {q:>9} | {tries:>9}번 시도 | {elapsed:.4f}초")

print()


# print("[2] 실험 (...)") → 마지막 실험이 오래 걸려 멈춘 것처럼 보일 수 있다고 미리 알려주겠다
# results = [] → 실험 결과를 모아 둘 빈 목록을 만들겠다
# for digits in range(2, 10): → p의 자릿수를 2부터 9까지 바꿔가며 실험하겠다 (n은 18자리까지)
# results.append((len(str(n)), tries, elapsed)) → (n 자릿수, 시도 횟수, 시간)을 한 묶음으로 목록 끝에 추가하겠다




# [3] 검증: 예측과 실제 비교
# 개념: 실행 전에 적은 예측값과 실제 결과를 나란히 놓고, 10배 법칙이 맞았는지 판단한다


prev_digits, prev_tries, prev_time = results[-2]
last_digits, last_tries, last_time = results[-1]
predicted_tries = 300_000_000
predicted_time = 40

print("[3] 검증")
print(f"시도 횟수 → 예측 약 {predicted_tries:,}번 / 실제 {last_tries:,}번")
print(f"시간 → 예측 약 {predicted_time}초 / 실제 {last_time:.1f}초")
print(f"{prev_digits}자리 → {last_digits}자리 시간 배율: {last_time / prev_time:.1f}배 (예측: 약 10배)")
print(f"1초당 시도 횟수: {prev_digits}자리 {prev_tries / prev_time:,.0f}번 / {last_digits}자리 {last_tries / last_time:,.0f}번")


# prev_digits, prev_tries, prev_time = results[-2] → 목록의 뒤에서 두 번째(16자리) 결과를 세 변수로 나눠 담겠다
# last_digits, last_tries, last_time = results[-1] → 목록의 맨 마지막(18자리) 결과를 세 변수로 나눠 담겠다
# predicted_tries = 300_000_000 → 예측한 시도 횟수 3억을 담겠다 (숫자 사이 _는 읽기 편하게 끊어 쓰는 표시, 값은 같음)
# predicted_time = 40 → 예측한 시간 40초를 담겠다
# last_time / prev_time → 18자리 시간을 16자리 시간으로 나눠 몇 배 늘었는지 구하겠다
# prev_tries / prev_time, last_tries / last_time → 두 실험의 1초당 시도 횟수를 비교해, 컴퓨터 속도가 일정한지 보겠다git