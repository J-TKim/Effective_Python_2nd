import random
random.seed(1234)

# range 내장 함수는 정수 집합을 이터레이션하는 루프가 필요할 때 유용하다
from random import randint


random_bits = 0
for i in range(32):
    if randint(0, 1):
        random_bits |= 1 << i

print(bin(random_bits))

# 반복할 데이터 구조가 있으면 시퀀스에 대해 바로 루프를 돌 수 있다
flavor_list = ['바닐라', '초콜릿', '피칸', '딸기']
for flavor in flavor_list:
    print(f'{flavor} 맛있어요.')

# 리스트를 이터레이션 하며 리스트의 인덱스도 필요한 경우
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i+1}: {flavor}')

# next를 이용해 원소를 가져오는 경우
it = enumerate(flavor_list)
print(next(it))
print(next(it))

# enumerate를 이용한 더 간단한 식
for i, flavor in enumerate(flavor_list):
    print(f'{i+1}: {flavor}')

# enumerate의 두번 째 파라미터로 어디서부터 수를 세기 시작할지 정할 수 있다.
for i, flavor in enumerate(flavor_list, 1):
    print(f'{i}: {flavor}')