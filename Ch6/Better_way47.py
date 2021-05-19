# 파이썬에서는 __getattr__ 이라는 특별 메서드를 사용해 동적 기능을 활용할 수 있다.
# 어떤 클래스 안에 __getattr__ 메서드 정의가 있으면, 이 객체의 딕셔너리에서 찾을 수 없는 애트리뷰트에 접근할 때마다 __getattr__이 호출된다
class LazyRecord:
    def __init__(self):
        self.exists = 5
    
    def __getattr__(self, name):
        value = f'{name}을 위한 값'
        setattr(self, name, value)
        return value

# 다음 코드에서는 foo라는 존재하지 않는 애트리뷰트를 사용한다.
data = LazyRecord()
print('이전:', data.__dict__)
print('foo: ', data.foo)
print('이후:', data.__dict__)

# LazyRecord에 로그를 추가해서 __getattr__이 실제로 언제 호출되는지 살펴보자.
class LogginLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* 호출: __getattr__({name!r}), '
            f'인스턴스 딕셔너리 채워 넣음')
        result = super().__getattr__(name)
        print(f'* 반환: {result!r}')
        return result

data = LogginLazyRecord()
print('exists:', data.exists)
print('첫 번째 foo', data.foo)
print('두 번재 foo', data.foo)

# __getattribute__는 객체의 애트리뷰트에 접근할 때 마다 호출된다.
class ValidatingRecord:
    def __init__(self):
        self.exists = 5
    
    def __getattribute__(self, name):
        print(f'* 호출: __getattr__({name!r})')
        try:
            value = super().__getattribute__(name)
            print(f'* {name!r} 찾음, {name!r} 반환')
            return value
        except AttributeError:
            value = f'{name}를 위한 값'
            print(f'* {name!r}를 {value!r}로 설정')
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print('exists:', data.exists)
print('첫 번째 foo:', data.foo)
print('두 번째 foo:', data.foo)

# 존재하지 않는 프로퍼티에 동적으로 접근하는 경우에는 AttributeError 예외가 발생한다.
class MissingPropertyRecord:
    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError(f'{name} is missing')
        value = f'{name}를 위한 값'
        setattr(self, name, value)
        return value

data = MissingPropertyRecord()
assert data.foo == 'foo를 위한 값' # Test thist works
try:
    data.bad_name
except AttributeError:
    print("AttributeError: bad_name is missing")

# hasattr를 이용해 프로퍼티가 존재하는지 검사하는 기능과, getattr 내장 함수를 통해 프로퍼티 값을 꺼내오는 기능에 의존할 때도 있다.
data = LogginLazyRecord() # __getattr__을 구현
print('이전:', data.__dict__)
print('최초에 foo가 있나:', hasattr(data, 'foo'))
print('이후:', data.__dict__)
print('다음에 foo가 있냐:', hasattr(data, 'foo'))

# 위 예제에서는 __getattr__이 한번만 호출되지만 다음 예제에서는 hasattr이나 getattr이 쓰일 떄 마다 호출된다.
data = ValidatingRecord() # __getattribute__를 구현
print('최초에 foo가 있나:', hasattr(data, 'foo'))
print('다음에 foo가 있냐:', hasattr(data, 'foo'))

# __setattr__를 이용해 객체에 값이 대입된 경우 나중에 이 값을 데이터베이스에 저장을 구현할 수 있다.
class SavingRecord:
    def __setattr__(self, name, value):
        # 데이터를 데이터베이스 레코드에 저장한다.
        pass
        super().__setattr__(name, value)

# 다음 코드듣 로그를 남기는 하위 클래스로 SavingRecord를 정의한다.
class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f'* 호출: __setattr__({name!r}, {value!r})')
        super().__setattr__(name, value)

data = LoggingSavingRecord()
print('이전:', data.__dict__)
data.foo = 5
print('이후:', data.__dict__)
data.foo = 7
print('최후:', data.__dict__)

# __getattribute__와 __setattr__의 문제점은 원하든 원하지 않든 어떤 객체의 모든 애트리뷰트에 접근할 때 마다 함수가 호출된다는 것 이다.

# 어떤 객체와 관련된 딕셔너리에 키가 있을 때만 이 객체에 애트리뷰트에 접근하고 싶은 경우
class BrokenDictionaryRecord:
    def __init__(self, data):
        self._data = {}
    
    def __getattribute__(self, name):
        print(f'* 호출: __getattribute__({name!r})')
        return self._data[name]

# 아래 코드를 돌려보면 재귀를 수행하다 RecursionError가 호출되게 된다.
data = Brokedata = BrokenDictionaryRecord({'foo', 3})
# data.foo  # __getattribute__가 self._data에 접근해서 __getattribute__가 다시 호출되기 때문에 문제 발생

# 해결방법은 super().__getattribute__를 사용하는 것 이다.
class DictionaryRecord:
    def __init__(self, data):
        self._data = data
    
    def __getattribute__(self, name):
        print(f'* 호출: __getattribute__({name!r})')
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryRecord({'foo': 3})
print('foo', data.foo)
