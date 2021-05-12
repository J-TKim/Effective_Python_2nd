# 애니메이션의 각 부분에서 필요한 화면상 이동 변위를 만들어낼 때 사용할 두 가지 제너레이터
def move(period, speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0

# 최종 애니메이션을 만들기 위해 위 함수를 합친 함수
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta

# 화면에서 이미지를 이동시키기 위한 코드
def render(delta):
    print(f'Delta: {delta:.1f}')

def run(func):
    for delta in func():
        render(delta)
    print()

run(animate)
# 위 코드들은 for문과 yield식이 반복되면서 잡음이 늘고 가독성이 줄어든다.
# 위 문제를 해결하기 위해 yield from 식을 사용한다.

def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)
    print()

run(animate)

# 더 명확하고 직관적인것 뿐 만 아니라, for문보다 성능도 더 좋아진다.

# timeit 내장 모듈을 통해 성능이 개선되는지 확인한다.
import timeit

def child():
    for i in range(1_000_000):
        yield i

def slow():
    for i in child():
        yield i

def fast():
    yield from child()

baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50
)
print(f'수동 내포: {baseline:.2f}s') # 5.36s

comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50
)
print(f'합성 사용: {comparison:.2f}s') # 4.38%

reduction = -(comparison - baseline) / baseline
print(f'{reduction:.1%} 시간이 적게 듦') # 18.2%