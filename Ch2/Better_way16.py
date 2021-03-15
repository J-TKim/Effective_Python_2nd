# 빵에 얼마나 투표했는지 저장하는 딕셔너리
counters = {
    '폼퍼니켈': 2,
    '사워도우': 1,
}

# 키가 존재할 때 참을 반환하는 in을 사용한 코드
key = '밑'

if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1

# 같은 동작을 달성하는 다른 방법(try, except)
counters = {
    '폼퍼니켈': 2,
    '사워도우': 1,
}

try:
    count = counters[key]
except KeyError:
    count = 0

counters[key] = count + 1

# get 메서드를 사용한 예시 (가장 깔끔)
count = counters.get(key, 0)
counters[key] = count + 1

# in 식과 KeyError를 사용하는 여러 방식 (가독성이 떨어진다)
counters = {
    '폼퍼니켈': 2,
    '사워도우': 1,
}

if key not in counters:
    counters[key] = 0
counters[key] += 1


counters = {
    '폼퍼니켈': 2,
    '사워도우': 1,
}

if key in counters:
    counters[key] += 1
else:
    counters[key] = 1

counters = {
    '폼퍼니켈': 2,
    '사워도우': 1,
}
try:
    counters[key] += 1
except KeyError:
    counters[key] = 1

# 딕셔너리에 저장된 값이 더 복잡한 값일 때 (in을 사용한 경우)
votes = {
    '바게트': ['철수', '순이'],
    '치아바타': ['하니', '유리'],
}
key = '브리오슈'
who = '단이'

if key in votes:
    names = votes[key]
else:
    votes[key] = names = []

names.append(who)
print(votes)

# KeyError 예외를 사용한 경우
votes = {
    '바게트': ['철수', '순이'],
    '치아바타': ['하니', '유리'],
}
key = '브리오슈'
who = '단이'

try:
    names = votes[key]
except KeyError:
    votes[key] = names = []

names.append(who)

# get을 이용하고, 키가없을 대는 키를 한 번 읽고 대입을 한 번 사용한 경우
votes = {
    '바게트': ['철수', '순이'],
    '치아바타': ['하니', '유리'],
}
key = '브리오슈'
who = '단이'

names = votes.get(key)
if names is None:
    votes[key] = names = []

names.append(who)

# if문 안에 get을 사용하면 더 짧고 가동성이 좋아진다
votes = {
    '바게트': ['철수', '순이'],
    '치아바타': ['하니', '유리'],
}
key = '브리오슈'
who = '단이'

if (names := votes.get(key)) is None:
    votes[key] = names = []

names.append(who)

# 키가 없으면 제공받은 디폴트 값을 키에 연관시켜 딕셔너리에 대입하고 반환하는 setdefault 메서드
votes = {
    '바게트': ['철수', '순이'],
    '치아바타': ['하니', '유리'],
}
key = '브리오슈'
who = '단이'

names = votes.setdefault(key, [])
names.append(who)

# 키가 없을 때 setdefault에 전달된 디폴트 값이 별도로 복사되지 않고 딕셔너리에 직접 대입된다
data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('이전:', data)
value.append('hello')
print('이후:', data)

# 최초 예제를 setdefault로 구현한 코드      
counters = {
    '폼퍼니켈': 2,
    '사워도우': 1,
}

count = counters.setdefault(key, 0)
counters[key] = count + 1