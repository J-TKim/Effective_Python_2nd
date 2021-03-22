# 두 값을 반환하는 것 처럼 보이는 함수
def get_stats(numbers):
    minimum = min(numbers)
    maximun = max(numbers)
    return minimum, maximun

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

minimum, maximun = get_stats(lengths)

print(f'최소: {minimum}, 최대: {maximun}')
# 이 코드는 원소가 두 개인 튜플에 여러 값을 넣어서 함께 반환하는 식으로 작동한다.

# 아래의 예시를 보자
first, second = 1, 2
assert first == 1
assert second == 2

def my_function():
    return 1, 2

first, second = my_function()
assert first == 1
assert second == 2

# 여러 값을 한번에 처리하는 별표 식을 사용해 여러 값을 반환받을 수 도 있다.
def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled

longest, *middle, shortest = get_avg_ratio(lengths)

print(f'최대 길이: {longest:>4.0%}')
print(f'최소 길이: {shortest:>4.0%}')

# 평균, 중앙값, 개채군의 개체 수 까지 요구하는 경우 호출하는 쪽에서 반환된 튜플값을 언패킹하도록 한다.
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]
    
    return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats(lengths)

print(f'최소 길이: {minimum}, 최대 길이: {maximum}')
print(f'평균: {average}, 중앙값: {median}, 개수: {count}')

# 반환값의 순서를 혼동하기 쉽다

# 올바르게 사용한 경우
minimum, maximum, average, median, count = get_stats(lengths)

# 중앙값과 평균값을 서로 바꿔 쓴 경우
minimum, maximum, median, average, count = get_stats(lengths)

# 함수를 호출하는 부분과 반환 값을 언패킹하는 부분이 길고, 여러가지 방법으로 줄을 바꿀 수 있어 가독성이 나빠진다.
minimum, maximum, average, median, count = get_stats(
    lengths)

minimum, maximum, average, median, count = \
get_stats(lengths)

(minimum, maximum, average,
 median, count) = get_stats(lengths)

(minimum, maximum, average, median, count
    ) = get_stats(lengths)

# 이런 문제를 피하기 위해서 여러 값을 반환하거나 언패킹할 때 변수를 네 개 이상 사용하면 안된다.