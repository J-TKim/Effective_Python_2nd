# 맴리듀스 구현에서 입력 데이터를 표현할 수 있는 공통 클래스가 필요한 경우
class InputData:
    def read(self):
        raise NotImplementedError

# 위 클래스를 이용해 생성한 클래스
class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()

# 입력 데이터를 소비하는 공통 방법을 제공하는 맵리듀스 작업자로 쓸 수 있는 추상 인터페이스 정의
class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

# 맵리듀스 기능을 구현한느 Worker의 하위 클래스
class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result

# 도우미 함수를 잉요해 객체를 직접 만들고 연결할 수 있다.
import os

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

# generate_inputsr를 통해 만든 InputData 인스턴스들을 사용하는 LineCountWorker 인스턴스를 만든다.
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

# Worker 인스턴스의 map단계를 여러 스레드에 공급해서 실행할 수 있다.
from threading import Thread

def excute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result

# 지금까지 만든 모든 조각을 합쳐 각 단계를 실행한다.
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return excute(workers)

import os
import random

def write_test_files(tmpdir):
    os.makedirs(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

tmpdir = 'test_inputs'
write_test_files(tmpdir)

result = mapreduce(tmpdir)
print(f'총 {result} 줄이 있습니다.')

# 클래스 메서드를 사용해 개별 객체가 아니라 클래스 전체에 적용시킬 수 있다.
class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

# 다음 코드는 입력 파일이 들어있는 디렉터리를 찾기 위해 이 config를 사용한다.
class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()
    
    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

# 비슷한 방식으로 GenericWorker 클래스 안에 create_workers 도우미 메서드를 추가할 수 있다.
class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
    
    def map(self):
        raise NotImplementedError
    
    def reduce(self, other):
        raise NotImplementedError
    
    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

# 이런 변경이 구체적인 GenericWorker 하위 클래스에 미치는 옇양은 부모 클래스를 바꾸는 것 뿐이다.
class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result

# 마짐가으로 mapreduce 함수가 create_workers를 호출하게 변경해서 mapreduce를 완전한 제네릭 함수로 만들 수 있다.
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return excute(workers)

config = {'data_dir': tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
print(f'총 {result} 줄이 있습니다.')