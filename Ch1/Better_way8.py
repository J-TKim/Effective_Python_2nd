# 리스트 컴프리헨션을 사용하면 소스 리스트에서 새로운 리스트를 파생시키기 쉽다
names = ['Cecilia', '남궁민수', '파이썬']
counts = [len(n) for n in names]
print(counts)

# 두 리스트는 인덱스가 같음
longest_name = None
max_count = 0

for i in range(len(names)):
    count = counts[i]
    if count > max_count:
        longest_name = names[i]
        max_count = count

print(longest_name)

# enumerate를 사용한 위를 짧게 만든 코드
for i, name in enumerate(names):
    count = counts[i]
    if count > max_count:
        longest_name = name
        max_count = count

# 위 코드를 더 깔끔하게 만들기 위해서 zip함수 사용
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count

# zip은 자신이 감싼 이터레이터 중 어느 하나가 끝날 때 까지 튜플을 반환한다 ('Rosalind')의 출력은 없음
names.append('Rosalind')
for name, count in zip(names, counts):
    print(name)

# 긴 이터레이터의 뒷부분을 사용하고 싶다면, itertools.zip_longest 사용
import itertools

for name, count in itertools.zip_longest(names, counts):
    print(f'{name}: {count}')