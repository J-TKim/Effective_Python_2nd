# 방문했던 세계 각국의 도시 이름을 저장하는 딕셔너리
visits = {
    '미국': {'뉴옥', '로스엔젤로스'},
    '일본': {'하코네'},
}

# 각 집합에 새 도시를 추가할 때 setdefault를 사용할 수 있다 (get 메서드와, 대입식을 사용하는 방식보다 코드가 짧다)
visits.setdefault('프랑스', set()).add('칸')

if (japan := visits.get('일본')) is None:
    visits['일본'] = japan = set()
japan.add('교토')

print(visits)

# 위 예제를 class로 감싸서 동적인 내부 상태에 접근할 수 있는 도우미 메서드를 제공하도록 작성
class Visits:
    def __init__(self):
        self.data = {}
    
    def add(self, country, city):
        city_set = self.data.setdefault(country, set()) 
        city_set.add(city)

# setdefault 호출의 복잡도를 완전히 감춰줌
visits = Visits()
visits.add('러시아', '예카테린부르크')
visits.add('탄자니아', '잔지바르')
print(visits.data)

# 코드를 처음 읽는 사람은 동작을 바로 이해하기 어렵고, 호출할 때 마다 키의 유무와는 상관없이 set 인스턴스를 새로 만든다는 단점이 있다

# collections 내장 모듈에 있는 defaultdict 클래스는 자동으로 키가 없을 때 디폴트 값을 저장해 간단히 처리한다
from collections import defaultdict

class Visits:
    def __init__(self):
        self.data = defaultdict(set) # 키가 없을 때 호출할 함수 제공 (set)

    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('영국', '바스')
visits.add('영국', '런던')
print(visits.data)