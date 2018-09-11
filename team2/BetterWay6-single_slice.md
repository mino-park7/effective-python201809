Better Way 6 한 슬라이스에 start, end, stride를 함께 쓰지 말자
=======================================================

***
# 기본
* 슬라이스의 스트라이드(stride: 간격)을 설정하는 특별한 문법
  * ```somelist[start:end:stride]```
  * 이 문법을 사용하면 시퀀스를 슬라이스할 때 매 n번째 아이템을 가져 올수 있음. ex) 홀수, 짝수
  ```python
  a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
  odds = a[::2]
  evens = a[1::2]
  print(odds)
  print(evens)
  
  >>>
  ['red', 'yellow', 'blue']
  ['orange', 'green', 'purple']
  ```
  
# 문제
* stride 문법의 예상치 못한 동작
  * ex) 파이썬에서 바이트 문자열을 역순으로 만드는 일반적인 방법은 -1로 문자열을 슬라이스 하는 것
  ```python
  x = b'mongoose'
  y = x[::-1]
  print(y)
  
  >>>
  b'esoognom'
  ```
  * 위의 코드는 바이트 문자열이나 아스키 문자에는 잘 동작하지만, UTF-8바이트 문자열로 인코드된 유니코드 문자에는 원하는 대로 동작하지 않음.
  ```python
  w = '破二先'
  x = w.encode('utf-8')
  y = x[::-1]
  z = y.decode('utf-8')
  
  >>>
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0x9d in
  position 0: invalis start byte
  ```
  
  * -1 이 아닌 수로 해보기
  ```python
  a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  a[::2]    # ['a', 'c', 'e', 'g']
  a[::-2]   # ['h', 'f', 'd', 'b']
  ```
  * -2::-2, -2:2:-2, 2:2:-2 비교
  ```python
  a[2::2]   # ['c', 'e', 'g']
  a[-2::-2] # ['g', 'e', 'c', 'a']
  a[-2:2:-2]# ['g', 'e']
  a[2:2:-2] # []
  ```
  
  * 요점은 슬라이싱 문법의 stride부분이 매우 혼란스러울 수 있음
    * 대괄호 안에 숫자가 세 개나 있으면 빽빽해서 읽기 어려움
    * 그래서 start와 end 인덱스가 stride와 연계되어 어떤 작용을 하는지 분명하지 않음
    * 특히 stride가 음수 일 땐 더욱 그러함
  * 이런 문제를 방지하려면 stride를 start, end 인덱스와 함께 사용하지 말아야 함
    * stride를 사용해야 한다면 양수 값을 사용하고 start와 end인덱스는 생략하는게 좋음
    * stride를 꼭 start 나 end 인덱스와 함계 사용해야 한다면 stride를 적용한 결과를 변수에 할당하고, 이 변수를 슬라이스한 결과를 다른 변수에 할당해서 사용.
    
  ```python
  b = a[::2]    # ['a', 'c', 'e', 'g']
  c = b[1:-1]   # ['c', 'e']
  ```
  * 슬라이싱부터 하고 스트라이딩을 하면 데이터의 얕은 복사본(shallow copy)이 추가로 생김
    * 첫 번째 연산은 결과로 결과로 나오는 슬라이스의 크기를 최대한 줄여서 할 것
    * 프로그램에서 두 과정에 필요한 시간과 메모리가 충분하지 않다면 내장 모듈 itertools의 islice 메서드(Better Way 46 "내장 알고리즘과 자료 구조를 사용하자" 참고할 것
      * islice 메서드는 ㄴtart, end, stride에 음수 값을 허용하지 않음
      
***
# 핵심정리
* 한 슬라이스에 start, end, stride를 지정하면 매우 혼란하다 혼란해
* 슬라이스에 start와 end 인덱스 없이 양수 stride 값을 사용할 것. 음수 stride 값은 가능하면 피하는게 좋음
* 한 슬라이스에 start, end, stride를 함께 사용하는 상황은 피할 것.
 * 파라미터 세 개를 사용해야 한다면 할당 두 개(하나는 슬라이스, 다른 하나는 스트라이드)를 사용하거나 내장 모듈 itertools의 islice를 사용할 것.
  
  
