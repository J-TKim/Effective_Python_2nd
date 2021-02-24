# C를 따라한 %d같은 형식 지정자 사용방법
a = 0b10111011
b = 0xc5f
print('이진수 :%d, 십육진수 :%d' % (a, b))

# 잘 작동하는 예시1
key = 'my_var'
value = 1.234
formatted = '%-10s = %.2d' % (key, value)
print(formatted)

# 오류가 발생하는 문제점1 예시1
# recordered_tuple = '%-10s = %.2d' % (value, key)
# TypeError: must be real number, not str

# 오류가 발생하는 문제점2 예시2
# recordered_tuple = '%.2f = %.-10s' % (key, value)
# TypeError: must be real number, not str

# 위와같은 오류들을 피하기 위해서는 % 연산자의 순서를 계속 검사해야 한다

# 예시2
pantry = [
    ('아보카도', 1.25),
    ('바나나', 2.5),
    ('체리', 15),
]
for i, (item, count) in enumerate(pantry):
    print('#%d: %-10s = %.2f' % (i, item, count))

# 아래와 같이 사용하게 되면 가독성이 더욱 나빠진다
for i, (item, count) in enumerate(pantry):
    print('#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count)))

# 같은 값을 여러번 반복해서 사용하기 위해서는 튜플에서 여러 번 반복해야한다
template = '%s는 음식을 좋아해. %s가 요리하는 모습을 봐요.'
name = '철수'
formatted = template % (name, name)
print(formatted)

# 형식화할 값을 바꿔주어야 할 때 매우 번거롭다
name = '영희'
formatted = template % (name.title(), name.title())
print(formatted)

# 이러한 문제를 해결하기 위해 %연산자에서 딕셔너리 기능이 추가되었다
key = 'my_var'
value = 1.234

old_way = '%-10s = %.2f' % (key, value)

new_way = '%(key)-10s = %(value).2f' % {'key': key, 'value': value} # 원래 방식

reordered = '%(key)-10s = %(value).2f' % {'value':value, 'key':key} # 바꾼 방식

assert old_way == new_way == reordered

# 딕셔너리를 사용하게되면 같은 키를 여러번 입력하지 않아도 됨
name = '철수'
template = '%s는 음식을 좋아해. %s가 요리하는 모습을 봐요.'
before = template % (name, name) # 튜플

template = '%(name)s는 음식을 좋아해. %(name)s가 요리하는 모습을 봐요.'
after = template % {'name': name} # 딕셔너리

assert before == after

# 딕셔너리 사용할 시 생기는 문제점 (형식화 식이 길어짐)
for i, (item, count) in enumerate(pantry):
    before = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))

    after = '#%(loop)d: %(item)-10s = %(count)d' % {
        'loop': i + 1,
        'item': item.title(),
        'count': round(count),
    }

    assert before == after

soup = 'lentil'
formatted = 'Today\'s soup is %(soup)s.' % {'soup': soup}
print(formatted)

# 형식화 식이 길어지는 것을 방지하기 위해서 아래와 같은 방법을 이용
menu = {
    'soup': 'lentil',
    'oyster': 'tongyoung',
    'special': 'schnitzel',
}
template = ('Today\'s soup is %(soup)s, '
            'buy one get two %(oyster)s oysters, '
            'and out special entree is %(special)s.')
formatted = template % menu
print(formatted)

# 내장함수 format과 str.format
a = 1234.5678
formatted = format(a, ',.2f')
print(formatted)

b = 'my 문자열'
formatted = format(b, '^20s')
print('*', formatted, '*')

# 위치지정자 {}사용
key = 'my_var'
value = 1.234

formatted = '{} = {}'.format(key, value)
print(formatted)

formatted = '{:<10} = {:.2f}'.format(key, value)
print(formatted)

# %, {}를 표시하고 싶은 경우
print('%.2f%%' % 12.5)
print('{} replaces {{}}'.format(1.23))

# 위치 지정자 중괄호에 인덱스를 넣어서 표현 가능
formatted = '{1} = {0}'.format(key, value)
print(formatted)

# 같은 위치 인덱스 여러번 사용 가능
formatted = '{0}는 음식을 좋아해 {0}가 요리하는 모습을 봐요.'.format(name)
print(formatted)

# 코드 읽기 어려워지는 점은 여전히 불편함
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))

    new_style = '#{}: {:<10s} = {}'.format(
        i + 1,
        item.title(),
        round(count))

    assert old_style == new_style

# 아래와 같은 고급옵션 사용 가능 (!r: ''붙혀서 출력)
formatted = '첫 번째 글자는 {menu[oyster][0]!r}'.format(
    menu=menu)
print(formatted)

# 같은 키 중복 문제 여전히 발생
old_template = (
    'Today\'s soup is %(soup)s, '
    'buy one get two %(oyster)s oyster '
    'and our special entree is %(special)s.'
)
old_formatted = old_template % {
    'soup': 'lentil',
    'oyster': 'tongyoung',
    'special': 'schnitzel',
}

new_template = (
    'Today\'s soup is {soup}, '
    'buy one get two {oyster} oyster '
    'and our special entree is {special}.')
new_formatted = new_template.format(
    soup='lentil',
    oyster='tongyoung',
    special='schnitzel',
)

assert old_formatted == new_formatted

# 인터폴레이션을 통한 형식 문자열 (f-문자열)
key = 'my_var'
value = 1.234

formatted = f'{key} = {value}'
print(formatted)

# 내장 미니언어 역시 사용 가능
formatted = f'{key!r:<10} = {value:.2f}'
print(formatted)

f_string = f'{key:<10} = {value:.2f}'

c_tuple = '%-10s = %.2f' % (key, value)

str_args = '{:<10} = {:.2f}'.format(key, value)

str_kw = '{key:<10} = {value:.2f}'.format(key=key, value=value)

c_dict = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}

assert c_tuple == c_dict == f_string
assert str_args == str_kw == f_string

# 여러 줄이 필요한 형식자를 한 줄로 표현 가능
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))

    new_style = '#{}: {:<10s} = {}'.format(
        i + 1,
        item.title(),
        round(count))

    f_string = f'#{i+1}: {item.title():<10} = {round(count)}'

    assert old_style == new_style == f_string

# f-문자열을 여러 열로 나눌 수 있다.
for i, (item, count) in enumerate(pantry):
    print(f'#{i+1}'
    f'{item.title():<10s} = '
    f'{round(count)}')

# 파이썬 식을 형식 지정자 옵션에 넣을 수 있다.
places = 3
number = 1.23456
print(f'내가 고른 숫자는 {number:.{places}f}')