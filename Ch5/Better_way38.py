# sort의 key값을 len으로 설정하면 단어 길이 순 으로 리스트를 정렬할 수 있다.
names = ['소크라테스', '아르키메데스', '플라톤', '아리스토텔레스']
names.sort(key=len)
print(names)

# 존재하지 않는 키에 접근할 때 로그를 남기고 0을 반환하는 코드
def log_missing():
    print('키 추가됨')
    return 0

# 위 처럼 만든 함수를 defaultdict의 디폴트값으로 사용할 수 있다.
from collections import defaultdict

current = {'초록': 12, '파랑': 3}
increments = [
    ('빨강', 5),
    ('파랑', 17),
    ('주황', 9),
]
result = defaultdict(log_missing, current)
print('이전', dict(result))
for key, amount in increments:
    result[key] += amount
print('이후', dict(result))

# default에 전달하는 디폴트 값 훅이 존재하지 않는 키에 접근한 총 횟수를 세는 코드
def increment_with_report(current, increments):
    added_count = 0
    
    def missing():
        nonlocal added_count # 상태가 있는 클로저
        added_count += 1
        return 0
    
    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count

result, count = increment_with_report(current, increments)
assert count == 2

# 클래스를 이용하는 방법도 있다.
class CountMissing:
    def __init__(self):
        self.added = 0
    
    def missing(self):
        self.added += 1
        return 0

# 파이썬은 CountMissing.missing 메서드를 직접 디폴트 값 훅으로 전달할 수 있다.
counter = CountMissing()
result = defaultdict(counter.missing, current) # 메서드 참조
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

# class의 __call__을 사용해 객체를 함수처럼 사용할 수 있다.
class BetterCountMissing:
    def __init__(self):
        self.added = 0
    
    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)

counter = BetterCountMissing()
result = defaultdict(counter, current) # __call__에 의존
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

