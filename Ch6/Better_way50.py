# 다음 코드는 애트리뷰트와 컬럼 이름을 연결하는 디스크립터 클래스다.
class Field:
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name
    
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')
    
    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

# 로우로 표현하는 클래스를 정의하려면 애트리뷰트별로 해당 테이블 컬럼 이름을 지정하면 된다.
class Customer:
    # 클래스 애트리뷰트
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

cust = Customer()
print(f'이전: {cust.first_name!r} {cust.__dict__}')
cust.first_name = '유클리드'
print(f'이전: {cust.first_name!r} {cust.__dict__}')

# 하지만 이 클래스에는 중복이 많다.
class Customer:
    # Left side is redundant with right side
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


# 이런 경우 중복을 줄이기 위해 메타클래스를 사용할 수 있다.
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

# 다음 코드는 메타클래스를 사용하는 기반 클래스 정의다.
class DatabaseRow(metaclass=Meta):
    pass

# 메타클래스를 사용하기 위해 Field 디스크립터에서 바꿔야 할 부분은 생성자가 없단느 점 뿐 이다.
class Field:
    def __init__(self):
        # 이 두 정보를 메타클래스가 채워준다.
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')
    
    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

# 데이터베이스 로우에 대응하는 클래스 정의에는 이전과 달리 중복이 없다.
class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

# 동작은 이전 클래스와 같다.
cust = BetterCustomer()
print(f'이전: {cust.first_name!r} {cust.__dict__}')
cust.first_name = '유클리드'
print(f'이전: {cust.first_name!r} {cust.__dict__}')

# DatabaseRow를 상속하지 않으면 코드가 깨진다.
class BrokenCustomer:
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = BrokenCustomer()
try:
    cust.first_name = '메르센'
except TypeError:
    print("TypeError: attribute name must be string, not 'NoneType'")

# 이 문제를 해결하는 방법은 디스크립터에 __set_name__ 특별 메서드를 사용하는 것 이다.
class Field:
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        # 클래스가 생성될 떄 모든 스크립터에 대해 이 메서드가 출력된다.
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

# 이제 특정 기반 클래스를 상속하거나 메타클래스를 사용하지 않아도 Field 디스클비터가 제공하는 기능을 모두 활용할 수 있다.
class FixedCustomer:
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = FixedCustomer()
print(f'이전: {cust.first_name!r} {cust.__dict__}')
cust.first_name = '메르센'
print(f'이후: {cust.first_name!r} {cust.__dict__}')