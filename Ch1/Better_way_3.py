# Type Bytes
a = b'h\x65llo'
print(list(a))  # >>> [104, 101, 108, 108, 111]
print(a)  # >>> b'hello'

a = 'a\u0300 propos'
print(list(a))  # >>> ['a', '̀', ' ', 'p', 'r', 'o', 'p', 'o', 's']
print(a)  # >>> à propos

# bytes나 str 인스턴스를 받아서 항상 str을 return


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # str 인스턴스


print(repr(to_str(b'foo')))  # >>> 'foo'
print(repr(to_str('bar')))  # >>> 'bar'
print(repr(to_str(b'\xed\x95\x9c')))  # >>> '한'    (UTF-8 에서 한글은 3바이트)

# bytes나 str 인스턴스를 받아서 항상 bytes를 return


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value


print(repr(to_bytes(b'foo')))  # >>> b'foo'
print(repr(to_bytes('bar')))  # >>> b'bar'
print(repr(to_bytes('한글')))  # >>> b'\xed\x95\x9c\xea\xb8\x80'

# + 연산자를 사용하면 bytes + bytes or str + str 이 가능
print(b'one' + b'two')  # >>> b'onetwo'
print('one' + 'two')  # >>> onetwo

# But str + bytes는 불가능
# print(b'one' + 'two')
# TypeError: can't concat str to bytes

# 이항 연산자를 사용하면 bytes끼리 or str끼리 비교 가능
assert b'red' > b'blue'
assert 'red' > 'blue'

# But str인스턴스와 bytes인스턴스는 비교 불가능
#assert 'red' > b'blue'
# TypeError: '>' not supported between instances of 'str' and 'bytes'

# But bytes인스턴스와 str인스턴스 또한 비교 불가능
#assert b'blue' < 'red'
# TypeError: '<' not supported between instances of 'bytes' and 'str'

# 내부가 같은 문자이더라도 bytes와 str을 비교할 시 에는 항상 False가 나온다
print(b'foo' == 'foo')  # >>> false

# % 연산자는 각 타입의 format string에 대해 작동한다
print(b'red %s' % b'blue')  # >>> b'red blue'
print('red %s' % 'blue')  # >>> red blue

# But str인스턴스를 bytes format string에 넘길 수 없다
# print(b'red %s' % 'blue')
# TypeError: %b requires a bytes-like object, or an object that implements __bytes__, not 'str'

# str format string에 bytes 인스턴스를 넘길 수 있다. 하지만 예상과 다르게 작동
print('red %s' % b'blue')  # >>> red b'blue'

# 이진 읽기 모드 ('wb') 가 아닌 텍스트 쓰기 모드인 ('w')로 열었기 때문에 에러가 발생
# with open('data.bin', 'w') as f:
#     f.write(b'\xf1\xf2\xf3\xf4\xf5')
# TypeError: write() argument must be str, not bytes

with open('data.bin', 'wb') as f:
    f.write(b'\xf1\xf2\xf3\xf4\xf4')

# 이진 읽기 모드 ('rb') 가 아닌 텍스트 읽기 모드인 ('r')로 열었기 때문에 에러 발생
# with open('data.bin', 'r') as f:
#     data = f.read()
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1 in position 0: invalid continuation byte
with open('data.bin', 'rb') as f:
    data = f.read()
assert data == b'\xf1\xf2\xf3\xf4\xf4'

# open함수의 encoding함수를 명시하면 플랫폼에 따라 동작이 달라지는 일을 막을 수 있다
with open('data.bin', 'r', encoding='cp1252') as f:
    data = f.read()
assert data == 'ñòóôô'
