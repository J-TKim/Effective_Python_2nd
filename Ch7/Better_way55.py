# 동시성 파이프라인을 이용해 디지털 카메라에서 이미지 스트림을 계속 가져와 이미지를 변경하고 온라인 포토 갤러리에 저장하는 코드이다.
def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item

# 가장 먼저 필요한 기능은 파이프라인의 단계마다 작업을 전달하는 방법이다.
from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()
    
    # 생산자인 디지털 카메라는 미처리 작업을 표현하는 dequq의 끝에 새로운 이미지를 추가한다.
    def put(self, item):
        with self.lock:
            self.items.append(item)

    # 파이프라인의 첫 번째 단계인 소비자는 미처리 작업을 표현하는 deque의 맨 앞에서 이미지를 제거한다.
    def get(self):
        with self.lock:
            return self.items.popleft()

# 다음 코드는 큐에서 가져온 작업에 함수를 적용하고, 그 결과를 다른 큐에 넣는 스레드를 통해 파이프라인의 각 단계를 구현한다.
# 그리고 각 작업자가 얼마나 많은이 새로운 입력을 검사했고 얼마나 많이 작업을 완료했는지 추적한다.
from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    # 큐가 비어있는 경우 IndexError 예외를 잡아내 문제를 해결한다.
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)
            except AttributeError:
                return
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

# 이제 파이프라인을 조율하기 위한 조율 지점 역할을 할 수 있도록 각 단계별로 큐를 생성하고 각 단계에 맞는 작업 스레드를 만들어 서로 연결할 수 있다.
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()

done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

# 각 단계를 처리하기 위해 세 가지 스레드를 시작하고, 파이프라인의 첫 번째 단계에서 원하는 만큼 작업을 넣는다.
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

while len(done_queue.items) < 1000:
    # 기다리는 동안 유용한 작업을 수행한다.
    time.sleep(0.1)

for thread in threads:
    thread.in_queue = None
    thread.join()

# 이 코드는 제대로 작동하지만, 스레드들이 새로운 작업을 기다리면서 큐를 폴링하기 떄문에 IndexError 예외를 잡아내는 부분이 상당히 많이 실행된다.
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f'{processed} 개의 아이템을 처리했습니다,'
    f'이때 풀링을 {polled} 번 했습니다.')

# queue를 이용해 앞에 있는 문제들을 해결할 수 있다.
from queue import Queue

my_queue = Queue()

def consumer():
    print('소비자 대기')
    my_queue.get() # 다음에 보여줄 put()이 실행된 다음에 실행된다.
    print('소비자 완료')

thread = Thread(target=consumer)
thread.start()

# 이 스레드가 먼저 실행되지만, Queue에 원소가 put되기 전까지 스레드는 끝나지 않는다.
print('생산자 데이터 추가')
my_queue.put(object()) # 앞에서 본 get()이 실행된 다음에 실행된다.
print('생산자 완료')
thread.join()

# 파이프라인 중간이 막히는 경우를 해결하기 위해 Queue 클래스에서는 두 단계 사이에 허용할 수 있는 미완성 작업의 최대 개수를 지정할 수 있다.
my_queue = Queue(1) # 버퍼 크기 1
def consumer():
    time.sleep(0.1) # 대기
    my_queue.get() # 두 번재로 실행됨
    print('소비자 1')
    my_queue.get() # 네 번째로 실행됨
    print('소비자 2')
    print('소비자 완료')

thread = Thread(target=consumer)
thread.start()

# 큐의 크기가 1이기 때문에 하나씩 처리한다.
my_queue.put(object)
print('생잔자 1')
my_queue.put(object)
print('생산자 2')
print('생산자 완료')
thread.join()

# Queue 클래스의 task_done 메서드를 통해 작업의 진행을 추적할 수 있다.
in_queue = Queue()
def consumer():
    print('소비자 대기')
    work = in_queue.get() # 두 번째로 실행됨
    print('소비자 작업 중')
    # 작업 진행
    print('소비자 완료')
    in_queue.task_done() # 세 번째로 실행됨

thread = Thread(target=consumer)
thread.start()

# in_queue가 비어 있더라도 지금까지 이 큐에 들어간 모든 원소에 대해 task_done이 호출되기 전까지는 join이 끝나지 않는다.
print('생산자 데이터 추가')
in_queue.put(object()) # 첫 번째로 실행됨
print('생산자 대기')
in_queue.join() # 네 번째로 실행됨
print('생산자 완료')
thread.join()

# 다음 코드는 큐에 더 이상 다른 입력이 없음을 표시하는 센티넬 원소를 추가하는 close 메서드를 정의한다.
class ClosableQueue(Queue):
    SENTINAL = object()

    def close(self):
        self.put(self.SENTINAL)

    # 이터레이션하다가 이 특별한 object를 찾으면 이터레이션을 끝낸다.
    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINAL:
                    return # 스레드를 종료시킨다
                yield item
            finally:
                self.task_done()

# 이제 작업자 스레드가 ClosableQueue 클래스의 동작을 활용하게 할 수 있다.
class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
    
    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

# 입력이 모두 끝났음을 표시하는 신호를 추가한다.
download_queue.close()

# 마지막으로 각 단계를 연결하는 큐를 join함으로써 작업 완료를 기다린다.
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), '개의 원소가 처리됨')

for thread in threads:
    thread.join()

# 이 접근 방법을 확장해 단계마다 여러 작업자를 사용할 수 있다.
def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()
    
    closable_queue.join()

    for thread in threads:
        thread.join()

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

download_threads = start_threads(
    3, download, download_queue, resize_queue)
resize_threads = start_threads(
    4, resize, resize_queue, upload_queue)
upload_threads = start_threads(
    5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), '개의 원소가 처리됨')