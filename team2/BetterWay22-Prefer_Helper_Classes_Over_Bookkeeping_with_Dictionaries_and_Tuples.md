BetterWay 22 딕셔너리와 튜플보다는 헬퍼 클래스로 관리하자
=====

* 파이썬에 내장되어 있는 딕셔너리 타입은 객체의 수명이 지속되는 동안 동적인 내부상태를 관리하는 용도로 아주 좋음
  * 여기서 '동적'이란? 예상하지 못한 식별자들을 관리해야 하는 상황 
  * ex) 이름을 모르는 학생 집단의 성적 기록
    * 학생별로 미리 정의된 속성을 사용하지 않고 딕셔너리에 이름을 저장하는 클래스를 정의 할 수 있음
    
```python
class SimpleGradebook(object):
  def __init__(self):
      selt._grades = {}
  
  def add_student(self, name):
      self.grades[name] = []
      
  def report_grade(self, name, score):
      self._grades[name].append(score)
  
  def average_grade(self, name):
      grades = self._grades[name]
      return sum(grades) / len(grades)
```

  * 클래스를 사용하는 방법(간단함)

```python
book = SimpleGradebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)
# ...
print(book.average_grade('Isaac Newton'))

>>>
90.0
```

* 하지만!
* 딕셔너리는 정말 사용하기 쉬워서 과도하게 쓰다가 코드를 취약하게 작성할 위험이 있음
  * ex) SimpleGradebook 클래스를 확장해서 모든 성적을 한곳에 저장하지 않고 과목별로 저장한다고 할 때
    * __grades 딕셔너리를 변경해서 학생 이름(키)을 또 다른 딕셔너리(값)에 매핑하면 됌
    * 가장 안쪽에 있는 딕셔너리는 과목(키)을 성적(값)에 매핑

```python
class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}
        
    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)
        
    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count
```

  * 위와 같이 모든 성적을 한곳에 저장하지 않고 과목별로 저장할 때 클래스를 사용하는 방법(아직 간단함)

```python
book = BySubjectGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75)
book.report_grade('Albert Einstein', 'Math', 65)
book.report_grade('Albert Einstein', 'Gym', 90)
book.report_grade('Albert Einstein', 'Gym', 95)
```
    * 이어서 수업의 최종 성적에서 각 점수가 차지하는 비중을 매겨서 중간고사와 기말고사를 쪽지시험보다 중요하게 만들려고 한다면!?
    * 이 기능을 구현하는 방법 중 하나는 가장 안쪽 딕셔너리르 변경해서 과목(키)을 성적(값)에 매핑하지 않고,
    * 성적과 비중을 담은 튜플 (score, weight)에 매핑 하는 것

```python
class WeightedGradebook(object):
    # ...
    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grdae_list = by_subject.setdefault(subject,  [])
        grade_list.append((score,weight))
```
    * 값을 튜플로 바꾸기만 한 것 뿐
    * report_grade를 수정한 내역은 간단해 보이지만, average_grade 메서드는 루프 안에 루프가 생겨서 이해하기 어려워졌음

```python
    def average_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0,0
        for subject, scores in by_subejct.items():
            subject_avg, total_weight = 0,0
            for score, weight in scores:
                # ...
        return score_sum / score_count
```
    * 클래스를 사용하는 방법도 어려워 지기 시작

```python
book.report_grade('Albert Einstein', 'Math', 80, 0.10)
```
  * 이렇게 복잡해지면 딕셔너리와 튜플 대신 클래스의 계층 구조를 사용할 때가 된 것이라 보면 됌
      * 처음엔 성적에 비중을 적용하게 될지 몰랐으니 복잡하게 헬퍼 클래스를 추가 할 필요 까지는 없어 보였지만
      * 파이썬의 내장 딕셔너리와 튜플 타입을 쓰면 내부 관리용으로 층층이 타입을 추가하는 게 쉬워짐.
      * 하지만 계층이 한 단계가 넘는 중첩은 다른 프로그래머들이 코드를 이해하기 어렵고 유지보수가 힘들어 져서 피해야 함
        * (즉, 딕셔너리를 담은 딕셔너리는 쓰지 말 것)
        * 관리하기 복잡하다고 느끼는 즉시 클래스로 옮기면 됌
        * 그러면 데이터를 더 잘 캡슐화 한 잘 정의된 인터페이스를 제공할 수 있음
        * 또한 인터페이스와 실제 구현 사이에 추상화 계층을 만들 수 있음

## 클래스 리팩토링
* ex) 의존 관계에서 가장 아래에 있는 성적부터 클래스로 옮기기
  * 이렇게 간단한 정보를 담기에 클래스는 너무 무거워 보임
  * 성적은 변하지 않으니 튜플을 사용하는 게 더 적절해 보임
  * 다음 코드에서는 리스트 안에 성적을 기록하려고 (score, weight) 튜플을 사용

```python
grades - []
grades.append((95, 0.45))
# ...
total = sum(score * weight for scre, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight
```
  * 문제! 일반 튜플은 위치에 의존함
  * 성적에 선생님의 의견 같은 더 많은 정보를 연관지으려면 이제 튜플을 사용하는 곳을 모두 찾아서 아이템 두 개가 아니라 세 개를 쓰도록 수정해야 함
    * 다음 코드에서는 튜플에 있는 세 번째 값을 _로 받아서 그냥 무시하도록 함(파이썬에서는 관례적으로 사용하지 않을 변수에 밑줄 변수 이름을 씁니당ㅎㅎ)
    
```python
grades = []
grades.append((95, 0.45, 'Great job'))
# ...
total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight
```

    * 튜플을 점점 더 길게 확장하는 패턴은 딕셔너리의 계층을 깊게 두는 방식과 비슷
    * 튜플의 아이템이 두 개를 넘어가면 다른 방법도 고려해야함
       * collections 모듈의 namedtuple 타입이 정확히 이런 요구에 부합
       * namedtuple을 이용하면 작은 불변 데이터 클래스(immutable data class)를 쉽게 정의 할 수 있음

```python
import collections
Grade = collections.namedtuple('Grade', ('score', 'weight'))
```

      * 불변 데이터 클래스는 위치 인수나 키워드 인수로 생성할 수 있음
      * 필드는 이름이 붙은 속성으로 접근할 수 있음
      * 이름이 붙은 속성이 있으면 나중에 요구 사항이 또 변해서 단순 데이터 컨테이너에 동작을 추가해야 할 때 
      * namedtuple에서 직접 작성한 클래스로 쉽게 바꿀 수 있음
      
> **namedtuple의 제약**
> namedtuple이 여러 상황에서 유용하긴 하지만 장점보다 단점을 만들어 낼 수 있는 상황도 이해 할 것!
> * namedtuple로 만들 클래스에 기본 인수 값을 설정할 수 없음. 
>    * 그래서 데이터에 선택적인 속성이 많으면 다루기 힘들어 짐.
>    * 속성을 사용할 때는 클래스를 직접 정의하는 게 나을 수 있음
>  * namedtuple 인스턴스의 속성 값을 여전히 숫자로 된 인덱스와 순회 방법으로 접근 할 수 있음
>    * 특히 외부 API로 노출한 경우에는 의도와 다르게 사용되어 나중에 실제 클래스로 바꾸기 더 어려울 수도 있음
>    * namedtuple 인스턴스를 사용하는 방식을 모두 제어 할 수 없다면 클래스를 직접 정의하는 게 나음.

1. ex) 성적들을 담은 단일 과목을 표현하는 클래스

```python
class Subject(object):
    def __init__(self):
        self._grades = []
        
    def report_grade(self, scroe, weight):
        self._grades.append(Grade(score, weight))
        
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight
```

2. ex) 한 학생이 공부한 과목들을 표현하는 클래스

```python
class Student(object):
    def __init__(self):
        self._subjects = {}
        
    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]
        
    def average_grade(self):
        total, count = 0,0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count
```

3. ex) 학생의 이름을 키로 사용해 동적으로 모든 학생을 담을 컨테이너

```python
class Gradebook(object):
    def __init__(self):
        self._students = {}
        
    def studnet(self, name):
        if name not in self._students:
            self._studnets[name] = Student()
        return self._students[name]
```

* 위 세 클래스의 코드 줄 수는 이전에 구현한 코드의 두 배에 가깝지만 
  * 훨씬 이해하기 쉽고
  * 이 클래스들을 사용하는 예제도 더 명확하고
  * 확장하기 쉬움
  
```python
book = Gradebook()
albert = book.student('Albert Einstein')
math = albert.subject('Math')
math.report_grade(80, 0.10)
# ...
print(albert.average_grade())

>>>
81.5
```
* 필요하면 이전 형태의 API 스타일로 작성한 코드를 새로 만든 객체 계층 스타일로 바꿔주는 하위 호환용 메서드를 작성해도 됌

***
# 핵심정리
* 다른 딕셔너리나 긴 튜플을 값으로 담은 딕셔너리를 생성하지 말 것.
* 정식 클래스의 유연성이 필요 없다면 가벼운 불변 데이터 컨테이너에는 namedtuple을 사용 할 것.
* 내부 상태를 관리하는 딕셔너리가 복잡해지면 여러 헬퍼 클래스를 사용하는 방식으로 관리 코드를 바꿀 것.
