# 다음 코드는 어떤 타입이 실제로 구성되기 전에 클래스 정보를 살펴보고 변경하는 모습을 보여준다.
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print(f'* 실행: {name}의 메타 {meta}.__new__')
        print('기반 클래스들:', bases)
        print(class_dict)
        return type.__new__(meta, name, bases, class_dict)

class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

class MySubclass(MyClass):
    other = 567

    def bar(self):
        pass

# 연관된 클래스가 정의되기 전에 이 클래스의 모든 파라미터를 검증하려면 Meta.__new__에 기능을 추가해야 한다.
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Polygon의 하위 클래스만 검증한다.
        if bases:
            if class_dict['sides'] < 3:
                raise ValueError('다각형 변은 3개 이상이어야 함')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None # 하위 클래스는 이 애트리뷰트에 값을 지정해야 한다.

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

class Rectangle(Polygon):
    sides = 4

class Nonagon(Polygon):
    sides = 9

assert Triangle.interior_angles() == 180
assert Rectangle.interior_angles() == 360
assert Nonagon.interior_angles() == 1260

# 이 검증은 변 개수가 3보다 작은 경우에 해당 class 정의문의 본문이 실행된 직후 예외를 발생시킨다.
try:
    print('class 이전')

    class Line(Polygon):
        print('sides 이전')
        sides = 2
        print('sides 이후')

    print('class 이후')
except ValueError:
    print("ValueError: 다각형 변은 3개 이상이어야 함")

# __init_subclass__를 이용해 더 간단하게 구현이 가능하다.
class BetterPolygon:
    sides = None # 하위 클래스에서 이 애트리뷰트의 값을 지정해야 함

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError('다각형 변은 3개 이상이어야 함')
    
    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Hexagon(BetterPolygon):
    sides = 6

assert Hexagon.interior_angles() == 720
# BetterPolygon의 하위 클래스를 잘못 정의하면 앞의 예제와 똑같은 예외를 볼 수 있다.
try:
    print('class 이전')

    class Point(BetterPolygon):
        sides = 1

    print('class 이후')
except ValueError:
    print("ValueError: 다각형 변은 3개 이상이어야 함")

# 다음 코드는 어떤 영역에 칠할 색을 검증하기 위한 메타클래스다.
class ValidataFilled(type):
    def __new__(meta, name, bases, class_dict):
        # Filled 클래스의 하위 클래스만 검증한다.
        if bases:
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('지원하지 않는 color 값')
        return type.__new__(meta, name, bases, class_dict)

class Filled(metaclass=ValidataFilled):
    color = None # 하위 클래스에서 이 애트리뷰트의 값을 지정해야 한다.

# Polygon 메타클래스와, Filled 메타클래스를 함께 사용하려고 시도하면, 오류가 발생한다.
try:
    class RedPentagon(Filled, Polygon):
        color = 'red'
        sides = 5
except TypeError:
    print("TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases")

# 검증을 여러 단계로 만들기 위해 복잡한 메타클래스 type 정의를 복잡한 계층으로 설계함으로써 이런 문제를 해결할 수도 있다.
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # 루트 클래스가 아닌 경우에만 작동한다.
        if not class_dict.get('is_root'):
            if class_dict['sides'] < 3:
                raise ValueError('다각형 변은 3개 이상이어야 함')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    is_root = True
    sides = None # 하위 클래스에서 이 애트리뷰트 값을 지정해야 한다.

class ValidateFilledPolygon(ValidatePolygon):
    def __new__(meta, name, bases, class_dict):
        # 루트 클래스가 아닌 경우만 검증한다.
        if not class_dict.get('is_root'):
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('Fill color must be supported')
        return super().__new__(meta, name, bases, class_dict)

class FilledPolygon(Polygon, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None # 하위 클래스에서 이 애트리뷰트 값을 지정해야 한다.

# 이렇게 정의하면 모든 FiledPolygon은 Polygon의 인스턴스가 된다.
class GreenPentagon(FilledPolygon):
    color = 'green'
    sides = 5

greenie = GreenPentagon()
assert isinstance(greenie, Polygon)

# 색을 검증하면 잘 작동한다.
try:
    class OrangePentagon(FilledPolygon):
        color = 'orange'
        sides = 5
except ValueError:
    print("ValueError: Fill color must be supported")

# 변의 개수 검증도 잘 작동한다.
try:
    class RedLine(FilledPolygon):
        color = 'red'
        sides = 2
except ValueError:
    print("ValueError: 다각형 변은 3개 이상이어야 함")

# ValidateFilledPolygon에 있는 색 검증을 다른 클래스 계층 구조에 적용하려면 모든 로직을 중복 정의해야 하므로, 코드 재사용이 줄고 불필요한 준비 코드는 늘어난다.

# __init_subclass__ 특별 클래스 매서드를 사용하면 이 문제도 해결할 수 있다.
class Filled:
    color = None # 하위 클래스에서 이 애트리뷰트 값을 지정해야 한다.

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError('지원하지 않는 color 값')

# 새로운 클래스에서 BetterPolygon과 Filled 클래스를 모두 상속할 수 있다.
class RedTriangle(Filled, Polygon):
    color = 'red'
    sides = 3

ruddy = RedTriangle()
assert isinstance(ruddy, Filled)
assert isinstance(ruddy, Polygon)

# 변의 수를 잘못 지정하면 검증 오류가 발생한다.
try:
    print('class 이전')

    class BlueLine(Filled, Polygon):
        color = 'blue'
        sides = 2

    print('class 이후')
except ValueError:
    print("ValueError: 다각형 변은 3개 이상이어야 함")

# 색을 잘못 지정해도 검증 오류가 발생한다.
try:
    print('class 이전')

    class BeigeSquare(Filled, Polygon):
        color = 'beige'
        sides = 4

    print('class 이후')
except ValueError:
    print("ValueError: 지원하지 않는 color 값")

# 다이아몬드 상속같은 복잡한 구조에도 __init_subclass__를 사용할 수 있다.
class Top:
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 TOP')

class Left(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 Left')

class Right(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 Right')

class Bottom(Left, Right):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 Bottom')
