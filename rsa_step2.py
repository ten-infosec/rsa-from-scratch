# 2단계: 모듈러 거듭제곱 (base의 exp제곱을 mod로 나눈 나머지) 빠르게 구하기


def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp = exp // 2
    return result


# def mod_pow(base, exp, mod): → base를 exp번 곱한 값을 mod로 나눈 나머지를 구하는 함수를 만들겠다
# result = 1 → 답을 모아갈 그릇을 1로 시작하겠다 (곱셈의 시작값이라 0이 아니라 1)
# base = base % mod → 시작부터 base를 mod 범위 안으로 줄여두겠다
# while exp > 0: → exp가 0보다 큰 동안 계속 반복하겠다 (exp가 0이 되는 순간 멈춤)
# if exp % 2 == 1: → exp가 홀수면(= 지금 보는 2진수 자리가 1이면)
# result = (result * base) % mod → 지금의 base를 답에 곱해 넣고 나머지만 남기겠다
# base = (base * base) % mod → 다음 자리를 위해 base를 제곱해두고 나머지만 남기겠다
# exp = exp // 2 → exp를 반으로 나눠(몫만) 다음 2진수 자리로 넘어가겠다
# return result → 모아온 답을 돌려주겠다




# 2단계 가시화: mod_pow의 매 바퀴를 문장으로 풀어서 보여주기


def mod_pow_trace(base, exp, mod):
    result = 1
    base = base % mod
    print(f"시작: exp={exp} → 2진수로 {bin(exp)[2:]} / result={result}, base={base}")
    count = 1
    while exp > 0:
        if exp % 2 == 1:
            new_result = (result * base) % mod
            print(f"{count}바퀴: exp={exp} 홀수 → result = {result}×{base} mod {mod} = {new_result}")
            result = new_result
        else:
            print(f"{count}바퀴: exp={exp} 짝수 → result 그대로 {result}")
        new_base = (base * base) % mod
        print(f"       다음 준비: base = {base}×{base} mod {mod} = {new_base}, exp = {exp}//2 = {exp // 2}")
        base = new_base
        exp = exp // 2
        count += 1
    print("exp가 0이 됨 → 멈춤")
    return result


# bin(exp)[2:] → exp를 2진수 글자로 바꾸겠다 (bin(13)은 '0b1101'이라, 앞의 '0b' 두 글자를 [2:]로 잘라내겠다)
# if exp % 2 == 1: ... new_result = ... → 홀수면 곱하기 전 값과 곱한 후 값을 둘 다 보여주려고 new_result에 먼저 담아두겠다
# print(f"{count}바퀴: ... 홀수 ...") → 어떤 두 수를 곱해서 새 result가 됐는지 찍겠다
# else: → 홀수가 아니면(= 짝수면)
# print(f"... 짝수 → result 그대로 ...") → 이번 바퀴는 result를 건드리지 않았다고 찍겠다
# new_base = (base * base) % mod → 다음 base를 먼저 계산해두겠다
# print(f"       다음 준비: ...") → 다음 바퀴를 위해 base를 어떻게 제곱했고 exp를 어떻게 반으로 줄였는지 찍겠다
# base = new_base / exp = exp // 2 → 실제로 base와 exp를 다음 바퀴 값으로 바꾸겠다
# count += 1 → 바퀴 번호를 1 늘리겠다




# 확인: 여러 숫자로 과정과 결과 보기

if __name__ == "__main__":
    
    print("답:", mod_pow_trace(3, 13, 7))
    print()
    print("답:", mod_pow_trace(3, 8, 7))
    print()
    print("mod_pow 결과:", mod_pow(3, 13, 7), mod_pow(3, 8, 7), mod_pow(3, 0, 7))
    print("pow 검산:", pow(3, 13, 7), pow(3, 8, 7), pow(3, 0, 7))
    print()
    print("65를 공개키(17, 3233)로 잠그면:", mod_pow(65, 17, 3233))


# print("답:", mod_pow_trace(3, 13,

# step2: 모듈러 거듭제곱
#
# 65를 17번 곱하는 걸 그냥 하면 숫자가 폭발하고, 실제 RSA처럼 지수가 수백 자리면 영원히 안 끝나요.
# 그래서 지수를 2진수로 읽으면서 홀수 자리(1인 자리)에서만 result에 곱하고, base는 매번 제곱해 둬요.
# 13(= 1101)이면 4바퀴 중 세 번 곱하고, 8(= 1000)이면 마지막 한 번만 곱했죠.
# 곱할 때마다 % mod를 해서 숫자가 커지지 않게 눌러줘요. 이게 암호화와 복호화의 엔진이에요.


# 설명 글 전체 → 줄마다 #를 붙여 주석으로 만들겠다 (파이썬이 읽지 않으므로 실행에 영향 없음)