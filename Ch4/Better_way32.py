# 각 줄에 있는 문자 수를 반환하는 코드
# 파일에서 읽은 x에는 새줄 문자가 들어 있으므로 길이가 눈에 보이는 길이보다 1만큼 더 길다.
path = 'my_numbers.txt'
value = [len(x) for x in open(path)]
print(value)

# 위 문제를 해결하기 위해 제너레이터 식을 사용할 수 있다.
it = (len(x) for x in open(path))
print(it)

# 제너레이터에서 다음 값을 가져오려면 next를 사용하면 된다.
print(next(it))
print(next(it))

# 제너레이터 식은 두 제너레이터 식을 합성할 수 있다는 강력한 특징이 있다.
roots = ((x, x**0.5) for x in it)
print(next(roots))
