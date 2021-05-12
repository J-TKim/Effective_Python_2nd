# 주어진 간격과 진폭에 따른 사인파 값을 생성하는 코드
import math

def wave(amplitude, steps):
    step_size = 2 * math.pi / steps # 2 라디안 / 단계 수
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output

# wave 제너리에터를 이터레이션하며 진폭이 고정된 파형 신호를 송신한다.
def transmit(output):
    if output is None:
        print(f'출력: None')
    else:
        print(f'출력: {output:>5.1f}')

def run(it):
    for output in it:
        transmit(output)

run(wave(3.0, 8))

# 제너레이터를 이터레이션 할 때 마다 진폭을 변조할 수 있는 방법이 필요하다.

# 일반적으로 제너레이터를 이터레이션 할 때 yield 식이 반환하는 값은 None이다.
def my_generator():
    received = yield 1
    print(f'받은 값 = {received}')

it = iter(my_generator())
output = next(it) # 첫 번째 제너레이터 출력을 얻는다.
print(f'출력값 = {output}')

try:
    next(it) # 종료될 때 까지 제너레이터를 실행한다.
except StopIteration:
    pass

# 위 문제를 해결하기 위해 send 메서드를 사용할 수 있다.
it = iter(my_generator())
output = it.send(None) # 첫 번째 제너레이터 출력을 얻는다.
print(f'출력값 = {output}')

try:
    it.send('안녕!') # 값을 제너레이터에 넣는다.
except StopIteration:
    pass

# 위 동작을 활용해 문제를 해결할 수 있다.
def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield # 초기 진폭을 받는다.
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output # 다음 진폭을 받는다.

def run_modulating(it):
    amplitudes = [
        None, 7, 7, 7, 2, 2, 2, 10, 10, 10, 10, 10,
    ]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)

run_modulating(wave_modulating(12))

# yield from과 같이 활용할 수 있다.
def complex_wave():
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)

run(complex_wave())

# 위 코드에 send를 적용시켜보자.
def complex_wave_modulating():
    yield from wave_modulating(3)
    yield from wave_modulating(4)
    yield from wave_modulating(5)

run_modulating(complex_wave_modulating())

# send를 쓰지 않고 wave 함수에 이터레이터를 전달하면 중간에 None이 출력되는 문제를 해결할 수 있다.
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it) # 다음 입력 받기
        output = amplitude * fraction
        yield output

def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)

def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)

run_cascading() # None이 출력되지 않는다!