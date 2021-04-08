# 문자열에서 찾은 단어의 인덱스를 반환하느 코드
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == " ":
            result.append(index + 1)
    return result

address = "컴퓨터(영어: Computer, 문화어: 콤퓨터, 순화어: 전산기)는 진공관"
result = index_words(address)
print(result[:10])

# 가독성 부분을 개선하기 위해 제너레이터와, yield를 사용한다.
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == " ":
            yield index + 1

# next()를 사용해 앞에있는 값 부터 받아올 수 있다.
it = index_words_iter(address)
print(next(it))
print(next(it))

# list()로 감싸면 리스트로 변환할 수 있다.
result = list(index_words_iter(address))
print(result[:10])

# index_words는 반환하기 전에 모든 결과를 리스트에 저장해야 하기 때문에 메모리를 많이 사용한다.
# 같은 함수를 제너레이터 버전으로 만들면 메모리 크기를 제한할 수 있다.
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == " ":
                yield offset

import itertools

it = index_file(address)
results = itertools.islice(it, 0, 10)
print(list(results))