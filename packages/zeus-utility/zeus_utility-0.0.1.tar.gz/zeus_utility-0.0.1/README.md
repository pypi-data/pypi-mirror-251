# Zeus's Utility

## Features
- [x] Parallel Execute

## Quick Usage:
### Install:
```shell
pip install zeus-utility
# or 
pip install git+https://github.com/zeuscsc/zeus_utility.git
```
### Usage
```python
def print_a_plus_b(a,b):
    print(a+b)
queue=[]
for i in range(10):
    queue.append((print_a_plus_b,{"a":i,"b":i}))
execute_queue

```