# 계산양이 많은 작업의 예로 사용할 인수찾기 알고리즘이다.
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

# 여러 수로 이뤄진 집합 내 모든 원소의 인수를 찾으려면 상당히 오래 걸린다.
import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')

# 다음 코드는 앞 코드와 똑같은 계산을 수행하는 파이썬 쓰레드 정의다.
from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


# 각 수마다 스레드를 시작해 병렬로 인수를 찾을 수 있다.
start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

# 마지막으로 모든 스레드가 끝날 때 까지 기다린다.
for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')

# 직렬 포트를 통해 원격 제어 헬리콥터에 신호를 보내는 코드
import select
import socket

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)

# 이 시스템 콜을 순차적으로 실행하면 실행에 필요한 시간이 선형으로 증기한다.
start = time.time()

for _ in range(5):
    slow_systemcall()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')

# 다음 코드에서는 slow_systemcall 함수를 여러 스레드에서 따로따로 호출한다.
start = time.time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)

def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')