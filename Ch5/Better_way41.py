from pprint import pprint

# 자식 클래스가 사용할 메서드 몇 개만 정의하는 클래스인 믹스인을 사용할 수 있다.

# 메모리 내에 있는 객체를 직렬화에 사용할 수 있도록 딕셔너리로 바꿔보자.
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

# 다음은 위 믹스인을 사용해 이진 트리를 딕셔너리 표현으로 변경하는 예제 코드이다.
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        
tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))
orig_print = print
print = pprint
print(tree.to_dict())
print = orig_print

# 다음 코든느 BinaryTree에 대한 참조를 저장하는 BinaryTree의 하위 클래스이다.
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None,
                 right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    # BinaryTreeWithParent._traverse 메서드를 오버라이드해서 믹스인이 무한 루프를 돌지 못하게 한다.
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and
                key == 'parent'):
            return value.value  # 순환 참조 방지
        else:
            return super()._traverse(key, value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
orig_print = print
print = pprint
print(root.to_dict())
print = orig_print

# BinaryTreeWithParent._traverse를 오버라이드함에 따라 BinaryTreeWithParent를 애트리뷰트로 제공하는 모든 클래스도 자동으로 ToDictMixin을 문제없이 사용할 수 있게 된다.
class NamedSubtree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubtree('foobar', root.left.right)
orig_print = print
print = pprint
print(my_tree.to_dict())
print = orig_print

# 믹스인을 서로 합성할 수 도 있다.
import json

class JsonMixin:
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)
    
    def to_json(self):
        return json.dumps(self.to_dict())

# 위 클래스를 이용해 데이터 센터의 각 요소 간 연결을 표현하는 클래스를 생성할 수 있다.
class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
            Machine(**kwargs) for kwargs in machines
        ]

class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed

class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk

# 데이터를 직렬화한 다음에 다시 역질렬화 하는 양변환 변환이 가능한지 검사하는 코드
serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12},
        {"cores": 2, "ram": 4e9, "disk": 500e9}
    ]
}"""

deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)