BetterWay 21 키워드 전용 인수로 명료성을 강요하자
====================================================
* 키워드 전용 인수
 * 위치로 구분하는 일반 인수가 아닌 ignore_overflow=False 와 같은 명시적 인수

* 키워드로 인수를 넘기는 방법은 파이썬 함수의 강력한 기능
* 키워드 인수의 유연성 덕분에 쓰임새가 분명하게 코드를 작성할 수 있음
 * ex) ignore_zero_division
 * ex) ignore_overflow

```python
def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
 try:
  return number / divisor
 except OverflowError:
 if ignore_overflow:
  return 0
 else:
  raise
 except ZeroDivisionError:
  if ignore_zero_division:
   return float('inf')
  else:
   raise
```
* 다음 함수 호출은 나눗셈에서 일어나는 float 오버플로우를 무시하고 0을 반환
```python
result = safe_division(1, 10**500, Ture, False)
print(result)

>>>
0.0
```
* 다음 함수호출은 0으로 나누면서 일어나는 오류를 무시하고 무한대 값을 반환
```python
result = safe_division(1, 0, False, True)
print(result)

>>>
inf
```

* 문제! 예외 무시 동작을 제어하는 두 bool 인수의 위치를 혼동하기 쉬움
* 이런 코드의 가독성을 높이기 위해 다음과 같이 키워드 인수를 사용

```python
def safe_division_b(number, divisor, 
                    ignore_overflow=False,
                    ignore_zero_division=False):
 # ...
```
* 키워드 인수를 지정했기 때문에 호출하는 쪽에서 키워드 인수로 특정 연산에는 기본 동작(여기에선 False)을 덮어 쓰고 무시할 플래그를 지정할 수 있음
```python
safe_division_b(1, 10**500, ignore_overflow=True)
safe_division_b(1, 0, ignore_zero_division=True)
```

* 문제! 이런 키워드 인수가 선택적인 동작이라서 함수를 호출하는 쪽에 키워드 인수로 의도를 명황하게 드러내라고 강요는 못함. 하지만 책에선 쓸것을 추천
```python
safe_division_b(1, 10**500, True, False)
```
* 위와같은 복잡한 함수(?)를 작성할 때는 호출하는 쪽에서 의도를 명확히 드러내도록 요구하는 게 낫기 때문에 파이썬 3에서는 키워드 전용 인수(keyword-only argument)로 함수를 정의해서 의도를 명확히 드러내도록 요구살 수 있음
 * 키워드 전용인수는 키워드로만 넘길 뿐, 위치로는 절대 넘길 수 없음
 * 다음과 같이 인수 리스트에 있는 "*"기호로 위치 인수의 끝과 키워드 전용 인수의 시작을 가르킬 수 있음
```python
def safe_division_c(number, divisor, *, 
                    ignore_overflow=False, 
                    ignore_zero_division=False):
 # ...
```

* 키워드 인수가 아닌 위치 인수를 사용하는 함수 호출은 동작하지 않음
```python
safe_division_c(1, 10**500, True, False)

>>>
TypeError: safe_division_c() takes 2 positional arguments but 4 were given
```
* 키워드 인수와 그 기본값은 기대한대로 동작
```python
safe_division_c(1, 0, ignore_zero_division=True) # 문제없음

try:
    safe_division_c(1,0)
except ZeroDivisionError:
    pass # 기대한 대로 동작함
```

## 파이썬 2의 키워드 전용 인수
* 파이썬 2에는 파이썬 3처럼 키워드 전용 인수를 지정하는 명시적 문법이 없음
* 하지만 인수 리스트에 ** 연산자를 사용해 올바르지 않은 함수 호출을 할 때 TypeError를 일으키는 방법으로 같은 동작을 만들어 왔음
** 가변 개수의 위치 인수 대신에 키워드 인수를 몇 개든 받을 수 있다는 점 기억할 것!(이것만 빼면 ** 연산자는 * 연산자와 비슷)

### 파이썬2
```python
def print_args(*args, **kwards):
   print 'Positional:', args
   print 'Keyword:   ', kwargs
   
print_args(1, 2, foo='bar', stuff='meep')

>>>
Positional: (1, 2)
Keyword: {'foo': 'bar', 'stuff': 'meep'}
```
1. 위와같이 파이썬 2에서는 safe_division이 **kwargs를 받게 만들어서 키워드 전용 신수를 받게 함
2. 그런 다음 pop 메서드로 kwargs 딕셔너리에서 원하는 키워드 인수를 꺼냄
3. 키가 없을 때의 기본값은 pop 메서드의 두번째 인수로 지정
4. 마지막으로 kwargs에 더는 남아 있는 키워드가 없음을 확인하여 호출하는 쪽에서 올바르지 않은 인수를 넘기지 않게 함

### 파이썬2
```python
def safe_division_d(number, divisor, **kwargs):
    ignore_overflow = kwargs.pop('ignore_overflow', False)
    ignore_zero_div = kwargs.pop('ignore_zero_division', False)
    if kwargs:
        raise TypreError('Unexpected **kwargs: %r' % kwargs)
    # ...
```

* 위와같이 코딩한다면 이제 키워드 인수를 넘기든 안넘기든 함수를 호출할 수 있음
```python
safe_division_d(1, 10)
safe_division_d(1, 0, ignore_zero_division=True)
safe_division_d(1, 10**500, ignore_overflow=True)
```
* 키워드 전용 인수를 위치로 넘기려고 하면 파이썬 3와 마찬가지로 제대로 동작하지 않음
```python
safe_division_d(1, 0, False, True)

>>>
TypeError: safe_division_d() takes 2 positional arguments but 4 were given
```
* 원하지 않은 키워드 인수를 넘겨도 제대로 동작하지 않음
```python
safe_division_d(0, 0, unexpected=True)

>>>
TypeError: Unexpected **kwargs: {'unexpected': Ture}
```
***
# 핵심정리
* 키워드 인수는 함수 호출의 의도를 더 명확하게 해줌
* 특히 bool 플래그를 여러 개 받는 함수처럼 헷갈리기 쉬운 함수를 호출할 때 키워드 인수를 넘기게 하려면 키워드 전용 인수를 사용하는 것이 좋음
* 파이썬 3는 함수의 키워드 전용 인수 문법을 명시적으로 지원함
* 파이썬 2에서는 **kwargs를 사용하고 TypeError 예외를 직접 일으키는 방법으로 함수의 키워드 전용 인수를 흉내 낼 수 있음
