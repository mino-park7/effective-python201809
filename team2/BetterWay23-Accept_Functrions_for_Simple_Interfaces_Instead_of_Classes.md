BetterWay 23 인터페이스가 간단하면 클래스 대신 함수를 받자
=

* 파이썬 내장 API의 상당수에는 함수를 넘겨서 동작을 사용자화하는 기능이 있음
* API는 이런 후크(hook)를 이용해서 개발자가 작성한 코드를 실행 중에 호출 함
* ex) list 타입의 sort 메서드는 정렬에 필요한 각 인덱스의 값을 결정하는 선택적인 key 인수를 받음
  * 다음 코드에서는 lambda 표현식을 key 후크로 넘겨서 이름 리스트를 길이로 정렬함

  ```python
  names = ['Sorates', 'Archimedes', 'Plato', 'Aristotle']
  names.sort(key=lambda x: len(x))
  print(names)

  >>>
  ['Plato', 'Socrates', 'Aristotle', 'Archimedes']
  ```
  * 다른 언어에서라면 후크를 추상 클래스로 정의할 것이라고 예상할 수도 있지만
  * 파이썬의 후크 중 상당수는 인수와 반환 값을 잘 정의해놓은 단순히 상태가 없는 함수
    * 함수는 클래스보다 설명하기 쉽고 정의하기도 간단해서 후크로 쓰기에 이상적
    * 함수가 후크로 동작하는 이유는 파이썬이 일급 함수(first-class function)를 갖췄기 때문
      * 다시 말해, 언어에서 함수와 메서드를 다른 값처럼 전달하고 참조할 수 있기 때문
      * 일급함수 : 특정 언어의 일급 객체(first-class citizens, 일급 값, 일급 엔티티, 혹은 일급 시민)이라 함은 일반적으로 다른 객체들에 적용 가능한 연산을 모두 지원하는 객체를 가리킴

* ex) defaultdict 클래스의 동작을 사용자화 한다면?(Better way 46 "내장 알고리즘과 자료 구조를 사용하자" 참조)
  * 이 자료구조는 찾을 수 없는 키에 접근할 때마다 호출될 함수를 받음
  * defaultdict에 넘길 함수는 딕셔너리에서 찾을 수 없는 키에 대응할 기본값을 반환해야하는데
  * 다음의 키를 찾을 수 없을 때마다 로그를 남기고 기본값으로 0을 반환하는 후크를 정의한 코드를 보고 참고할 것.
 
  ```python
  def log_missing():
    print('Key added')
    return 0
  ```
  * 초깃값을 담은 딕셔너리와 원하는 증가 값 리스트로 log_missing 함수를 두번(각각 'red'와 'orange'일 때) 실행하여 로그를 출력하게 해본다면
  ```python
  current = {'green': 12, 'blue': 3}
  increments = [
      ('red', 5),
      ('blue', 17),
      ('orange', 9),
  ]
  result = defaultdict(log_missing, current)
  print('Before:', dict(result))
  for key, amount in increments:
      result[key] += amount
  print('After: ', dict(result))

  >>>
  Before: {'green': 12, 'blue': 3}
  Key added
  Key added
  After: {'orange': 9, 'green': 12, 'blue': 20, 'red': 5}
  ```

* log_missing 같은 함수를 넘기면 결정 동작과 부작용을 분리하므로 API를 쉽게 구축하고 테스트할 수 있음
* ex) 기본값 후크를 defaultdict에 넘겨서 찾을 수 없는 키의 총 개수를 센다고 할 때
  1. 상태 보존 클로저(betterway 15 "클로저가 변수 스코프와 상호 작용 하는 방법을 잘자" 참조)를 사용하기도 함
  2. 보존할 상태를 캡슐화 하는 작은 클래스를 정의 하는 것
 
###### 다음은 상태 보존 클로저를 기본값 후크로 사용하는 헬퍼 함수
```python
def increment_with_report(current, increments):
  added_count = 0
  
  def missing():
    nonlocal added_count  # 상태 보존 클로저
    added_count += 1
    return 0
    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
        
    return result, added_count
```
* defualtdict는 missing 후크가 상태를 유지한다는 사실을 모르지만,
* increment_with_report 함수를 실행하면 튜플의 요소로 기대한 개수인 2를 얻음
  * 이는 간단한 함수를 인터페이스용으로 사용할 때 얻을 수 있는 또 다른 이점
  * 클로저 안에 상태를 숨기면 나중에 기능을 추가하기도 쉬움
  ```python 
  result, count = increment_with_report(current, increments)
  assert count == 2
  ```
   * 상태 보존 후크용을 클로저를 정의할 때 생기는 문제!
    * 상태가 없는 함수의 예제보다 이해하기 어려움

###### 다음은 보존할 상태를 캡슐화 하는 작은 클래스를 정의 하는 것.  
```python
class CountMissing(object):
  def __init__(self):
      self.added = 0
      
  def missing(self):
      self.added += 1
      return 0
```
  * 다른 언어에서라면 이제 CountMissing의 인터페이스를 수용하도록 defaultdict를 수정해야 한다고 생각 할테지만
  * 파이썬에서는일급 함수 덕분에 객체로 CountMissing.missing 메서드를 직접 참조해서 defaultdict의 기본값 후크로 넘길 수 있음
    * 메서드가 함수 인터페이스를 충족하는 건 자명 하드ㅏㅏㅏ
  ```python
  counter = CounterMissing()
  result = defaultdict(counter.missing, current) # 메서드 참조
  for key, amount in increments:
      result[key] += amount
  assert counter.added == 2
  ```
  * 헬퍼 클래스로 상태보존 클로저의 동작을 제공하는 방법이 앞에서 increment_with_report 함수를사용한 방법보다 명확
  * 하지만 CountMissing 클래스 자체만으로는 용도가 무엇인지 바로 이해하기 어려움


* 클래스에 __call__이라는 특별한 메서드를 정의해서 용도를 명확하게 해줌
* __call__ 메서드는 객체를 함수처럼 호출할 수 있게 해줌
* 내장 함수 callable일 이런 인스턴스에 대해서는 True를 반환하게 만듬
```python
class BetterCountMissing(object):
    def __init__(self):
        self.addef = 0
    
    def __call__(self):
        self.added += 1
        return 0
        
counter = BetterCountMissing()
counter()
assert callable(counter)
```
* 다음은 BetterCountMissing 인스턴스를 defaultdict의 기본값 후크로 사용하여 딕셔너리에 없어서 새로 추가된 키의 개수를 알아내는 코드
```python
count = BetterCountMissing()
result = defaultdict(counter, current) # __call__이 필요함
for key, amount in incrments:
    result[key] += amount
assert counter.added == 2
```

* 위 예제가 CounterMissing.missing 예제보다 명확한데
* __call__ 메서드는 (API 후크처럼) 함수 인수를 사용하기 적합한 위치에 클래스의 인스턴스를 사용할 수 있다는 사실을 드러냄.
  * 이 코드를 처음 보는 사람을 클래스의 주요 동작을 책임지는 진입점(entry point)으로 안내하는 역할도 함.
  * 클래스의 목적이 상태 보존 클로저로 동작하는 것이라는 강력한 인트 제공
 
* 무엇보다도 __call__을 사용할 때 defaultdict는 여전히 무슨일이 일어나는지 모름
  * defualtdict에 필요한 건 기본값 후크용 함수 뿐
  * 파이썬은 하고자 하는 장업에 따라 간단한 함수 인터페이스를 충족하는 다양한 방법을 제공
 
***
# 핵심정리
* 파이썬에서 컴포넌트 사이의 간단한 인터페이스용으로 클래스를 정의하고 인스턴스를 생성하는 대신에 함수만 써도 종종 충분함
* 파이썬에서 함수와 메서드에 대한 참조는 일급. 즉, 다른 타입처럼 표현식에서 사용할 수 있음
* __call__이라는 특별한 메서드는 클래스의 인스턴스를 일반 파이썬 함수처럼 호출할 수 있게 해줌
* 상태를 보존하는 함수가 필요할 때 상태 보존 클로저를 정의하는 대신 __call__ 메서드를 제공하는 클래스를 정의하는 방안을 고려할 것
  * (Betterway 15 "클로저가 변수 스코프와 상호 작용하는 방법을 알자" 참고)
