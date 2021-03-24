# 숫자로 이루어진 list의 앞쪽에 우선순위를 부여한 몇몇 숫자를 위치하고 정렬하기

# sort 메서드에 key 인자로 도우미 함수를 전달한다.
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 4, 7}
sort_priority(numbers, group)
print(numbers)
# 파이썬은 비교할 때 0번 인덱스 값을 비교한 뒤, 이 값이 같으면 뒤의 값으로 비교한다.

# 우선순위가 높은 원소가 있는지 체크하는 함수
def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 4, 7}
found = sort_priority2(numbers, group)
print(f'발견: {found}') # 정렬 결과는 맞지만 False를 출력한다.
print(numbers)
"""
파이썬은 아래의 순서대로 변수를 찾아본다.
1. 현재 함수의 영역
2. 현재 함수를 둘러싼 영역(현재 함수를 둘러싸고 있는 함수 등)
3. 현재 코드가 들어 있는 모듈의 영역(전역 영역)
4. 내장 영역
"""

# 위 네 영역에 변수가 없으면 NameError가 발생한다.
try:
    foo = does_not_exist * 5
except NameError:
    print("NameError: name 'does_not_exist' is not defined")

"""
변수 대입의 경우에는 변수가 현재 영역에 이미 정의돼 있다면 그 변수의 값만 새로운 값으로 변한다.
위 문제 때문에 found가 바뀌지 않은 것 이다.
"""
def sort_priority2(numbers, group):
    found = False # sort_priority2 안에 있는 변수
    def helper(x):
        if x in group:
            found = True # helper의 변수
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# 클로저 밖으로 데이터를 끌어내는 구문인 nonlocal을 사용하여 해결 가능하다.
def sort_priority2(numbers, group):
    found = False 
    def helper(x):
        nonlocal found # 추가
        if x in group:
            found = True 
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# nonlocal을 쓰면 이해하기가 어려워지므로 도우미 함수로 상태를 감싸는걸 고려해보자.
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False
    
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True