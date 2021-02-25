# 파이썬에는 불변 순서쌍을 만들어 낼 수 있는 tuple이 있다
snack_calories = {
    '감자칩': 140,
    '팝콘': 80,
    '땅콩': 190,
}

items = tuple(snack_calories.items())
print(items)

# 튜플에 있는 값은 인덱스를 사용해 접근이 가능하다
item = ('호박엿', '식혜')
first = item[0]
second = item[1]
print(first, '&', second)

# 튜플은 한번 생성되면 새 값을 대입하는 변경이 불가능하다
# pair = ('약과', '호박엿')
# pair[0] = '타래과'
# TypeError: 'tuple' object does not support item assignment

# 파이썬에는 언패킹 구문이 존재한다
item = ('호박엿', '식혜')
first, second = item # 언패킹
print(first, '&', second)

# 언패킹 사용 예시
favorite_snacks = {
    '짭조름한 과자': ('프레즐', 100),
    '달콤한 과자': ('쿠키', 180),
    '채소': ('당근', 20),
}

((type1, (name1, cals1)),
 (type2, (name2, cals2)),
 (type3, (name3, cals3))) = favorite_snacks.items()

print(f'제일좋아하는 {type1} 는 {name1}, {cals1} 칼로리입니다.')
print(f'제일좋아하는 {type2} 는 {name2}, {cals2} 칼로리입니다.')
print(f'제일좋아하는 {type3} 는 {name3}, {cals3} 칼로리입니다.')

# 정렬하는 과정에서 temp사용하는 예시
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                temp = a[i]
                a[i] = a[i-1]
                a[i-1] = temp

names = ['프레즐', '당근', '쑥갓', '베이컨']
bubble_sort(names)
print(names)

# 정렬 과정에서 언패킹 구문 사용하는 예시
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                a[i-1], a[i] = a[i], a[i-1] # 맞바꾸기

names = ['프레즐', '당근', '쑥갓', '베이컨']
bubble_sort(names)
print(names)

# 언패킹을 하지 않고 간식이 들어있는 list를 순환하는 코드
snacks = [('베이컨', 350), ('도넛', 240), ('머핀', 190)]
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name} 은 {calories} 칼로리 입니다.')

# enumerate 내장 함수와 언패킹을 사용한 같은 코드
snacks = [('베이컨', 350), ('도넛', 240), ('머핀', 190)]
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} 은 {calories} 칼로리 입니다.')