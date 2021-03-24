# 파이썬에서는 함수를 호출할 때 위치에 따라 인자를 넘길 수 있다
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6

# 인자를 키워드를 사용해 넘길 수 있다. 키워드 인자를 넘기는 순서는 관계 없다. 다음은 모두 같은 코드이다.
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)

# 위치 기반 인자를 지정하려면 키워드 인자의 앞에 지정해야 한다.
# remainder(number=20, 7)
# SyntaxError: positional argument follows keyword argument

# 각 인자는 한 번만 지정해야 한다.
# remainder(20, number=7)
# TypeError: remainder() got multiple values for argument 'number'

# 딕셔너리의 내용물을 사용해 함술르 호출하고 싶다면 **를 사용할 수 있다.
my_kwargs = {
    'number': 20,
    'divisor': 7,
}
assert remainder(**my_kwargs) == 6

# **연산자를 이용해 키워드 인자와 섞어서 호출할 수 있다. (중복되는 인자가 없어야 함)
my_kwargs = {
    'divisor': 7,
}
assert remainder(number=20, **my_kwargs) == 6

# 아무 키워드 인자나 받는 함수를 만들고 싶다면 **kwargs를 사용한다.
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, 감마=4) # 한글 파라미터도 잘 작동한다.

# 키워드 인자를 사용하면 얻을 수 있는 이점이 3가지가 있다.
# 1. 키워드 인자를 사용하면 코드를 처음 보는 사람들에게 함수 호출의 의미를 명확히 알려줄 수 있다.
# 2. 키워드 인자의 경우 함수 정의에서 디폴트 값을 지정할 수 있다.

# 탱크에 흘러 들어가는 유체의 시간당 유입량을 계산하는 함수
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print(f'{flow:.3} kg/s')

# 시간 단위를 계산하기 위한 배율을 추가하면 다른 단위로 계산이 가능하다.
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period

# 위 처럼 지정하면 매번 period를 지정해야 하는 문제가 생긴다.
flow_per_second = flow_rate(weight_diff, time_diff, 1)

# 잡음을 줄이기 위해 period 인자에 디폴트 값을 지정한다.
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_houd = flow_rate(weight_diff, time_diff, period=3600)

# 3. 어떤 함수를 사용하던 기존 호출자에게는 하위 호환성을 제공하며, 함수 파라미터를 확장할 수 있다.
def flow_rate(weight_diff, time_diff,
            period=1, units_per_kg=1):
            return ((weight_diff * units_per_kg) / time_diff) * period

pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)

# period나 units_per_kg 같은 선택적인 키워드 인자를 여전히 위치 인자로 지정할 수 있다는 문제점이 있다.
pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2) # 3600과 2.2가 어떤 의미인지 알기 어렵다.