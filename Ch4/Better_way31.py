# 텍사스 주의 여행자 수를 분석하는 코드
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# 방문자 데이터가 들어있는 리스트가 입력으로 들어오면 잘 작동한다.
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

# 이 코드의 확장성을 높이기 위해선 모든 도시에 대한 여행자 정보가 들어있는 파일에서 데이터를 읽어야 한다.
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

# normalize 함수에 read_visits가 반환된 값을 전달하면 아무것도 나오지 않음
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages) # []

# 이터레이터가 결과를 한 번만 만들어내기 때문에 그렇다.
it = read_visits('my_numbers.txt')
print(list(it))
print(list(it))

# 위 문제를 해결하기 위해 이터레이터의 전체 내용을 리스트에 넣어둔다.
def normalize_copy(numbers):
    numbers_copy = list(numbers) # 이터레이터 복사
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result

# read_visits 제너레이터가 반환하는 값에 대해서도 잘 작동한다.
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0

# 위 코드는 잘 작동하지만 메모리를 엄청 사용할 수 있기때문에,
# 함수가 호출될 때마다 새로 이터레이터를 반환하는 함수를 받는 방법이 더 좋을 수 있다.
def normaize_func(get_iter):
    total = sum(get_iter()) # 새 이터레이터
    result = []
    for value in get_iter(): # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result

# normalize_func를 사용할 때, 매번 제러레이터를 호출해 새 이터레이터를 생성하는 lambda 식을 사용할 수 있다.
path = 'my_numbers.txt'
percentages = normaize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0

# 이터레이터 프로토콜을 구현한 새로운 컨테이너 클래스를 사용할 수 있다.
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path
    
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

# 더 깔끔한 모양으로 코드가 작동한다.
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

# 파라미터로 받은 값이 단순한 이터레이터가 아니라도 잘 작동하는 함수
def normalize_defensive(numbers):
    if iter(numbers) is numbers: # 이터레이너 -- 나쁨
        raise TypeError("컨테이너를 제공해야 합니다")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# collections.abc 의 Iterator 클래스를 사용하는 방법도 있다.
from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator): # 이터레이터인지 확인하는 방법
        raise TypeError("컨테이너를 제공해야 합니다")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# 이 함수는 리스트와 ReadVisits에 대해 모두 제대로 작동한다.
visits = [15, 35, 80]
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

visits = ReadVisits(path)
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0

# 입력이 컨테이너가 아닌 이터레이터면 예외를 발생시킨다.
visits = [15, 35, 80]
it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    print("TypeError: 컨테이너를 제공해야 합니다")