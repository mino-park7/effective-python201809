BetterWay 24 객체를 범용으로 생성하려면 @classmethoc 다형성을 이용하자
=

* 파이썬에서는 객체가 다형성을 지원할 뿐만 아니라 클래스도 다형성을 잘 지원함

* 다형성: 계층 구조에 속한 여러 클래스가 자체의 메서드를 독립적인 버전으로 구현하는 방식
  * 다형성을 이용하면 여러 클래스가 같은 인터페이스나 추상기반 클래스를 충족하면서도 다른 기능을 제공할 수 있음
    * (Better wya 28 "커스텀 컨테이터 타입은 collections.abc의 클래스를 상속받게 만들자"의 예제 참조
    
* ex) 맵리듀스(MapReduce) 구현을 작성할 때 입력 데이터를 표현할 공통 클래스가 필요하다고 가정
  * 다음은 서브클래스에서 정의해야 하는 read 메서드가 있는 입력 데이터 클래스

  ```python
  class InputData(object):
      def read(self):
          raise NotImplementedError
  ```
  * 다음은 디스크에 있는 파일에서 데이터를 읽어오도록 구현한 InputData의 서브클래스
  ```python
  class PatheInputData(InputData):
      def __init__(self, path):
      super().__init__()
      self.path = path
      
      def read(self):
          return open(self.path).read()
  ```
  * PathInpuData 같은 INputData 서브클래스가 몇개든 있을 수 있고,
  * 각 서브 클래스에서는 처리할 바이트 데이터를 반환하는 표준 인터페이스인 read를 구현할 것임
  * 다른 InputData 서브 클래스는 네트워크에서 데이터를 읽어오거나 데이터의 압축을 해제하는 기능 등을 할 수 있음
  
  * 표준 방식으로 입력 데이터를 처리하는 맵 리듀스 작업 클래스에도 비슷한 추상 인터페이스가 필요함

*** 
# 핵심정리
* 파이썬에서는 클래스별로 생성자를 한 개(__init__메서드)만 만들 수 있음
* 클래스에 필요한 다른 생성자를 정의하려면 @classmethod를 사용할 것
* 구체 서브클래스들을 만들고 연결하는 범용적인 방법을 제공하려면 클래스 메서드 다형성을 이용할 것.
