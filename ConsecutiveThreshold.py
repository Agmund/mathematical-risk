from BDD import BDDStructure
from ROBDD import ROBDDStructure

class BDDConsecutiveThreshold(BDDStructure):
    def __init__(self,w,wsum,s0,th):
        super().__init__(len(w))
        self.weights=w
        self.weightsum=wsum
        self.initialvalue=s0
        self.threshold=th
    
    def selectPivotIndex(self):
        return 0
    
    def restriction(self):
        w=[]
        for i in range(1,self.order):
            w.append(self.weights[i])
        struct=BDDConsecutiveThreshold(w,self.weightsum-self.weights[0],0,self.threshold)
        for i in range(1,self.order):
            struct.addComponent(self.components[i])
        return struct
    def contraction(self):
        w=[]
        for i in range(1,self.order):
            w.append(self.weights[i])
        struct=BDDConsecutiveThreshold(w,self.weightsum-self.weights[0],self.initialvalue+self.weights[0],self.threshold)
        for i in range(1,self.order):
            struct.addComponent(self.components[i])
        return struct

    def isFunctioning(self):
        return self.threshold<=self.initialvalue
    def isFailed(self):
        return self.threshold>self.weightsum+self.initialvalue

class ROBDDConsecutiveThreshold(ROBDDStructure):
    def __init__(self,w,wsum,s0,th):
        super().__init__(len(w))
        self.weights=w
        self.weightsum=wsum
        self.initialvalue=s0
        self.threshold=th
    
    def selectPivotIndex(self):
        return 0
    
    def restriction(self):
        w=[]
        for i in range(1,self.order):
            w.append(self.weights[i])
        struct=ROBDDConsecutiveThreshold(w,self.weightsum-self.weights[0],0,self.threshold)
        return struct
    def contraction(self):
        w=[]
        for i in range(1,self.order):
            w.append(self.weights[i])
        struct=ROBDDConsecutiveThreshold(w,self.weightsum-self.weights[0],self.initialvalue+self.weights[0],self.threshold)
        return struct

    def isFunctioning(self):
        return self.threshold<=self.initialvalue
    def isFailed(self):
        return self.threshold>self.weightsum+self.initialvalue
    def isEquivalentTo(self,s):
        return self.initialvalue==s.initialvalue