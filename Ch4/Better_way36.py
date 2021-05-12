import itertools

# 여러 이터레이터 연결하기

# 여러 이터레이터를 하나의 순차적인 이터레이터로 합치고 싶을 때 chain을 사용한다.
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))

# 한 값을 계속 반복해 내놓고 싶을 때 repeat를 사용한다.
it = itertools.repeat('안녕', 3)
print(list(it))

# 어떤 이터레이터가 내놓는 원소들을 계속 반복하고 싶을 때 cycle을 사용한다.
it = itertools.cycle([1, 2])
result = [next(it) for _ in range(10)]
print(result)

# 한 이터레이터를 병렬적으로 두 번째 인자로 지정된 개수의 이터레이터로 만들고 싶을 때 tee를 사용한다.
it1, it2, it3 = itertools.tee(['하나', '둘'], 3)
print(list(it1))
print(list(it2))
print(list(it3))

# zip_longest는 여러 이터레이터중 짧은 쪽 이터레이터의 원소를 다 사용한 경우 fillvalue로 지정한 값을 채워 넣어준다.
keys = ['하나', '둘', '셋']
values = [1, 2]

normal = list(zip(keys, values))
print('zip: ', normal)
it = itertools.zip_longest(keys, values, fillvalue='없음')
longest = list(it)
print('zip_longest:', longest)

# 이터레이터에서 원소 거르기

# 이터레이터를 복사하지 않으면서 원소 인덱스를 이용해 슬라이싱하고 싶을 때 islice를 사용하라.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

first_five = itertools.islice(values, 5)
print('앞에서 다섯 개:', list(first_five))

middle_odds = itertools.islice(values, 2, 8, 2)
print('중간의 홀수들:', list(middle_odds))

# takewhile은 이터레이터에서 주어진 술어가 False를 반환하는 첫 원소가 나타날 때 까지 원소를 돌려준다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_then_seven = lambda x: x < 7
it = itertools.takewhile(less_then_seven, values)
print(list(it))

# dropwhile은 이터레이터에서 주어진 술어가 False를 반환하는 첫 번째 원소를 찾을 때 까지 이터레이터의 원소를 건너뛴다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_then_seven = lambda x: x < 7
it = itertools.dropwhile(less_then_seven, values)
print(list(it))

# filterfalse는 주어진 이터레이터에서 술어가 False를 반환하는 모든 원소를 돌려준다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0

filter_result = filter(evens, values)
print('Filter:', list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))

# 이터레이터에서 원소의 조합 만들어내기

# accumulate는 파라미터를 두개 받는 함수를 반복 적용하면서 이터레이터 원소를 값 하나로 줄여준다.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print('합계:', list(sum_reduce))

def sum_modulo_20(first, second):
    output = first + second
    return output % 20

modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('20으로 나눈 나머지의 합계:', list(modulo_reduce))

# prodict는 하나 이상의 이터레이터에 들어있는 아이템들의 데카르트 곱을 반환한다.
single = itertools.product([1, 2], repeat=2)
print('리스트 한 개:', list(single))

multiple = itertools.product([1, 2], ['a', 'b'])
print('리스트 두 개:', list(multiple))

# permutations는 이터레이터가 내놓는 원소들로부터 만들어진 길이 N인 순열을 돌려준다.
it = itertools.permutations([1, 2, 3, 4], 2)
print(list(it))

# combinations는 이터레이터가 내놓는 원소들로부터 만들어낸 길이 N인 조합을 돌려준다.
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))

# combinations_with_replacement는 combinations와 같지만 원소의 반복을 허용한다.
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))