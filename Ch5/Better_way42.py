# 파이썬의 클래스 애트리뷰트에 대한 가시성은 공개와 비공개가 있다.
class MyObject:
    def __init__(self):
        self.public_field = 5 # 공개
        self.__private_field = 10 # 비공개

    def get_private_filed(self):
        return self.__private_field

foo = MyObject()
assert foo.public_field == 5

assert foo.get_private_filed() == 10
# 클래스 외부에서 점 연산자를 이용해 foo.__private_field에 접근하면 에러가 발생한다.

# 클래스 메서드 내부에서는 비공개 필드에 접근이 가능하다.
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71

# 하위 클래스에서는 부모 클래스의 비공개 필드에 접근할 수 없다.
class MyParentObject:
    def __init__(self):
        self.__private_field = 71

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field # 에러 발생

baz = MyChildObject()
try:
    baz.get_private_filed()
except AttributeError:
    print("AttributeError: 'MyChildObject' object has no attribute '_MyChildObject__private_field'")

# _MyParentObject__private_field == 71
# assert baz._MyParentObject__private_field == 71

# 객체 애트리뷰트 딕셔너리를 살펴보면 실제로 변환된 비공개 애트리뷰트 이름이 들어있다.
print(baz.__dict__)

# 하위 클래스나 클래스 외부에서 사용하면 안되는 API를 표현하기 위해 비공개 필드를 사용한다.
class MyStringClass:
    def __init__(self, value):
        self.__value = value
    
    def get_value(self):
        return str(self.__value)

foo = MyStringClass(5)
assert foo.get_value() == '5'

# 위처럼 만들면 클래스가 깨질 수 도 있고, 비공개 필드에 접근도 가능하다.
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass('5')
assert foo.get_value() == 5

# 하지만 클래스 정의를 변경하면 더 이상 비공개 애트리뷰트에 대한 참조가 바르지 않으므로 하위 클래스가 깨질 것 이다.
class MyBaseClass:
    def __init__(self, value):
        self.__value = value
    
    def get_value(self):
        return self.__value

class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value()) # 변경됨

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStingClass__value) # 변경되지 않음

# MyBaseClass에서 __value 애트리뷰트를 할당하기 때문에 self._MyStringClass__value가 깨진다.
foo = MyIntegerSubclass(5)
try:
    foo.get_value()
except AttributeError:
    print("AttributeError: 'MyIntegerSubclass' object has no attribute '_MyStingClass__value'")

# 강제로 접근을 막지 말고, 애트리뷰트 사용 법을 적어두자
class MyStringClass:
    def __init__(self, value):
        # 여기서 객체에게 사용자가 제공한 값을 저장한다.
        # 사용자가 제공하는 값은 문자열로 타입 변환이 가능해야 하며
        # 일단 한번 객체 내부에 설정되고 나면
        # 불변 값으로 취급돼야 한다.
        self._value = value

    def get_value(self):
        return str(self.__value)

# 하위 클래스의 필드와 이름이 충돌할 수 있는 경우엔느 비공개 애트리뷰트를 고려해보자.
class Apiclass:
    def __init__(self):
        self._value = 5
    
    def get(self):
        return self._value

class Child(Apiclass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # 충돌

a = Child()
print(f'{a.get()} 와 {a._value} 는 달라야 합니다.')

# 위처럼 이름이 흔한 경우 (value) 겹치는 일을 방지하기 위해서 비공개 애트리뷰트를 사용할 수 있다.
class ApiClass:
    def __init__(self):
        self.__value = 5 # 던더바

    def get(self):
        return self.__value # 던더바

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # OK!

a = Child()
print(f'{a.get()} 와 {a._value} 는 달라야 합니다.')