Chapter 2. 함수 

Better Way 14 None 을 반환하기보다는 예외를 일으키자 
======================================
어떤 사람들은 반환값 None 에 특정한 의미를 부여함.
* 예. 어떤 수를 다른 수로 나누는 헬퍼함수
 ```python
 def divide(a, b):
     try:
         return a / b 
     except ZeroDivisionError:
         return None
 ```
* 이 헬퍼함수를 사용하는 코드는 반환값을 아래처럼 해석해야 함 
```python
result = divide(x,y) 
if result is None:
    print('Invalid inputs')
```
* 그런데 이렇게 하면 0/5 같은 나눗셈을 수행했을 경우에 문제가 됨. 오류인지 알려고 None 대신 False 값에 대해서 검사할 수도 있고요 
* 어떻게 해결할 수 있을까요? (1) 반환 값을 둘로 나눠서 튜플에 담는다. 첫번째는 작업 성공 여부, 두번째는 계산된 결과
```python
def divide(a, b):
    try:
        return True, a / b 
    except ZeroDivisionError:
        return False, None
succes, result = divide(x,y) 
if not succes:
    print('Invalid inputs')
```
 * 잘 해결된 것 같지만 혹은 코드가 잘못된 것은 없지만, 호출자가 밑줄변수를 써서 튜플 첫부분을 무시해버리기 쉽고 그렇게 되면 결국 우리는 다시 원래 문제로 돌아와지게됩니다
```python
_, result = divide(x,y) 
if not result:
    print('Invalid inputs')
```
* 그러니 이렇게 하지 말고 (2) 아예 절대로 None 반환을 금지해버리자 
  * 대신 호출하는 쪽에서 예외를 처리할 수 있도록 예외를 일으킴 
```python
 def divide(a, b):
     try:
         return a / b 
     except ZeroDivisionError as e:
         raise ValueError('Invalid Inputs') from e # 입력값이 잘못됐음을 알리기 위해 ZeroDivisionError 를 ValueError 로 변경
 ```
 * 그러면 호출한 쪽에서는 잘못된 입력에 대한 예외를 처리하게 됩니다. refer to upcoming BetterWay49 
```python
x,y = 5,2
try : 
    result = divide(x,y) 
except ValueError: 
    print('invalid inputs')
else:
    print('result is %.f' % result)
```
