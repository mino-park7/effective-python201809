BetterWay 24 객체를 범용으로 생성하려면 @classmethod 다형성을 이용하자
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
  ```python
  class Worker(object):
      def __init__(self, input_data):
          self.input_data = input_data
          self.result = none
          
      def map(self):
          raise NotImplementedError
      
      def reduce(self, other):
          raise NotImplementedError
  ```
  * 다음은 적용하려는 특정 맵리듀스 함수를 구현한 Worker의 구체 서브클래스(간단한 줄바꿈 카운터).
  ```python
  class LineCountWorker(Worker):
      def map(self):
          data = self.input_data.read()
          self.result = data.count('\n')
          
      def reduce(self, other):
          self.result += other.result
  ```
  * 위 코드는 잘 동작할 것처럼 보이지만 결국 커다란 문제가 ㅣㅇㅆ음
  * 문제! 이 모든 코드 조각을 무엇으로 연결할 것인가
    * 적절히 인터페이스를 설계하고 추상화한 클래스들이지만 일단 객체를 생성한 후에 쓸 수 있음
     
    1. 헬퍼 함수로 직접 객체를 만들고 연결하는 것 - (가장 간단한 방법)
      * ex) 디렉토리의 내용을 나열하고 그 안에 있는 각 파일로 PathInputData 인스턴스를 생성하는 코드
      ```python
      def generate_inputs(data_dir):
          for name in os.listdir(data_dir):
              yield PathInputData(os.path.join(data_dir, name))
      ```
      * 다음으로 generate_inputs 함수에서 반환한 InpuData 인스턴스를 사용하는 LineCountWorkder 인스턴스를 생성하는 코드
      ```python
      def Create_workers(input_list):
          workers = []
          for input_data in input_list:
              workers.append(LineCountWorker(input_data))
          return workers
      ```
      * map 단계를 여러 스레드로 나눠서 이 Worker 인스턴스들을 실행
        * (Betterway 37 "스레드를 블로킹 I/O용으로 사용하고 병렬화용으로는 사용하지 말자" 참고)
      * 그 뒤에 reduce를 반복적으로 호출해서 결과를 최종값 하나로 합칠 것
      ```python
      def excute(workers):
          threads = [Thread(target=w.map) for w in workers]
          for thread in threads: thread.start()
          for thread in threads: thread.join()
          
          first, rest = workers[0], workers[1:]
          for worker in rest:
              first.reduce(worker)
          return first.result
      ```
      * 마지막으로 단계별로 실행하기 위해 mapreduce 함수에서 모든 조각을 연결
      ```python
      def mapreduce(data_dir):
      inputs = generate_inputs(data_dir)
      workers = create_workers*inputs)
      return exectue(workers)
      ```
      
      * 트스트용 입력파일로 함수 실행 결과
      ```python
      from tempfile import TmeporaryDirectory
      
      def write_test_files(tmpdir):
          # ...
          
      with TemporaryDirectory() as tmpdir:
          write_test_files(tmpdir)
          result = mapreduce(tmpdir)
          
      print('There are', result, 'lines')
      
      >>>
      There are 4360 lines
      ```
    * 하지만 위 코드는 mapreduce 함수가 전혀 범용적이지 않음
      * 다른 inputData나 Worker 서브클래스를 작성한다면 generate_inputs, create_workers, mapreduce 함수를 알맞게 다시 작성해야함
        * 따라서 객체를 생성하는 범용적인 방법의 필요성을 생각해서
          * 각 InputData 서브클래스에서 맵리듀스를 조율하는 헬퍼 메서드가 범용적으로 사용할 수 있는 특별한 생성자를 제공해야함
            * 근데 파이썬이 단일 생성자 메서드 __init__만을 허용
          * 결국 모든 InputData 서브클래스가 호환되는 생성자를 갖춰야 한다는 건 터무니 없는 요구사항..
    * **범용적으로 사용하기 위해 @classmethod 다형성을 이용**
      * @classmethod 다형성은 생성된 객체가 아니라 전체 클래스에 적용된다는 점만 빼면 InputData.read에 사용한 인스턴스 메서드 다형성과 같음
      * 맵리듀스 관련 클래스에 적용해보면
        * 공통인터페이스를 사용해 새 InputData 인스턴스를 생성하는 범용 클래스 메서드로 InputData 클래스를 확장
        ```python
        class GenericInputDAta(object):
            def read(self):
                raise NotImplementedError
                
            @classmethod
            def generate_inputs(cls, config):
                raise NotImplementedError
        ```
        * generate_inputs 메서드는 GenericInputData를 구현하는 서브클래스가 해석할 설정 파라미터들을 담은 딕셔너리를 받음
        * 다음은 입력파일들을 얻어올 디렉토리를 config로 알아내기 위한 코드
        ```python
        class PathInputData(GenericInputData):
            # ...
            def read(self):
                return open(self.path).read()
                
            @classmethod
            def generate_inputs(cls, config):
                data_dir = config['data_dir']
                for name in os.listdir(data_dir):
                    yield cls(os.path.join(data_dir, name))
        ```
        * 위 코드와 비슷하게 다음엔 GenericWorker 클래스에 create_workers 헬퍼를 작성
          * input_class 파라미터(GenericInputData의 서브클래스)로 필요한 입력을 만듬
          * cls()를 범용 생성자로 사용해서 GenericWorker를 구현한 서브클래스의 인스턴스를 생성
        ```python
        class GenericWorker(object):
            # ...
            def map(self):
                raise NotImplementedError
                
            def reduce(self, other):
                raise NotImplementedError
                
            @classmethod
            def create_workers(cls, input_class, config):
                workers = []
                for input_data in input_class.generate_inputs(config): # 클래스 다형성 - input_class.generate_inputs 호출
                    workers.append(cls(input_data))
                return workers
        ```
        * 위의 input_class.generate_inputs 호출이 바로 여기에서 보여주려는 클래스 다형성
          * create_workers가 __init__ 메서드를 직접 사용하지 않고 GenericWorker를 생성하는 또 다른 방법으로 cls를 호출함을 알 수 있음
          * GenericWorker를 구현할 서브클래스는 부모 클래스만 변경하면 됌
          ```python
          class LineCountWorker(GeneicWorker):
              # ...
          ```
        * 마지막으로 mapreduce 함수를 완전히 범용적으로 재작성 하면:
        ```python
        def mapreduce(worker_class, input_class, config):
            workers = worker_class.create_workers(input_class, config)
            return execute(workets)
        ```
        * 다음은 테스트용 파일로 새로운 작업 클래스 객체를 실행한 것: ( 같은결과 나옴, 다른건 mapreduece 함수가 범용적으로 동작하려고 더 많은 파라미터를 요구함)
        ```python
        with TemporaryDirectory() as tmpdir:
            write_test_files(tmpdir)
            config = {'data_dir': tmpdir}
            result = mapreduce(LineCountWorker, PathInputData, config)    
        ```
        * 이제 GenericInputData와 GenericWorker의 다른 서브클래스를 원하는 대로 만들어도 글루코드(glue code)를 작성할 필요가 없음
        
*** 
# 핵심정리
* 파이썬에서는 클래스별로 생성자를 한 개(__init__메서드)만 만들 수 있음
* 클래스에 필요한 다른 생성자를 정의하려면 @classmethod를 사용할 것
* 구체 서브클래스들을 만들고 연결하는 범용적인 방법을 제공하려면 클래스 메서드 다형성을 이용할 것.
