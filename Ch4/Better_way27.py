# 리스트에 있는 모든 원소의 제곱을 계산하는 코드
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)
print(squares)

# 리스트 컴프리헨션을 이용해 더 간단하게 코드를 작성할 수 있다.
squares = [x**2 for x in a]
print(squares)

# 대부분의 경우 map 내장 함수보다 리스트 컴프리헨션이 더 명확하다.
alt = map(lambda x: x**2, a)

# 리스트 컴프리헨션을 이용해 짝수의 제곱만 계산하는 코드
even_squares = [x**2 for x in a if x%2 == 0]
print(even_squares)

# filter 내장 함수와 map을 사용한 같은 코드 (읽기가 어렵다.)
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)

# 딕셔너리와 집합에도 컴프리헨션이 있다.
even_squares_dict = {x: x**2 for x in a if x%2==0}
three_cubed_set = {x**3 for x in a if x%3==0}
print(even_squares_dict)
print(three_cubed_set)

# map, filter을 적절히 사용하면 같은 결과를 얻을 수 있지만, 가독성이 떨어지므로 피하자
alt_dict = dict(map(lambda x: (x, x**2),
                filter(lambda x: x%2 == 0, a)))
alt_set = set(map(lambda x: x**3,
                filter(lambda x: x % 3 == 0, a)))