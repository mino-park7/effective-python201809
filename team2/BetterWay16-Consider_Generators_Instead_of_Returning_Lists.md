Better Way 16 리스트를 반환하는 대신 제너레이터를 고려하자
======================================
예. 문자열에 있는 모든 단어의 인덱스 출력하기 
```python
def index_words(text):
    result = []
    if text: 
        result.append(0)
    for index, letter in enumerate(text) 
        if letter == ' ':
            result.append(index + 1)
    return result 
```
샘플이 몇개 뿐일때는 잘 동작하지만, 이 함수에는 두가지 문제가 있다.
1. 코드가 복잡하고 깔끔하지 x
  * 새로운 결과가 나올 때마다 append 메서드를 호출해야 한다.
  * result.append 가 많아서 리스트에 추가하는 값 index+1 이 덜 중요해 보인다. 
  * 결과 리스트 생성에도 한 줄, 반환에도 한 줄이 필요하다. 130 개 문자 중에 중요한 문자는 75개 정도뿐
제너레이터generator를 사용하는 것이 더 좋다. 
* 제너레이터 : yeilds 표현식을 사용하는 함수 
* 호출되면 실제로 실행하지 않고 iterator 를 반환, 내장함수 next 호출할 때마다 iterator 는 제너레이터가 다음 yield 값으로 진행하게 함 
* 제너레이터에서 yeild 에 전달한 값을 이터레이터가 호출하는 쪽에 반환 
```python
def index_words_iter(text):
    if text: 
        yeild 0
    for index, letter in enumerate(text) 
        if letter == ' ':
            yields index + 1
```
* 이해가 훨씬 쉽고, 
* 결과는 리스트가 아니라 yiel 표현식으로 전달되고 
  * 제너레이터 호출로 반환되는 이터레이터를 내장 함수 list에 전달하면 손쉽게 리스트로 변환할 수 있다 refer to BetterWay9
```python
result = list(index_words_iter(address))
```
2. 두번째 문제는, 반환하기 전에 모든 결과를 리스트에 다 담아야 한다는 것이다. 메모리 문제를 일으킬 위험이 있음. 제너레이터는 안 그렇다 

마지막으로 알아둬야할 점: 이터레이터에 상태가 있고 재ㅇ사요할 수 없다는 사실을 호출하는 쪽에서는 알고 있어야 함 


핵심정리
* 제너레이터 방법이 결과 리스트를 반환하는 방법보다 이해하기 명확 
* 제너레이터에서 반환한 이터레이터는 제너레이터 함수 본문에 있은 yield 표현식에 전달된 값들의 집합 
* 제너레이터는 모든 입/출력을 메모리에 저장하는 것이 아님. 그러므로 입력값의 양을 알기 어려울 때도 연속된 출력을 만들수있다 
