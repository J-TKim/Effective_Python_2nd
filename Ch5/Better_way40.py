# 자식 클래스에서 부모 클래스를 초기화하기 위해서 부모 클래스의 __init__메서드를 직접 호출할 수 있다.
class MyBaseClass:
    def __init__(self, value):
        self.value = value
    
class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)

# 위처럼 다중 상속을 사용하는 경우 __init__호출 순서의 문제가 발생할 수 있다.
class TimesTwo:
    def __init__(self):
        self.value *= 2

class PlusFive:
    def __init__(self):
        self.value += 5

# 다음 클래스는 부모 클래스를 TimesTwo, PlusFive 순서로 정의하였다.
class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

# 이 클래스의 인스턴스를 만들면 부모 클래스의 순서에 따라 초기화된다.
foo = OneWay(5)
print('첫 번째 부모 클래스 순서에 따른 값은 (5 * 2) + 5 = ', foo.value)

# 다음 코드는 부모 클래스를 나열한 순서가 다른 경우
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

# 위 코드도 결과가 15로 나온다.
bar = AnotherWay(5)
print('두 번째 부모 클래스 순서에 따른 값은', bar.value)

# 다이아몬드 상속으로 인해 다른 문제가 생길 수 있다.
class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 7

class PlusNine(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 9

class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        PlusNine.__init__(self, value) # 이 부분이 실행되며 self.value가 다시 5로 초기화됨

foo = ThisWay(5)
print('(5 * 7) + 9 = 44 가 나와야 하지만 실제로는', foo.value)

# 위 문제를 해결하기 위해 super를 사용할 수 있다. super는 다이아몬드 계층의 공통 상위 클래스를 단 한번만 호출하도록 보장한다.
class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7

class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9

class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)


foo = GoodWay(5)
print('7 * (5 + 9) = 98 이 나와야 하고 실제로도', foo.value)

# 호출 순서는 이 클래스에 대한 MRO 정의를 따른다.
mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())
print(mro_str)

# super에 mro뷰를 제공할 부모 타입과, mor 뷰에 접근할 때 사용할 인스턴스를 넘길 수 있다.
class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super(ExplicitTrisect, self).__init__(value)
        self.value /= 3

# 클래스 안에서 super()을 호출하서 자동으로 __class__와 self를 파라미터로 넣어준다.
class AutomaticTrisect(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value)
        self.value /= 3

class ImplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value /= 3

# 위 세 class는 모두 같다.
assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3