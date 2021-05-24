# 센서 네트워크에서 광센서를 통해 빛이 들어온 경우를 샘플링하는 코드
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset

# 각 작업자 스레드는 센서 값을 측정한 다음에 카운터를 최댓값 까지 증가시킬 수 있다.
def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)

# 다음 코드는 병렬로 센서마다 하나씩 worker 스레드를 실행하고, 모든 스레드가 값을 다 읽을 때 까지 기다린다.
from threading import Thread

how_many = 10**5
counter = Counter()

threads = []
for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'카우터 값은 {expected}여야 하는데, 실제로는 {found} 입니다.')

# Counter 객체의 increments 메서드를 작업자 스레드 입장에서 보면 아래와 같다.
counter.count += 1

# 하지만 객체 애트리뷰트에 대한 += 연산자는 실제로는 세가지 연산으로 이뤄진다. 위 문장은 다음과 같다.
value = getattr(counter, 'count')
result = value + 1
setattr(counter, 'count', result)

# 카운터를 증가시키는 파이썬 스레드는 세 연산 사이에서 일시 중단될 수 있다.
# 스레드 A에서 실행
value_a = getattr(counter, 'count')
# 스레드 B에서 실행
value_b = getattr(counter, 'count')
result_b = value_b + 1
setattr(counter, 'count', result_b)
# 다시 스레드 A로 컨테스트 전환
result_a = value_a + 1
setattr(counter, 'count', result_a)

# 위처럼 순서가 꼬이는 일을 막기 위해 threading 내장 모듈을 사용할 수 있다.
from threading import Lock

class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0
    
    def increment(self, offset):
        with self.lock:
            self.count += offset

counter = LockingCounter()

threads = []
for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'카우터 값은 {expected}여야 하는데, 실제로는 {found} 입니다.')
