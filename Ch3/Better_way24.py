# 메세지와 시간을 함께 출력하는 코드
from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

# 함수가 정의되는 시간에 datetime.now()가 단 한 번만 호출되기 때문에 시간이 항상 같다.
log('안녕!')
sleep(0.1)
log('다시 안녕!')

# 위 문제를 해결하기 위해 when=None으로 지정한다.
def log(message, when=None):
    """메세지와 타임스탬프를 로그에 남긴다.
    
    Args:
        message: 출력할 메세지.
        when: 메세지가 발생한 시각(datetime).
            디폴트 값은 현재 시각이다.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

# 시간이 다르다.
log('안녕')
sleep(0.1)
log('다시 안녕')

# JSON 데이터 디코딩에 실패하면 디폴트로 빈 딕셔너리를 반환하는 코드
import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

# default에 지정된 딕셔너리가 decode 호출에 모두 공유된다.
foo = decode('잘못된 데이터')
foo['stuff'] = 5
bar = decode('또 잘못된 데이터')
bar['meep'] = 1
print('Foo', foo)
print('Bar', bar)

assert foo is bar

# default 인자를 None으로 지정하고 함수의 독스트링에 동작 방식을 기술하라
def decode(data, default=None):
    """문자열로부터 JSON 데이터를 읽어온다.

    Args:
        data: 디코딩 할 JSON 데이터.
        default: 디코딩 실패 시 반환할 값이다.
            디폴트 값은 빈 딕셔너리다.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default

# 원하는 대로 결과가 출력된다.
foo = decode('잘못된 데이터')
foo['stuff'] = 5
bar = decode('또 잘못된 데이터')
bar['meep'] = 1
print('Foo', foo)
print('Bar', bar)
assert foo is not bar

# 타입 애너테이션 으로도 잘 작동한다.
from typing import Optional

def log_typed(message: str,
            when: Optional[datetime]=None) -> None:
    """메세지와 타임스탬프를 로그에 남긴다.
    
    Args:
    message: 출력한 메세지.
    when: 메세지가 발생한 시각(datetime).
        디폴트 값은 현재 시각이다.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')