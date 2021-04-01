# 2차원 행렬을 1차원 행렬로 단순화하는 코드
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)

# 2차원 행렬의 shape 그대로 제곱하여 나타내는 코드
squared = [[x**2 for x in row] for row in matrix]
print(squared)

# 리스트 컴프리헨션 안에 다른 루프가 들어있게되면, 코드가 길어져 줄을 나누어 작성해야 한다.
my_lsts = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [10, 11, 12]],
]
flat = [x for sublist1 in my_lsts
        for sublist2 in sublist1
        for x in sublist2]

# 오히려 일반 루프문을 이용한 코드가 더 명확해 보인다.
flat = []
for sublist1 in my_lsts:
    for sublist2 in sublist1:
        flat.extend(sublist2)

# 리스트에서 4보다 큰 짝수만 남기는 두 방법의 리스트 컴프리헨션
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 ==0]
c = [x for x in a if x > 4 and x % 2 == 0]
assert b == c

# 합계가 10보다 큰 행의 3의 배수만 남기는 코드 (읽기가 매우 힘들다)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x%3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)

"""
컴프리헨션으로 3개 이상의 반복은 가능하면 피하는 것이 좋다.
"""