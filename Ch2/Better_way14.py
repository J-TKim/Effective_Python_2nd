# 정수 리스트를 작은 수 부터 큰 수 까지 순서대로 정렬하는 코드
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)

# 건설현장의 여러 도구를 표현하는 클래스
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

tools = [
    Tool('수준계', 3.5),
    Tool('해머', 1.25),
    Tool('스크류드라이버', 0.5),
    Tool('끌', 0.25),
]

# sort 매서드가 호출하는 객체 비교 특별 메서드가 정의돼 있지 않으므로 에러가 발생
try:
    tools.sort()
except TypeError:
    print("TypeError: '<' not supported between instances of 'Tool' and 'Tool")

# sort의 key를 lambda로 정의한 예시
print('미정렬:', repr(tools))
tools.sort(key=lambda x: x.name)
print('\n정렬:', tools)

# weight로 정렬하는 람다 함수를 만들어서 정렬할 수 있다
tools.sort(key=lambda x: x.weight)
print('무게순 정렬:', tools)

# 대소문자를 무시하고 정렬하는 코드
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('대소문자 구분:', places)
places.sort(key=lambda x: x.lower())
print('대소문자 무시:', places)

# 전동 공구를 weight기준으로 먼저 정렬한 뒤, name으로 정렬해보자
power_tools = [
    Tool('드릴', 4),
    Tool('원형 톱', 5),
    Tool('착암기', 40),
    Tool('연마기', 4),
]

# tuple을 쓰는 경우 (튜플은 앞에서부터 차례대로 비교한다)
saw = (5, '원형 톱')
jackhammer = (40, '착암기')
assert not (jackhammer < saw) # 예상한대로 saw가 더 작다고 나온다

# 0번째 값이 서로 같으면 1번째 값을 비교한다 -> 반복
drill = (4, '드릴')
sander = (4, '연마기')
assert drill[0] == sander[0] # 무게가 같다
assert drill[1] < sander[1] # 드릴이 더 작다(ㄱㄴㄷ순서)
assert drill < sander # 0번째 값은 같고 1번째 값이 드릴이 더 작으므로 드릴이 먼저이다

# 전동 공구 리스트를 먼저 weight로 정렬하고 그 후 name을 정렬할 수 있다
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)

# key함수의 제약사항: 모든 비교 기준의 정렬 순서가 같아야한다
power_tools.sort(key=lambda x: (x.weight, x.name),
                 reverse=True) # 모든 비교 기준을 내림차순으로 만든다
print(power_tools)

# 숫자값의 경우 -부호를 붙혀 반대방향으로 정렬할 수 있다
power_tools.sort(key=lambda x: (-x.weight, x.name),
                 reverse=True)
print(power_tools)

# name을 반전시려하면 에러가 발생한다
try:
    power_tools.sort(key=lambda x: (x.weight, -x.name),
                    reverse=True)
except TypeError:
    print("TypeError: bad operand type for unary -: 'str'")

# 리스트 타입의 sort 메서드는 key함수가 반환한 값이 서로 같은 경우 리스트에 들어있던 순서를 유지해준다
power_tools.sort(key=lambda x: x.name) # name 기준 오름차순
power_tools.sort(key=lambda x: x.weight, reverse=True) # weight 기준 내림차순
print(power_tools)

# 처음 sort를 진행하면 이름의 알파벳순으로 리스트가 정렬된다
power_tools.sort(key=lambda x: x.name)
print(power_tools)

# 두번재로 sort한 후 상태
power_tools.sort(key=lambda x: x.weight,
                 reverse=True)
print(power_tools)