from BDD import BDDSystem
from Thresholds import BDDThreshold


#eksempel 1 treshold

p=0.5#comp. rel.
a=[12,11,8,7,6,5,3,2]#comp. wheights
b=30#threshold
n=len(a)
wsum=0#sum of weights
for wg in a:
    wsum+=wg

sys=BDDSystem(BDDThreshold(a,wsum,b))

result=sys.calcRel0(p)

sys.printSystem()
print('')
print('System unreliability=',result[0])
print('System reliability=',result[1])


