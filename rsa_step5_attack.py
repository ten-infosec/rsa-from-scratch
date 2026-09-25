# 5단계 : 공격자 시점 - 공개키만으로 개인키 훔치기 ( 내가 만든 장난감 키로만 실습 )

from rsa_step2 import mod_pow
from rsa_step3 import mod_inverse



def factor(n) : 
    k = 2
    tries = 0 
    while k * k <= n : 
        tries += 1
        if n % k == 0 : 
            return k, n // k, tries
        k += 1  
    return None 
    
    
    

# from rsa_step2 ... / form rsa_step3 ... -> 암호를 여는 데 필요한 도구 두개를 가져오겠다. 
# def factor(n): -> n을 두 수의 곱으로 쪼개는 함수를 만들겠다. 
# k = 2 -> 나눠볼 수를 2부터 시작하겠다 (1은 모든 수를 나누니 의미없음)
# tries = 0 -> 몇 번 시도했는지 세겠다. 
# while k*k <= n : -> k를 제곱한 값이 n 이하인 동안만 반복하겠다. ( 이유는 아래 설명 )
# if n % k == 0: -> n이 k로 딱 나누어 떨어지면 
# return k, n // k, tries -> 찾은 두 약수와 시도 횟수를 돌려주겠다. 
# k += 1 -> 안 나누어 떨어지면 다음 수로 넘어가겠다.
# retrun None -> 끝까지 못 찾으면 n은 소수라서 쪼갤 수 없다는 뜻으로 None을 돌려주겠다. 


# 공격 실행 


e , n = 17, 3233
c = 2790


p, q, tries = factor(n)
phi = (p - 1) * (q - 1) 
d = mod_inverse(e, phi)
m = mod_pow(c, d, n )

print(f"공격자가 가진 것 : 공개키 (e, n) = ({e}, {n}) , 가로챈 암호문 = {c}")
print(f"① 소인수분해: {n} = {p} x {q} ({tries}번 시도)")
print(f"② phi = ({p}-1) x ({q}-1) = {phi}")
print(f"③ 개인키 d = {d}")
print(f"④ 암호문 {c}를 열면 : {m}")



# e, n = 17, 3233 → 공개된 공개키를 준비하겠다
# c = 2790 → 공격자가 중간에서 가로챈 암호문이라고 가정하겠다
# p, q, tries = factor(n) → 3233을 쪼개서 두 소수와 시도 횟수를 얻겠다
# phi = (p - 1) * (q - 1) → 키 주인만 알던 비밀값 phi를 계산하겠다
# d = mod_inverse(e, phi) → 3단계 함수로 개인키를 만들어내겠다
# m = mod_pow(c, d, n) → 훔친 개인키로 암호문을 열겠다



# step5: 공격자 시점
#
# 공개키 (17, 3233)만 가지고 2부터 하나씩 나눠서 52번 만에 3233 = 53 × 61을 찾고,
# phi와 d를 계산해 2790을 65로 열었어요. √n까지만 보면 된다는 요령(k * k <= n)도 배웠죠.
# 617자리 n이면 이 방법은 우주의 나이로도 불가능하지만, 양자컴퓨터의 쇼어 알고리즘은 가능하게 만들어요.


# 설명 글 전체 → 줄마다 #를 붙여 주석으로 만들겠다 (파이썬이 읽지 않으므로 실행에 영향 없음)