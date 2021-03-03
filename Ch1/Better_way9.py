# 파이썬에서는 루프가 반복 수행되는 내부 블록 다음에 else 블록을 추가할 수 있다
for i in range(3):
    print('Loop', i)
else:
    print('Else block!')

# else는 처리할 예외가 없을 때 이 블록을 실행하라 라는 의미이다

# 루프 안에서 break문을 사용하면 else블록이 실행되지 않는다
for i in range(3):
    print('Loop', i)
    if i == 1:
        break
else:
    print('Else block!')

# 빈 시퀀스에 대한 루프를 실행하면 else 블록이 바로 실행된다
for x in []:
    print('이 줄은 실행되지 않음')
else:
    print('For Else block!')

# While문의 조건이 False인 경우에도 else블록이 바로 실행된다
while False:
    print('이 줄은 실행되지 않음')
else:
    print('While Else block!')

# 서로소인지 확인하는 코드
a = 4
b = 9

for i in range(2, min(a, b) + 1):
    print('검사 중', i)
    if a % i == 0 and b % i == 0:
        print('서로소 아님')
        break
else:
    print('서로소')

# 서로소인지 확인하는 코드 2
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True

assert coprime(4, 9)
assert not coprime(3, 6)

# 서로소인지 확인하는 코드 3
def coprime_alternate(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime

assert coprime(4, 9)
assert not coprime(3, 6)