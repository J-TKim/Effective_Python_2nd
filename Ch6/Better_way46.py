# 학생의 숙제 점수가 백분율 값인지 검증하는 코드
class Homework:
    def __init__(self):
        self._grade = 0
    
    @property
    def grade(self):
        return self._grade
    
    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다'
            )
        self._grade = value

# @property를 사용하면 이 클래스를 쉽게 사용할 수 있다.

galileo = Homework()
galileo.grade = 95

# 이제 이 학생에게 여러 시험과목의 점수를 주는 코드를 작성해보자.
class Exam:
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다'
            )

    # 시험 과목을 이루는 각 부분마다 새로운 @property를 지정하고 관련 검증 메서드를 작성해야 한다는 번거로움이 있다.
    @property
    def writing_grade(self):
        return self._writing_grade
    
    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value
    
    @property
    def math_grade(self):
        return self._math_grade
    
    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

# 이런경우 디스크립터를 사용해볼 수 있다.

# 다음 코드는 Grade의 인스턴스인 클래스 애트리뷰트가 들어 있는 Exam 클래스를 정의한다.
class Grade:
    def __get__(self, instance, instance_type):
        pass

    def __set__(self, instance, value):
        pass

class Exam:
    # 클래스 애트리뷰트
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

# 다음과 같은 프로퍼티 대입은
exam = Exam()
exam.writing_grade = 40

# 다음과 같이 해석된다.
Exam.__dict__['writing_grade'].__set__(exam, 40)

# 다음과 같이 프로퍼티를 읽으면
exam.writing_grade

# 다음과 같이 해석된다.
Exam.__dict__['writing_grade'].__get__(exam, Exam)

# 다음은 Grade 디스크립터를 구현하려고 시도한 코드이다.
class Grade:
    def __init__(self):
        self._value = 0
    
    def __get__(self, instance, instance_value):
        return self._value
    
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다'
            )
        self._value = value

# 한 Exam 인스턴스에 정의된 여러 애트리뷰트에 접근할 경우에는 예상대로 작동한다.
class Exam:
    # 클래스 애트리뷰트
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('쓰기', first_exam.writing_grade)
print('과학', first_exam.science_grade)

# 하지만 여러 Exam 인스턴스 객체에 대해 애트리뷰트 접근을 시도하면 이상하게 작동한다.
second_exam = Exam()
second_exam.writing_grade = 75
print(f'두 번째 쓰기 점수 {second_exam.writing_grade} 맞음')
print(f'첫 번째 쓰기 점수 {first_exam.writing_grade} 틀림; '
    f'82점 이어야 함')

# writing_grade 클래스로 애트리뷰트 한 Grade 인스턴스를 모든 Exam 인스턴스가 공유하기 때문에 문제가 발생한다.

# Grade 클래스가 각각의 유일한 Exam 인스턴스에 대해 따로 값을 추적하게 해야 한다.
class Grade:
    def __init__(self):
        self._values = {}
    
    def __get__(self, instance, instance_value):
        if instance is None:
            return self
        return self._values.get(instance, 0)
    
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다'
            )
        self._values[instance] = value

# 위 방법은 잘 작동하지만, _values 딕셔너리 때문에 메모리 누수가 발생한다.

# 위 문제를 해결하기 위해선 waekref 내장 모듈을 사용할 수 있다.
from weakref import WeakKeyDictionary

class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_value):
        if instance is None:
            return self
        return self._values.get(instance, 0)
    
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다'
            )
        self._values[instance] = value

# 이 Grade 디스크립터 구현을 사용하면 모든 코드가 원하는 대로 작동한다.
class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print(f'첫 번째 쓰기 점수 {first_exam.writing_grade} 맞음')
print(f'두 번째 쓰기 점수 {second_exam.writing_grade} 맞음')