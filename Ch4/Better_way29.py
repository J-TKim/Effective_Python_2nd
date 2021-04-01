# 재고를 확인하는 코드
stock = {
    '못': 125,
    '나사못': 35,
    '나비너트': 8,
    '와셔': 24,
}

order = ['나사못', '나비너트', '클립']

def get_batches(count, size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)

# 딕셔너리 컴프리헨션을 사용해 로직을 더 간결하게 표현할 수 있다.
found = {name: get_batches(stock.get(name, 0), 8)
        for name in order
        if get_batches(stock.get(name, 0), 8)}
print(found)

# 가독성도 좋지 않고 같은 명령어가 반복되기 때문에 수정을 하며 실수할 가능성이 크다.
has_bug = {name: get_batches(stock.get(name, 0), 4)
        for name in order
        if get_batches(stock.get(name, 0), 8)}

print('예상:', found)
print('실제:', has_bug)

# 이러한 문제는 왈러스 연산자 (:=)를 사용하면 쉽게 해결할 수 있다.
found = {name: batches for name in order
        if (batches := get_batches(stock.get(name, 0), 8))}

# 왈러스 연산자를 사용할 때는 순서를 조심해야한다.
try:
    result = {name: (tenth := count // 10)
            for name, count in stock.items() if tenth > 0}
except NameError:
    print("NameError: name 'tenth' is not defined")

# 순서를 잘 설정하면 문제를 해결할 수 있다.
result = {name: tenth for name, count in stock.items()
            if (tenth := count // 10) > 0}
print(result)

# 왈러스 연산자에 대해 그 값에 대한 조건부분이 없다면 루프 밖 영역으로 루프 변수가 누출된다.
half = [(last := count // 2) for count in stock.values()]
print(f'{half}의 마지막 원소는 {last}')

# for문의 변수 누출과 비슷하다.
for count in stock.values():
    pass
print(f'{list(stock.values())}의 마지막 원소는 {count}')

# 컴프리헨션의 루프의 경우에는 누출이 생기지 않음
half = [ccount // 2 for ccount in stock.values()]
print(half) # 작동
try:
    print(ccount) # 에러 발생
except NameError:
    print("NameError: name 'ccount' is not defined")

# 대입식은 제너레이터의 경우에도 똑같은 방식으로 작동한다.
found = ((name, batches) for name in order
        if (batches := get_batches(stock.get(name, 0), 8)))
print(next(found))
print(next(found))