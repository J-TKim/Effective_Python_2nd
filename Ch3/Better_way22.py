# 위치 인자를 가변적으로 받을 수 있으면 함수 호출이 더 깔끔해지고, 시각적으로 잡음도 들어든다 (*args)

# 디버깅 정보를 로그에 남기는 함수
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('내 숫자는', [1, 2])
log('안녕', [])

# 남길 값이 없을 때에도 []를 넘겨야하므로 불편하다. 이 점을 고치기 위해 *을 변수 앞에 붙힌다.
def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('내 숫자는', 1, 2) # 언패킹 대입문에 사용한 *식과 비슷하게 작동한다.
log('안녕')

# 이미 시퀀스가 있고, 이 시퀀스를 변수로 넘기고 싶을 때 에도 *를 사용하면 된다.
favorites = [7, 33, 99]
log('좋아하는 숫자는', *favorites)


# 가번적인 위치 인자를 받는 데는 두 가지 문제점이 있다.
# 1. 이런 선택적인 위치 인자가 함수에 전달되기 전 항상 튜플로 번환된다. (제너레이터의 모든 원소를 얻기 위해 반복한다. 메모리 문제)
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)
# 그러므로 *args에 적은 인자가 들어올 것 이란느 걸 알 때만 사용하자

# 2. 함수에 새로운 위치 인자를 추가하면, 해당 함수를 호출하는 모든 코드를 변경해야한다.
def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')

log(1, '좋아하는 숫자는', 7, 33) # 문제 없음
log(1, '안녕') # 메세지만 사용

log('좋아하는 숫자는', 7, 33) # 이전 방식의 코드는 깨져서 출력됨
# *args를 받아들이는 함수를 확장할 때는 키워드 기반의 인자만 사용해야 한다.