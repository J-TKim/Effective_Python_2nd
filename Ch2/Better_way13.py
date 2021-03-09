# 기본 언패킹으로 리스트 맨 앞에서 원소를 가져왔을 때 예외 발생 예시
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
try:
    oldest, second_oldest = car_ages_descending
except ValueError:
    print("ValueError: too many values to unpack (expected 2)")

# 가장 오래된 자동차 두 대와, 나머지 자동차를 가져오는 코드 (시각적으로 잡음이 많음)
oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others)

# 인덱스나 슬라이싱 없이 같은 일을 하는 코드
odlest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

# 별표 식을 다른 위치에 사용해도 된다
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)

*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)

# 별표 식이 포함된 언패킹 대입을 처리하려면 필수인 부분이 적어도 하나는 필요
# *others = car_ages_descending
# SyntaxError: starred assignment target must be in a list or tuple

# 한 수준의 언패킹 패턴에 별표 식을 두 개 이상 쓸 수도 없다
# first, *middle, *second_middle, last = [1, 2, 3, 4]
# SyntaxError: two starred expressions in assignment

car_inventory = {
    '시내': ('그랜저', '아반떼', '티코'),
    '공항': ('제네시스 쿠페', '소나타', 'K5', '엑센트'),
}

((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()
print(f'{loc1} 최고는 {best1}, 나머지는 {len(rest1)} 종')
print(f'{loc2} 최고는 {best2}, 나머지는 {len(rest2)} 종')

# 별표 식은 항상 list 인스턴스가 된다, 언패킹하는 시퀀스에 남는 원소가 없으면 별표 부분 식은 빈 리스트가 된다
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest)

# 짧은 리스트를 언패킹하는 코드 (언패킹 할 필요가 없어보인다 차라리 리스트에 대입해 사용하자)
it = iter(range(1, 3))
first, second = it
print(f'{first} & {second}')

def generate_csv():
	yield ('Date', 'Make' , 'Model', 'Year', 'Price')
	for i in range(100):
		yield ('2019-03-25', 'Honda', 'Fit' , '2010', '$3400')
		yield ('2019-03-26', 'Ford', 'F150' , '2008', '$2400')

# 인덱스와 슬라이스를 사용해 처리 (시각적으로 잡음이 많음)
all_csv_rows = list(generate_csv())
header = all_csv_rows[0]
rows = all_csv_rows[1:]
print('CSV 헤더:', header)
print('행 수:', len(rows))

# 별표 식으로 언패킹해서 처리 (깔끔해 보인다)
it = generate_csv()
header, *rows = it
print('CSV 헤더:', header)
print('행 수:', len(rows))
