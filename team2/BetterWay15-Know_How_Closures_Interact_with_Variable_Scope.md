Better Way 15 클로저가 변수 스코프와 상호작용하는 방법을 알자
======================================
## 스코프 버그?
예. 숫자를 정렬할 때 특정 그룹의 숫자들이 먼저 오도록 하고 싶음. 
* 리스트의 sort 메소드에 헬퍼함수를 key 인수로 넘기는 것 
  * 헬퍼함수 반환값은 리스트 각 아이템 정렬하는 값으로 사용됨 
```python
def sort_priority(values, group):
    def helper(x): 
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)
# 실행 예시
numbers = [8, 3, 1, 2, 5, 4, 7, 6] 
group = {2, 3, 5, 7} 
sort_priority(numbers, group)
print(numbers)
>>> 
[2, 3, 5, 7, 1, 4, 6, 8]
```
이 코드가 왜 작동했는가? 
1. 파이썬이 클로저closure를 지원하기 때문. 
  * 클로저란? 자신이 정의된 스코프에 있는 변수를 참조하는 함수 
  * helper 함수가 sort_priority 의 group 인수에 접근할 수 있었던 것을 보세요 
2. 함수는 파이썬에서 일급객체first-class object이다. 
  * 함수를 직접 참조하고, 변수에 할당하고, 다른 함수의 인수로 전달하고, 표현식이나 if문 등에서 비교할 수 있다. 
  * 예를 들면 sort 메소드에서 클로저 함수를 key 인수로 받을 수 있다. 
3. 파이썬에는 특별한 튜플 비교 규칙이 있다. 
  * 인덱스 0으로 아이템 비교, 그 다음에는 인덱스 1 ,2, ... 
  * helper 클로저의 반환값이 정렬 순서를 두 파트로 나눌 수 있었던 것이 이 룰 때문 
우선순위가 높은 아이템을 발견했는지 여부를 반환해서 사용자인터페이스 코드가 그에 따라 동작하게 하면 어떨까? 
  * 헬퍼함수 반환값은 리스트 각 아이템 정렬하는 값으로 사용됨 
```python
def sort_priority2(values, group):
    found = False
    def helper(x): 
        if x in group:
            found = True    # Easy?
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found
# 실행 예시
numbers = [8, 3, 1, 2, 5, 4, 7, 6] 
group = {2, 3, 5, 7} 
found = sort_priority2(numbers, group):
print('Found:', found) 
>>> 
Found: False
[2, 3, 5, 7, 1, 4, 6, 8]
```
정렬은 잘 됐지만 found 는 예상과 다르게 나왔다. 이것은 인터프리터가 참조를 해결할 때 아래 순서로 스코프를 탐색하기 때문인데요 
1. 현재 함수 스코프 
2. 현재 스코프를 감싸고 있는 스코프 (현 스코프를 담고 있는 다른 함수 같은) 
3. 코드를 포함하고 있는 모듈의 스코프 (전역 스코프)
4. 내장 스코프 (len이나 str 같은 함수를 담고 있는)
* 이중 어디에도 참조한 이름으로 된 변수가 정의되어 있지 않으면 NameError 를 준다

(변수 값 할당과는 다른데요, 현 스코프에서 변수가 정의되어 있다면 새로운 값으로 교체되고, 그렇지 않다면 새 변수 정의처럼 작동함. 
이때 이 변수의 스코프는 그 정의를 포함하고 있는 함수가 되겠습니다) 

헬퍼 클로저 함수에서는 sort_priority2 에서 일어난 할당이 아니라, 새로운 변수 정의로 처리되었기 때문에 ㅠ 이런 일이 일어나게 되었음 

초심자들이 놀라고 그래서 이것이 스코프 버그라고도 불렸는데, 버그가아니라!! 의도한 결과이고, 전역변수들이 오염되거나 추적하기 어려운 상호작용이 마구 일어나는 것을 막아줍니다. 
## 데이터 얻어오기
python3 의 문법 중에, 클로저에서 데이터를 얻어오는 특별한 문법 nonlocal 
* nonlocal 문은 특정변수 이름에 할당할 때 스코프 탐색이 일어나야 함을 나타냄 
* 제약사항 : nonlocal 이 모듈 수준 스코프까지는 탐색할 수 없음. 이는 전역변수 오염을 막기 위함 
```python
def sort_priority3(values, group):
    found = False
    def helper(x):
        nonlocal found 
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found
```
* 클로저에서 데이터를 다른 스코프로 할당하는 시점을 알아보기 쉽게 해주며, 모듈 스코프에 직접 들어가게 하는 global 문을 보완함
* 그러나, 간단한 함수가 아닌 경우에는 nonlocal 문을 사용하지 않는 것이 좋다. nonlocal 때문에 생긴 부작용은 디버깅하기 어려움!! 

nonlocal 을 사용할 때 복잡해지기 시작하면 헬퍼 클래스로 상태를 감싸는 방법이 낫다. __call__ 에 대한 자세한 설명은 refer to upcoming BetterWay23
'``python
def sort_priority3(values, group):
    found = False
    def helper(x):
        nonlocal found 
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found
```
## Python2에서의 스코프 
python2 는 nonlocal 키워드 지원하지 않음 . 
```python
# python2
def sort_priority_python2(values, group):
    found = [False]
    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found[0]
```
이렇게 하는 트릭은... found 값은 수정가능한 list 이고, 클로저에서 일단 found 받아온 후에 내부 스코프에서 값만 변경해서 데이터를 보낼 수 있음 

핵심정리 
* 클로저 함수는 자기가 정의된 범위 중 어디에 있는 변수도 다 참조할 수 있지만 
* 클로저에서 변수 할당하면 범위 바깥쪽에는 영향을 못 줌 
* python3 에서는 nonlocal 문을 사용하여서 클로저를 감싸고 있는 범위의 변수도 수정할 수 있음을 알릴수있다 
* python2 에서는 리스트 같은 수정가능한 값으로 이 문제를 우회할 수도 있다 
* 간단한 함수이외에는 nonlocal 문을 쓰지 x 
