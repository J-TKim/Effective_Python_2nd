# 0으로 수를 나누려는 경우 None을 반환하는 함수
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

# 이함수를 사용하는 코드는 반환 값을 적절히 해석하면 된다.
x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print('잘못된 입력')

# 피제수가 0인 경우 0이 return되어 잘못된 코드가 실행된다.
x, y = 0, 5
result = careful_divide(x, y)
if not result:
    print('잘못된 입력')

# 위와 같은 실수를 줄이기 위한 방안들

# 방안1, 반환 값을 2튜플로 분리
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None # 첫 번째 부분은 연산이 성공인지 실패인지를 표시, 두 번째 부분은 계산에 성공한 경우 실제 결괏값을 저장

success, result = careful_divide(x, y)
if not success:
    print('잘못된 입력')

# 아래와 같이 실수할 경우가 있음
_, result = careful_divide(x, y)
if not success:
    print('잘못된 입력')

# 방안2, 결코 None을 반환하지 않는다.
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('잘못된 입력')

# 방안2를 사용하면 반환 값에 대한 조건문을 사용하지 않아도 된다. 반환된 값을 else에서 이용하자
x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print('잘못된 입력')
else:
    print(f'결과는 {result:.1f} 입니다.')

# 타입 애너테이션을 사용하는 코드에 적용해보기
def careful_divide(a: float, b: float) -> float:
    """a를 b로 나눈다.

    Raises:
        ValueError: b가 0이어서 나눗셈을 할 수 없을 때
    """
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('잘못된 입력')