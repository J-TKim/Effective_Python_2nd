# 예외를 무시하는 나누기 코드
def safe_division(number, divisor,
                ignore_overflow,
                ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division(1.0, 10**500, True, False)
print(result)

result = safe_division(1.0, 0, False, True)
print(result)

# 어떤 bool 변수를 True 로 설정했는지 이해하기 쉽도록 키워드 인자를 사용한다.
def safe_division_b(number, divisor,
                ignore_overflow=False,
                ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)

# 하지만 위 처럼 키워드 인자를 사용해도, 선택적인 사항 이므로 사용하지 않을 수 있다.
assert safe_division_b(1.0, 0, False, True) == float('inf')

# 키워드만 사용하는 인자를 이용해 의도를 명확히 밝힐 수 있다.
def safe_division_c(number, divisor, *,
                ignore_overflow=False,
                ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 이제 이 함수를 호출할 때, 무조건 위치 인자로 ignore 변수를 불러와야 한다.
try:
    safe_division_c(1.0, 10**500, True, False)
except TypeError:
    print("TypeError: safe_division() takes 2 positional arguments but 4 were given")

# 키워드 인자로 불러올 때는 잘 작동한다.
result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

try:
    result = safe_division_c(1.0, 0)
except ZeroDivisionError:
    pass

# 필수인자 number, divsior도 키워드로 사용할 수 있다.
assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4

# 나중에 number, divisor의 이름이 바뀐 경우에는 에러가 발생할 것 이다.
def safe_division_c(numerator, denominator, *,
                ignore_overflow=False,
                ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

try:
    safe_division_c(number=2, divisor=5)
except TypeError:
    print("TypeError: safe_division_c() got an unexpected keyword argument 'number'")

# 위 문제를 해결하기 위해 위치로만 지정하는 인자를 설정할 수 있다.
def safe_division_d(numerator, denominator, /, *,
                ignore_overflow=False,
                ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

assert safe_division_d(2, 5) == 0.4

try:
    safe_division_d(numerator=2, denominator=5)
except TypeError:
    print("TypeError: safe_division_d() got some positional-only arguments passed as keyword arguments: 'numerator, denominator'")
# 위처럼 함수를 정의하면 파라미터 이름을 변경해도 안전하게 사용이 가능하다.

# /와 * 기호 사이에 들어간 파라미터는 위치, 키워드 모두 사용 가능하다.
def safe_division_e(numerator, denominator, /,
                ndigits=10, *,
                ignore_overflow=False,
                ignore_zero_division=False):
    try:
        fraction = numerator / denominator
        return round(fraction, ndigits)
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division_e(22, 7)
print(result)

result = safe_division_e(22, 7, 5)
print(result)

result = safe_division_e(22, 7, ndigits=2)
print(result)