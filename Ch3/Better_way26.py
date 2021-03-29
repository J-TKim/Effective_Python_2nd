# 파이썬은 함수에 적용할 수 있는 데코레이터를 정의하는 특별한 구문을 제공한다.

# 함수가 호출될 때 마다 인자 값과 반환 값을 출력하는 코드
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
        f'-> {result!r}')
        return result
    return wrapper

# 이 데코레이터를 함수에 적용할 때는 @ 기호를 사용한다.
@trace
def fibonacci(n):
    """n번째 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

"""
@ 기호를 사용하는 것은 이 함수에 대해 데코레이터를 호출한 후, 데코레이터가 반환한 결과를
원래 함수가 속해야 하는 영역에 원래 함수와 같은 이름으로 등록하는 것과 같다.
fibonacci = trace(fibonacci)
"""
print(fibonacci(4))

# 데코레이터가 반환하는 함수의 이름이 fibonacci가 아닌 문제점이 발생
print(fibonacci)

# help 내장 함수를 사용해도 fibonacci의 독스트링이 출력되지 않음
print(help(fibonacci))

# pickle의 경우에도 깨짐
import pickle

try:
    print(pickle.dumps(fibonacci))
except AttributeError:
    print("AttributeError: Can't pickle local object 'trace.<locals>.wrapper'")

# functools 내장 모듈에 정의된 wraps 도우미 함수를 사용하여 문제를 해결
from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
        f'-> {result!r}')
        return result

@trace
def fibonacci(n):
    """n번째 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

# 이제 help를 통해 fibonacci의 독스트링 출력 가능
print(help(fibonacci))

# pickle 객체 직렬화도 제대로 작동함
print(pickle.dumps(fibonacci))