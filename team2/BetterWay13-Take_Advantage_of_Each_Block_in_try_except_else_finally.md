
Better Way 13 try/except/else/finally에서 각 블록의 장점을 이용하자 
======================================
예외 처리와 관련된 4가지 구문
***
# finally 블록
* 예외를 전달하고 싶지만, 예외가 발생해도 정리 코드를 실행하고 싶을 때 try/finally
* 파일 핸들러 종료 코드를 실행시키는 작업을 할 수 있음
```python
handle = open('temp/randomdata.txt') # IOError 가 날 수도 있삼
try : 
    data = handle.read() #UnicideDecodeError 가 날 수도 있삼
finally : 
    handle.close() # try: 문 후에 반드시 항상 실행됨
```
* 위에서, read() 메소드에서 발생한 에러는 호출 코드까지 전달됨. close() 메소드는 finally: 문에서 반드시 실행됨. 
* 한편 open() 메소드에서 일어난 에러는 finally 블록에서 처리하지 않아야 하며, 그래서 try 블록 전에 작성해 둠
 # else 블록
* 어떤 예외를 처리하고 또 전달할지 명백하게 작성하기 위해서는 try/except/else 블록을 사용하면 됨.
* try 블록이 예외를 일으키지 않으면 else 블록이 실행됨. else 문을 통해서 try 블록의 코드를 줄이고 가독성을 높인다. 
* JSON 딕셔너리 데이터 읽고 어쩌고 예제
```python
def load_json_key(data,key): 
    try:
        result_dict = json.loads(data)  #ValueError 가 날수도 있삼
    except ValueError as e :
        raise keyError from e 
    else: 
        return result_dict[key]         # KeyError 가 날 수도 있음
```
* 데이터가 올바른 JSON 이 아니라면? 
  * json.loads 로 디코드 되다 말고 ValueError 가 일어나며 except 블록에서 잘 처리됨 
* 올바른 JSON 이라서 디코딩이 잘 되면...! 
  * 그러면 else 블록이 시행이 되며 키를 찾는다. 그런데 key 찾다가도 예외가 날 수도 있고, 그 예외는 try 밖에 있으므로 호출 코드까지 전달이 됨 
* else 절을 사용하면 try/except 문 다음에 나오는 처리를 시각적으로 except 와 구분해주고, 그러므로 예외전달이 명확해진다. 
  # 모두 함께 사용하기 
* 파일에서 수행할 작업 설명을 읽고 처리한 후 즉석에서 파일을 업데이트한다고 하자. 
  * try : 파일 읽고 처리
  * except : try 에서 일어난 예외를 처리 
  * else : 파일 업데이트, 예외 전달 
  * finally : 파일 핸들 정리 
```python
UNDEFINED = object() 

def divide_json(path): 
    handle = open(path, 'r+')       #IOError? 
    try:
        data = handle.read()        #UnicodeDecodeError?
        op = json.loads(data)       #ValueError?
        value = (
            op['numerator']/
            op['denominator']       #ZeroDivisionError? 
    except ZeroDivisionError as e:
        return UNDEFINED 
    else: 
        op['result'] = value 
        result = json.dumps(op) 
        handle.seek(0) 
        handle.write(result)        #IOError?
        return value
    finally: 
        handle.close()              # 항상 실행, else 블록에서 오류가 나더라도요
```

요약 
* try/finally 복합문을 이용하면 try 블록에서 예외가 발생하든 말든 정리코드를 실행시킬수 있다
* else 블록은 try 블록에 있는 코드 양을 최소화할 수 있고, try/except 블록 과 성공시 실행할 코드를 분리해준다 
* else 블록은 또한 try 와 finally 사이에 수행할 추가작업을 위해 사용할 수도 있다.
