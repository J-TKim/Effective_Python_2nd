# 다른 언어를 사용하다 파이썬을 접한 프로그래머들은 클래스에 게터나 세터 메서드를 명시적으로 정의하곤 한다.
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms
    
    def get_ohms(self):
        return self._ohms
    
    def set_ohms(self, ohms):
        self._ohms = ohms

# 세터와 게터를 사용하기는 쉽지만, 파이썬다운 코드가 아니다.
r0 = OldResistor(50e3)
print('이전:', r0.get_ohms())
r0.set_ohms(10e3)
print('이후:', r0.get_ohms())

# 코드가 지저분해 지기도 쉽다.
r0.set_ohms(r0.get_ohms() - 4e3)
assert r0.get_ohms() == 6e3

# 파이썬에서는 세터나 게터 메서드를 구현하지 말고 단순한 공개 애트리뷰트부터 구현을 시작하자.
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3

# 이렇게 애트리뷰트를 사용하면 연산이 저 자연스럽고 명확해진다.
r1.ohms += 5e3

# 특별한 기능을 수행해야 하는 경우 애트리뷰트를 @property 데코레이터와 대응하는 setter 애트리뷰트로 옮겨갈 수 있다.
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0
    
    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

# voltage 프로퍼티에 대입하면 vltage 세터 메서트가 호출되고, 이 메서드는 객체의 current 애트리뷰트를 변경된 전압 값에 맞춰 갱신한다.
r2 = VoltageResistance(1e3)
print(f'이전: {r2.current:.2f} 암페어')
r2.voltage = 10
print(f'이후: {r2.current:.2f} 암페어')

# 프로퍼티에 대해 setter를 지정하면 타입을 검사하거나 클래스 프로퍼티에 전달된 값에 대한 검증을 수행할 수 있다.
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'저항 > 0이어야 합니다. 실제 값: {ohms}')
        self._ohms = ohms

# 이제 잘못된 저항값을 대입하면 예외가 발생한다.
r3 = BoundedResistance(1e3)
try:
    r3.ohms = 0
except ValueError:
    print("ValueError: 저항 > 0이어야 합니다. 실제 값: 0")

# 생성자에 잘못된 값을 넘기는 경우에도 예외가 발생한다.
try:
    BoundedResistance(-5)
except ValueError:
    print("ValueError: 저항 > 0이어야 합니다. 실제 값: -5")

# @property를 사용햇 부모 클래스에 정의된 애트리뷰트를 불변으로 만들 수 도 있다.
class FixedResitance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
    
    @property
    def ohms(self):
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError('Ohms는 불변 객체입니다')
        self._ohms = ohms

# 이 객체를 만든 다음, 프로퍼티에 값을 대입하면 예외가 발생한다.
r4 = FixedResitance(1e3)
try:
    r4.ohms = 2e3
except AttributeError:
    print("AttributeError: Ohms는 불변 객체입니다")

# @property 메서드를 사용해 세터와 게터를 구현할 때는 게터나 세터 구현이 예기치 않은 동작을 수행하지 않도록 만들어야 한다.
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms

# 게터 프로퍼티 메서드에서 다른 애트리뷰트를 설정하면 코드가 아주 이상하게 작동할 수 있다.
r7 = MysteriousResistor(10)
r7.current = 0.01
print(f'이전: {r7.voltage:.2f}')
r7.ohms
print(f'이후: {r7.voltage:.2f}')