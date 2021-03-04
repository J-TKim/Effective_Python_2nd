# 주스 바에서 과일 바구니 관리 예제
fresh_fruit = {
    '사과': 10,
    '바나나': 8,
    '레몬': 5,
}

def make_lemonade(count):
    print(f'Making {count} lemons into lemonade')

def out_of_stock():
    print('Out of stock!')

count = fresh_fruit.get('레몬', 0)
if count:
    make_lemonade(count)
else:
    out_of_stock()

# 앞에서 본 코드를 왈러스 연산자(:=)로 다시 쓴 코드
if count := fresh_fruit.get('레몬', 0):
    make_lemonade(count)
else:
    out_of_stock()

# 고객이 사과주스를 구매했을 때 사과의 갯수를 확인하는 코드
def make_cider(count):
    print(f'Making cider with {count} apples')

count = fresh_fruit.get('사과', 0)
if count >= 4:
    make_cider(count)
else:
    out_of_stock()

# 위와같이 변수를 if문 내에서 한번 쓸 경우 왈라스 연산자로 사용 (대입식 괄호 사용해서 묶어주기)
if (count := fresh_fruit.get('사과', 0)) >= 4:
    make_cider(count)
else:
    out_of_stock()

# 바나나 슬라이스 갯수 확인 코드
def slice_bananas(count):
    print(f'Slicing {count} bananas')
    return count * 4

class OutOfBananas(Exception):
    pass

def make_smoothies(count):
    print(f'Making a smoothies with {count} banana slices')

pieces = 0
count = fresh_fruit.get('바나나', 0)
if count >= 2:
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()

# pieces = 0 대입문을 else 블록에 넣기
count = fresh_fruit.get('바나나', 0)
if count >= 2:
    pieces = slice_bananas(count)
else:
    pieces=0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()

# 왈러스 연산자를 적용해 코드 길이 줄이기
pieces = 0
if (count := fresh_fruit.get('바나나', 0)) >= 2:
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()

# 왈러스 연산자와 else문 사용
if (count := fresh_fruit.get('바나나', 0)) >= 2:
    pieces = slice_bananas(count)
else:
    pieces = 0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()

# switch문을 따라한 코드
count = fresh_fruit.get('바나나', 0)
if count >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
else:
    count = fresh_fruit.get('사과', 0)
    if count >= 4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get('레몬', 0)
        if count:
            to_enjoy = make_lemonade(count)
        else:
            to_enjoy = 'Nothing'

# 왈러스 연산자를 사용하면 훨신 간단하게 switch문 구현 가능
if (count := fresh_fruit.get('바나나', 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('사과', 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get('레몬', 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = 'Nothing'

# while루프로 do/while을 구현한 코드
FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

def pick_fruit():
    if FRUIT_TO_PICK:
        return FRUIT_TO_PICK.pop(0)
    else:
        return []

def make_juice(fruit, count):
    return [(fruit, count)]

bottles = []
fresh_fruit = pick_fruit()
while fresh_fruit:
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
    fresh_fruit = pick_fruit()

print(bottles)

# 무한 루프-중간에서 끝내기 관용어 사용 코드
FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

bottles = []
while True: # 무한루프
    fresh_fruit = pick_fruit()
    if not fresh_fruit: # 중간에서 끝내기
        break

    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)

# 위 코드를 왈러스 연산자를 이용해 줄인 방법
FRUIT_TO_PICK = [
    {'apple': 1, 'banana': 3},
    {'lemon': 2, 'lime': 5},
    {'orange': 3, 'melon': 2},
]

bottles = []
while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)