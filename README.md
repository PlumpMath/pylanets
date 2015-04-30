# pylanets

```python
from pylanets.highlevel import Empire
from pylanets.highlevel import (reports, goals, resources)

emp = Empire.from_game(111111)

print('Empire resources:')
for k,v in emp.resources()['total'].items():
  print('{} : {}'.format(k,v))
  
print('Empire planets:')
for p in emp.planets():
  print(p)
```

# output

```

```
