from BDD import BDDSystem
from ROBDD import ROBDDSystem
from ConsecutiveThreshold import BDDConsecutiveThreshold,ROBDDConsecutiveThreshold

p=0.5
a=[8,7,6,5,3,2]
b=10
s0=0
n=len(a)

wsum=0
for wg in a:
    wsum+=wg

sys=BDDSystem(BDDConsecutiveThreshold(a,wsum,s0,b))
result=sys.calcRel0(p)
sys.printSystem()

print("")
print("---------")
print("BDD-method:")
print('System unreliability=',result[0])
print('System reliability=',result[1])

print("")
print("--------------")
print("")

sys=ROBDDSystem(ROBDDConsecutiveThreshold(a,wsum,s0,b))
result=sys.calcRel0(p)
sys.printSystem()

print("")
print("---------")
print("ROBDD-method:")
print('System unreliability=',result[0])
print('System reliability=',result[1])
