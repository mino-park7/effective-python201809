# 1. 사용중인 파이썬의 버전을 알자

* python 명령어는 보통 python2.7을 가리키지만 때때로 2.6, 2.5를 가르킬 수도 있기 때문에, --version 플래그를 사용하여 버전 확인하자

```bash
$ python --version
Python 2.7.8
```

* 파이썬3은 보통 python3으로 실행

```bash
$ python3 --version
Python 3.5.2
```

* 파이썬에 내장된 sys 모듈을 이용하여 파이썬의 버전을 알아낼 수도 있음

```python
import sys
print(sys.version_info)
print(sys.version)

>>>
sys.version_info(major=3, minor=4, micro=2, releaselevel='final', serial=0)
3.4.2 (default, ....
```

* 파이썬 2와 3 모두 커뮤니티에서 유지보수 되는중
  * 파이썬 2의 개발은 버그 수정, 보안 강화, 2를 3으로 쉽게 포팅하는 기능 이외에는 중지됨
  * 2to3, six 와 같은 module을 사용하면 파이썬 3과 호환이 쉬워짐
* 파이썬 3은 새 기능과 향상이 지속적으로 이루어짐.
* 새로 프로젝트를 실행한다면 파이썬 3 사용을 적극 추천

---
* **핵심정리**
  * 파이썬의 주요 버전인 파이썬2, 3 모두 활발히 사용됨
  * 파이썬에는 CPython, Jython, IronPython, PyPy 같은 다양한 런타임이 존재함
  * 시스템에서 파이썬을 실행하는 명령이 사용하고자 하는 파이썬 버전인지 확이 필요
  * 파이썬 3 추천

