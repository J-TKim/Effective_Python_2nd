# 파이썬 3.7 버전 이후로는 dict를 출력하면 사용자가 지정한 순서가 보존해서 출력됨
baby_names = {
    'cat': 'kitten',
    'dog': 'puppy'
}
print(baby_names)

# 순서가 정해져있는 모습
print(list(baby_names.keys()))
print(list(baby_names.values()))
print(list(baby_names.items()))
print(baby_names.popitem()) # 마지막에 삽입된 원소

# 키워드 인자 (**kwargs)의 순서도 변하지 않음
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

my_func(goose='gosling', kangaroo='joey')

# 인스턴트 틱셔너리에 dict타입을 사용하는 클래스의 모습(인스턴트 필드 대입 순서 보존)
class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'

a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')

# 각 동물의 득표수를 저장한 딕셔너리
votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

# 득표 데이터를 처리하고 각 동물의 이름과 순위를 빈 딕셔너리에 저장하는 함수
def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

# 어떤 동물이 우승했는지 보여주는 함수 (populate_rank가 등수를 오름차순으로 등록한다고 가정)
def get_winner(ranks):
    return next(iter(ranks))

# 결과 표시 확인
ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)

# 결과를 보여줄 때 알파벳순으로 표시(collections.abc 모듈을 사용해 알파벳 순서대로 iteration하는 클래스를 새로 정의)
from collections.abc import MutableMapping

class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)

votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

# 표준 딕셔너리의 프로토클을 지키며 만들었으므로, dict위치에 SortedDict를 사용해도 에러가 발생하지 않음
sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner) # fox (우리가 원하는 결과가 아니다)
# get_winner의 구현이 populate_ranks의 삽입 순서에 맞게 딕셔너리를 이터레이션 하기 때문에 다른 결과가 나온다

# 문제를 해결하기 위해 get_winner 함수를 구현
def get_winner(ranks):
    for name, rank in ranks.items():
        if rank == 1:
            return name

winner = get_winner(sorted_ranks)
print(winner)

# ranks의 타입이 우리가 원하는 타입인지 검사하는 코드를 추가
def get_winner(ranks):
    if not isinstance(ranks, dict):
        print("TypeError('dict 인스턴트가 필요합니다')")
        return
    return next(iter(ranks))

get_winner(sorted_ranks)