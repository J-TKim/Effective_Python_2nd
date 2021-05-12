# throw의 작동 방식을 보여주는 코드
class MyError(Exception):
    pass

def my_generator():
    yield 1
    yield 2
    yield 3

it = my_generator()
print(next(it)) # 1을 내놓음
print(next(it)) # 2를 내놓음
# print(it.throw(MyError('test error')))

# try except를 사용해 예욀르 잡아낸다.
def my_generator():
    yield 1

    try:
        yield 2
    except MyError:
        print('MyError 발생!')
    else:
        yield 3

    yield 4

it = my_generator()
print(next(it)) # 1을 내놓음
print(next(it)) # 2를 내놓음
print(it.throw(MyError('test error')))

# throw 메서드에 의존하는 제너레이터를 통해 타이머를 구현하는 코드
class Reset(Exception):
    pass

# Reset 예외가 발생할 때 마다 카운터가 period로 재설정된다.
def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period

# 매 초 한 번 폴링되는 외부 입력과 이 재설정 이벤트를 연결할 수 있다.
RESETS = [
    False, False, False, True, False, True, False,
    False, False, False, False, False, False, False]

def check_for_reset():
    # 외부 이벤트를 폴링한다.
    return RESETS.pop()

def announce(remaining):
    print(f'{remaining} 틱 남음')

def run():
    it = timer(4)
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)

run()

# 위 기능을 컨테이너 객체를 사용해 더 단순하게 구현할 수 있다.
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):
        while self.current:
            self.current -= 1
            yield self.current

RESETS = [
    False, False, True, False, True, False,
    False, False, False, False, False, False, False]

# run 코드가 훨씬 읽기 쉬워진다.
def run():
    timer = Timer(4)
    for current in timer:
        if check_for_reset():
            timer.reset()
        announce(current)

run()