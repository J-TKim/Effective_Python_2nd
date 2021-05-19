# 남은 가용 용량과 이 가용 용량의 잔존 시간을 표현하는 코드 (리키 버킷)
from datetime import datetime, timedelta

class Bucket:
    def __init__(self, peirod):
        self.period_delta = timedelta(seconds=peirod)
        self.reset_time = datetime.now()
        self.quota = 0
    
    def __repr__(self):
        return f'Bucket(quota={self.quota})'

'''
리키 버킷 알고리즘은 시간을 일정한 간격으로 구분하고,
가용 용량을 소비할 때 마다 시간을 검사해서 주기가 달라질 경우에는
이전 주기에 사용한 미사용한 가용 용량이 새로운 주기로 넘어오지 못하도록 막는다.
'''
def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

# 가용 용량을 소비하는 쪽 에서는 어떤 작업을 하고 싶을 때마다 먼저 리키 버킷으로부터 자신의 작업에 필요한 용량을 할당받아야 한다.
def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False # 새 주기가 시작됐는데 아직 버킷 할당량이 재설정되지 않았다.
    if bucket.quota - amount < 0:
        return False # 버킷의 가용 용량이 충분하지 못하다.
    else:
        bucket.quota -= amount
        return True # 버킷의 가용 용량이 충분하므로 필요한 분량을 사용한다.

# 이 클래스를 사용하려면 먼저 버킷에 사용 용량을 미리 정해진 할당량만큼 채워야 한다.
bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

# 그 후 사용할 때마다 필요한 용량을 버킷에서 빼야 한다.
if deduct(bucket, 99):
    print('99 용량 사용')
else:
    print('가용 용량이 작아서 99 용량을 처리할 수 없음')
print(bucket)

# 버킷에 들어 있는 가용 용량이 데이터 처리에 필요한 용랑보다 작아지게되면 더이상 작업을 못하게 된다.
if deduct(bucket, 3):
    print('3 용량 사용')
else:
    print('가용 용량이 작아서 3 용량을 처리할 수 없음')
print(bucket)

# False를 리턴하는 것이 두 가지 이므로 어떤 이유로 False를 리턴하는지 알 수 없는 문제가 있다.

# 이러한 문제를 해결하기 위해, 이번 주기에 재설정된 가용 용량인 max_quota와 이번 주기에 버킷에서 소비한 용량의 합계인 quota_consumed를 추적하도록 클래스를 변경할 수 있다.
class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # 새로운 주기가 되고 가용 용량을 재설정 하는 경우
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # 새로운 주기가 되고 가용 용량을 추가하는 경우
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # 어떤 주기 안에서 가용 용량을 소비하는 경우
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

bucket = NewBucket(60)
print('최초', bucket)
fill(bucket, 100)
print('보충 후 ', bucket)

if deduct(bucket, 99):
    print('99 용량 사용')
else:
    print('가용 용량이 작아서 99 용량을 처리할 수 없음')
    
if deduct(bucket, 3):
    print('99 용량 사용')
else:
    print('가용 용량이 작아서 3 용량을 처리할 수 없음')

print('여전히', bucket)