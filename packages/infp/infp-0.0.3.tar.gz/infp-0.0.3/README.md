# Infinite Precision
Adding big big number!!

# Usage

```python
from infp import BigNumber

num1 = BigNumber("1648976548.65498")
num2 = BigNumber("-4564984945.654")
sum = num1 + num2       # -2916008396.99902
print(sum)      
num1 = BigNumber("10")
num2 = BigNumber("10")
sub = num1 - num2
print(sub)              # 0
ans = BigNumber("132") / BigNumber("132")
print(ans)              # 1

```

# Unit Test

* Install pytest if haven't

```
pip install pytest
```

* Run test command

```
pytest
```

# Run the main program example
```
python main.py
```