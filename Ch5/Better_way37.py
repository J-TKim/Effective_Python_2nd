# 이름을 미리 알 수 없는 상황에서 학생들의 점수를 기록하는 코드
class SimpleGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('아이작 뉴턴')
book.report_grade('아이작 뉴턴', 90)
book.report_grade('아이작 뉴턴', 85)
book.report_grade('아이작 뉴턴', 95)

print(book.average_grade('아이작 뉴턴'))



# 과목별 성적을 리스트로 저장하고 싶은 경우 딕셔너리 안의 딕셔너리 형태로 구현할 수 있다.
from collections import defaultdict

class BySubjectGradebook:
    def __init__(self):
        self._grades = {} # 외부 dict
    
    def add_student(self, name):
        self._grades[name] = defaultdict(list) # 내부 dict
    
    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)
    
    def average_grade(self, name):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grade in by_subject.values():
            total += sum(grade)
            count += len(grade)
        return total / count

book = BySubjectGradebook()
book.add_student('알버트 아인슈타인')
book.report_grade('알버트 아인슈타인', '수학', 75)
book.report_grade('알버트 아인슈타인', '수학', 65)
book.report_grade('알버트 아인슈타인', '체육', 90)
book.report_grade('알버트 아인슈타인', '체육', 95)

print(book.average_grade('알버트 아인슈타인'))

# 각 점수의 가중치를 함께 저장해서 중간고사와 기말고사가 다른 쪽지 시험보다 성적에 더 큰 영향을 미치도록 하는 코드
class WeightedGradebook:
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))

    def average_grade(self, name):
        by_subject = self._grades[name]

        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0

            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight
            
            score_sum += subject_avg / total_weight
            score_count += 1
        
        return score_sum / score_count



book = WeightedGradebook()

book.add_student('알버트 아인슈타인')
book.report_grade('알버트 아인슈타인', '수학', 75, 0.05)
book.report_grade('알버트 아인슈타인', '수학', 65, 0.15)
book.report_grade('알버트 아인슈타인', '수학', 70, 0.80)
book.report_grade('알버트 아인슈타인', '체육', 100, 0.40)
book.report_grade('알버트 아인슈타인', '체육', 95, 0.60)

print(book.average_grade('알버트 아인슈타인'))

# 리스트 안에 점수를 저장하기 위해 튜플을 활용한다.
grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight

# 튜플이 커지면 _ 를 더 많이 사용해야하는 문제점이 발생한다.
grades = []
grades.append((95, 0.45, '참 잘했어요'))
grades.append((85, 0.55, '조금만 더 열심히'))
total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight

# 위와 같은 문제를 해결하기 위해 namedtuple를 사용할 수 있다.
from collections import namedtuple

Grade = namedtuple('Grade', ('score', 'weight'))

# 일련의 점수를 포함하는 단일 과목을 표현하는 클래스를 작성할 수 있다.
class Subject:
    def __init__(self):
        self._grades = []
    
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

# 한 학생이 수강하는 과목들을 표현하는 클래스를 작성할 수 있다.
class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]
    
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

# 모든 학생을 저장하는 컨테이너를 작성할 수 있다.
class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)
    
    def get_student(self, name):
        return self._students[name]

# 가독성이 더 좋아졌다.
book = Gradebook()
albert = book.get_student('알버트 아인슈타인')
math = albert.get_subject('수학')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject('체육')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())