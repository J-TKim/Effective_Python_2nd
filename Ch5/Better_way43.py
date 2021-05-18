# 멤버들의 빈도를 계산하는 메서드가 포함된 커스텀 리스트 타입이 필요한 경우
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)
    
    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts

# FrequencyList를 리스트의 하위 클래스로 만들어, 리스트가 제공하는 모든 표준 함수를 사용할 수 있고 필요한 기능 추가도 가능하다.
foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('길이:', len(foo))

foo.pop()
print('pop한 다음:', repr(foo))
print('빈도:', foo.frequency())

# 이진 트리 클래스를 시퀀스의 의미 구조를 사용해 다룰 수 있는 이진 클래스를 만드는 코드
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# 인덱스를 사용해 시퀀스에 접근하는 코드는 특별 메서드 getitem으로 해석된다.
bar = [1, 2, 3]
assert bar[0] == bar.__getitem__(0)

# BinaryNode 클래스가 시퀀스처럼 작동하게 하려면 트리 노드를 깊이 우선 순회하는 커스텀 getitem 메서드 구현을 제공하면 된다.
class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()
    
    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'인덱스 범위 초과: {index}')

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7))),
    right=IndexableNode(
        15,
        left=IndexableNode(11)))

# 이 트리를 left나 right 애트리뷰트를 사용해 순회할 수 도 있지만, 추가로 리스트처럼 접근할 수 도 있다.
print('LRR:', tree.left.right.right.value)
print('인덱스 0:', tree[0])
print('인덱스 1:', tree[1])
print('11이 트리 안에 있나?', 11 in tree)
print('17이 트리 안에 있니?', 17 in tree)
print('트리:', list(tree))

# 아직 리스트 인스턴스에서 기대할 수 있는 모든 시퀀스의 의미 구조를 제공할 수는 없다.
try:
    len(tree)
except TypeError:
    print("TypeError: object of type 'IndexableNode' has no len()")

# len 내장함수는 __len__을 구현해야 한다.
class SequenceNode(IndexableNode):
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count

tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6,
            right=SequenceNode(7))),
    right=SequenceNode(
        15,
        left=SequenceNode(11))
)

print('트리 길이:', len(tree))

# collections.abc 모듈이 필요한 메서드 구현을 잊어버린 경우 실수한 부분을 알려준다.
from collections.abc import Sequence

class BadType(Sequence):
    pass

try:
    foo = BadType()
except TypeError:
    print("TypeError: Can't instantiate abstract class BadType with abstract methods __getitem__, __len__")

class BetterNode(SequenceNode, Sequence):
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6,
            right=BetterNode(7))),
    right = BetterNode(
        15,
        left=BetterNode(11)))

print('7의 인덱스:', tree.index(7))
print('10의 개수:', tree.count(10))