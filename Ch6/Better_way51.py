# 다음 코드는 어떤 클래스의 모든 메서드를 감싸서 메서드에 전달되는 인자, 반환 값, 발생한 예외를 모두 출력하는 코드이다.
from functools import wraps

def trace_func(func):
    if hasattr(func, 'tracing'): # 단 한 번만 데코레이터를 적용한다.
        return func
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f'{func.__name__}({args!r} {kwargs!r}) -> '
                f'{result!r}')

    wrapper.tracing = True
    return wrapper

# 다음과 같이 이 데코레이터를 새 dict 하위 클래스에 속한 여러 특별 메서드에 적용할 수 있다.
class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)

# 이 클래스의 인스턴스와 상호작용해보면 메서드가 잘 데코레이션됐는지 확인할 수 있다.
trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 발생할 것으로 예상함

# 이 코드의 문제점은 꾸미려는 모든 메서드를 @trace_func 데코레이털르 써서 재정의해야 한다는 것이다.

# 이 문제를 해결하는 방법은 메타클래스를 사용해 클래스에 속한 모든 메서드를 자동으로 감싸는 것이다.
import types

trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType
)

class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)
    
        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)
        
        return klass

class TraceDict(dict, metaclass=TraceMeta):
    pass

# 코드가 잘 작동하는 모습을 볼 수 있다.
trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 발생할 것으로 예상함#

# 상위 클래스가 메타클래스를 이미 정의한 경우, TraceMeta를 사용하면 어떤 일이 일어날까
try:
    class OtherMeta(type):
        pass
    
    class SimpleDict(dict, metaclass=OtherMeta):
        pass
    
    class TraceDict(SimpleDict, metaclass=TraceMeta):
        pass
except TypeError:
    print("TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases")

# TraceMeta를 OtherMeta가 상속하지 않았으므로 오류가 발생한다.
class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = type.__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass

class OtherMeta(TraceMeta):
    pass

class SimpleDict(dict, metaclass=OtherMeta):
    pass

class TraceDict(SimpleDict, metaclass=TraceMeta):
    pass

trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 날 것으로 예상함

# 클래스 선언 앞에 @ 기호와 데코레이터 함수를 적어 클래스 데코레이터를 사용할 수 있다.
def my_class_decorator(klass):
    klass.extra_param = '안녕'
    return klass

@my_class_decorator
class MyClass:
    pass

print(MyClass)
print(MyClass.extra_param)

# TraceMeta.__new__ 메서드의 핵심 부분을 별도의 함수로 옮겨서 어떤 클래스에 속한 모든 메서드와 함수에 trace_func를 적용하는 클래스 데코레이터를 만들 수 있다.
def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            wrapped = trace_func(value)
            setattr(klass, key, wrapped)
    return klass

# 이 데코레이터를 우리가 만든 dict의 하위 클래스에 적용하면 앞에서 메타클래스를 썼을 때와 같은 결과를 얻을 수 있다.
@trace
class TraceDict(dict):
    pass

trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 발생할 것으로 예상함

# 데코레이션을 적용할 클래스에 이미 메타클래스가 있어도 데코레이터를 사용할 수 있다.
class OtherMeta(type):
    pass

@trace
class TraceDict(dict, metaclass=OtherMeta):
    pass

trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 발생할 것으로 예상함