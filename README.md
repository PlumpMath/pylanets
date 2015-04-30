## Note, this is written for python3

# pylanets

```python
from pylanets.highlevel import Empire
from pylanets.highlevel import (reports, goals, resources)

emp = Empire.from_game(111111)

print('Empire resources:')
for k,v in emp.resources()['total'].items():
  print('{} : {}'.format(k,v))
  
print('\nEmpire planets:')
for p in emp.planets():
  print('\t'+str(p))
```

# output

```
Empire resources:
    mc : 43868
    molybdenum : 37437
    neutronium : 53619
    tritanium : 24587
    duranium : 49900
    supplies : 42177

Empire planets:
    Planet(18) [lohec] : Milab, P[2851/10405], M[18/18/18/12]
    Planet(103) [lohec] : Rio Linda, P[1612/88278], M[10097/3900/6757/3715]
    Planet(120) [lohec] : Cattlian, P[1674/0], M[100/534/30/9522]
    Planet(153) [lohec] : Mileb , P[2888/53801], M[571/153/144/78]
    Planet(172) [lohec] : Colony 7, P[1 362/0], M[9630/102/6102/101]
    Planet(180) [lohec] : Libra, P[97018/1354   9], M[6219/4608/1536/353]
    Planet(205) [lohec] : Sirius A, P[14222/1147    84], M[4/45/45/18]
    Planet(218) [lohec] : Anditius, P[1861/0], M[8364/6 828/984/12154]
    Planet(222) [lohec] : Canes Delta, P[153/8637], M[582/3 51/604/687]
    Planet(236) [lohec] : Corona, P[1014/0], M[7879/593/694/68  5]
    Planet(281) [lohec] : Bootes, P[355/49576], M[678/5620/161/381]
    Planet(289) [lohec] : Tarsus, P[100/60088], M[235/5033/654/461]
    Planet(312) [lohec] : Alienation, P[4970/92222], M[36/36/36/27]
    Planet(362) [lohec] : Fresno, P[3145/62048], M[15/55/47/19]
    Planet(383) [lohec] : Holstein, P[269/58025], M[620/406/743/285]
    Planet(420) [lohec] : Shwarts   , P[145/0], M[919/653/400/7026]
    Planet(426) [lohec] : Ceti Alpha 5, P[  65/0], M[874/489/2674/672]
    Planet(443) [lohec] : Cave World, P[1831/64 685], M[737/523/662/456]
    Planet(461) [lohec] : Karelia, P[5986/42600],    M[22/8398/8/16]
    Planet(467) [lohec] : Atlantia 11, P[3819/0], M[9/112   55/788/469]

```
