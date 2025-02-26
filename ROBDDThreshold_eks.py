from ROBDD import ROBDDSystem
from Thresholds import ROBDDThreshold

p=0.5
a=[12,11,8,7,6,5,3,2]
b=30
n=len(a)
wsum=0
for wg in a:
    wsum+=wg
sys=ROBDDSystem(ROBDDThreshold(a,wsum,b))
result=sys.calcRel0(p)
sys.printSystem()
print('')
print('System unreliability=',result[0])
print('System reliability=',result[1])