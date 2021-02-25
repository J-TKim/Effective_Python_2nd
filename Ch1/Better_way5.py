# 문자열을 구문분석 하기
from urllib.parse import parse_qs

my_values = parse_qs('빨강=5&파랑=0&초록=',
                    keep_blank_values=True)

print(repr(my_values))

# 딕셔너리에 get메서드를 사용하면 상황에 따라 다른 값이 반환
print('빨강:', my_values.get('빨강'))
print('초록:', my_values.get('초록'))
print('투명도:', my_values.get('투명도'))

# 질의 문자열이 '빨강=5&파랑=0&chfhr='인 경우
red = my_values.get('빨강', [''])[0] or 0
green = my_values.get('초록', [''])[0] or 0
opacity = my_values.get('투명도', [''])[0] or 0

print(f'빨강: {red!r}')
print(f'초록: {green!r}')
print(f'투명도: {opacity!r}')

# 위 식을 정수로 변환하기 위해서는 아래와 같이 이용
red = int(my_values.get('빨강', [''])[0] or 0)

# if/else 조건식을 활용하여 위와 같은 코드를 작성
red_str = my_values.get('빨강', [''])
red = int(red_str[0]) if red_str[0] else 0

# 위와 같은 코드를 여러줄로 작성한 경우
green_str = my_values.get('초록', [''])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0

# 이 로직을 반복해서 이용하기 위해서는 함수를 작성해야 한다
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

# 함수 호출을 사용해 작성하면, 훨씬 명확
green = get_first_int(my_values, '초록')