# 생성자 파라미터를 기록하고, 이를 JSON 딕셔너리로 변환하는 방식으로 일반적인 파이썬 object를 JSON 문자열로 변환하는 코드
import json

class Serializable:
    def __init__(self, *args):
        self.args = args
    
    def serialize(self):
        return json.dumps({'args': self.args})

# 이 클래스를 사용하면 Point2D 같은 간단한 불변 데이터 구조를 쉽게 직렬화 할 수 있다.
class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

point = Point2D(5, 3)
print('객체:', point)
print('직렬화한 값:', point.serialize())

# 다음 코드에서는 Serializable을 부모 클래스로 하며, 이 부모 클래스를 활용해 데이터를 역직렬화 하는 클래스를 보여준다.
class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

# Deserializable을 사용하면 간단한 불변 객체를 쉽게 직렬화하고 역직렬화 할 수 있다.
class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

before = BetterPoint2D(5, 3)
print('이전:', before)
data = before.serialize()
print('직렬화한 값:', data)
after = BetterPoint2D.deserialize(data)
print('이후:', after)

# 객체의 클래스 이름을 직렬화해 JSON 데이터에 포함시킬 수 있다.
class BetterSerializable:
    def __init__(self, *args):
        self.args = args
    
    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })
    
    def __repr__(self):
        name = self.__class__.__name__
        args_str = ', '.join(str(x) for x in self.args)
        return f'{name}({args_str})'

# 클래스 이름을 객체 생성자로 다시 연결해주는 매핑을 유지할 수 있다.
registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

# deserialize가 항상 제대로 작동하려면 나중에 역직렬화한 모든 클래스에서 register_class를 호출해야 한다.
class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

register_class(EvenBetterPoint2D)

# 이제 임의의 JSON 문자열이 표현하는 클래스를 알지 못하더라도 해당 문자열을 역직렬화 할 수 있다.
before = EvenBetterPoint2D(5, 3)
print('이전:', before)
data = before.serialize()
print('직렬화한 값:', data)
after = deserialize(data)
print('이후:', after)

# 이 방식의 문제점은 register_calss 호출을 잊어버릴 수 있다는 것이다.
class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

# register_class 호출을 잊어버리고 클래스의 인스턴스를 역직렬화하려고 시도하면 프로그램이 깨진다.
point = Point3D(5, 9, -4)
data = point.serialize()
try:
    deserialize(data)
except KeyError:
    print("KeyError: 'Point3D'")

# 다음 코드는 메타클래스를 사용해서 클래스 본문을 처리한 직후에 새로운 타입을 등록한다.
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisterSerializable(BetterSerializable,
                            metaclass=Meta):
    pass

# 이제는 RegisterSerializable의 하위 클래스를 정의할 때 register_class가 호출되고 deserialize가 항상 제대로 작동한다
class Vector3D(RegisterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

before = Vector3D(10, -7, 3)
print('이전:', before)
data = before.serialize()
print('직렬화한 값:', data)
print('이후:', deserialize(data))

# 더 좋은 접근 방법은 __init_subclass__ 특별 클래스 메서드를 사용하는 것 이다.
class BetterRegisterSerializable(BetterSerializable):
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)

class Vector1D(BetterRegisterSerializable):
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude

before = Vector1D(6)
print('이전:', before)
data = before.serialize()
print('직렬화한 값:', data)
print('이후:', deserialize(data))