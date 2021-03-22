# sns 프로필 사진을 관리하는 코드
pictures = {}
path = 'profile_1234.png'

if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'경로를 열 수 없습니다: {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

# 위와 같은 방식으로 in, KeyError가 아닌 setdefault를 사용할 수 있다.
try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'경로를 열 수 없습니다: {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()

# 위 코드는 open이 딕셔너리에 경로가 있는지 여부와 관계없이 항상 호출된다. open이 예외를 던질 수 있으므로 이 예외를 처리해야 한다.

# 내부 상태를 관리하기 위해 defaultdict를 사용할 수 있다.
from collections import defaultdict

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'경로를 열 수 없습니다: {profile_path}')
        raise

pictures = defaultdict(open_picture)
try:
    handle = pictures[path]
except TypeError:
    print("TypeError: open_picture() missing 1 required positional argument: 'profile_path'")
handle.seek(0)

# 위 코드의 문제는 defaultdict 생성자에 전달한 함수는 인자를 받을 수 없다는 데 있다.

# 위 문제들을 해결하기 위해 파이썬에서는 __missing__ 특별 메서드를 사용할 수 있다.
class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()

# path가 없으면 __missing__ 메서드가 호출되고, 디폴트 값을 딕셔너리에 넣어준 뒤, 그 값을 반환한다. 없으면 __missing__이 호출되지 않는다.