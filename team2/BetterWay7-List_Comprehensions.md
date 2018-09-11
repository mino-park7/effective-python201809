Better Way 7.
map과 filter 대신 리스트 컴프리헨션을 사용하자
=====================================
* list comprehension(리스트 함축 표현식)이란? 한 리스트에서 다른 리스트를 만들어내는 문법
***

```python
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x ** 2 for x in a]
print(squares)

>>>
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

* 인수가 하나뿐인 함수를 적용하는 사오한이 아니면, 간단한 연산에는 리스트 컴프리헨션이 내장 함수 map보다 명확함.
  * map을 쓰려면 계산에 필요한 lamda 함수를 생성해야 해서 깔끔해 보이지 않음
```python
sqaures = [x ** 2 for x in a]
squares = map(lambda x: x ** 2, a)
```
* map과 달리 리스트 컴프리헨션을 사용하면 입력 리스트에 있는 아이템을 간편하게 걸러내서 그에 대응하는 출력을 결과에서 삭제할 수 있음.
* ex) 2로 나누어 떨어지는 숫자의 제곱만 계산
```python
even_squares = [x ** 2 for x in a if x % 2 == 0]
print(even_squares)

>>>
[4, 16, 36, 64, 100]
```
  * 내장 함수 filter를 map과 연계해서 사용해도 같은 결과를 얻을 수 있지만 훨씬 읽기 어려움
```python
alt = map(lambda x: x ** 2, filter(lambda x : x % 2 == 0, a))
assert even_squares == list(alt)
```
    * assert란? True 확인하고 아니면 error발생
      * 쓰임새? 디버깅 효과

* 딕셔너리와 세트에도 리스트 컴프리헨션에 해당하는 문법이 있음
  * 컴프리헨션 문법을 쓰면 알고리즘을 작성할 때 파생되는 자료 구조를 쉽게 생성 가능.
  
```python
chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}
chile_len_set = {len(name) for name in rank_dict.values()}
print(rank_dict)
print(chile_len_set)

>>>
{1: 'ghost', 2: 'habanero', 3: 'cayenne'}
{8, 5, 7}
```

# 핵심정리
* 리스트 컴프리헨션은 추가적인 lambda 표현식이 필요 없어서 내장 함수인 map이나 filter를 사용하는 것보다 명확
* 리스트 컴프리헨션을 사용하면 입력 리스트에서 아이템을 간단히 건너뛸 수 있음.
  * map이나 filter를 사용하지 않고선 이런 작업 불가
* 딕셔너리와 세트도 컴프리헨션 표현식을 지원


