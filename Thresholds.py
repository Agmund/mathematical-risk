from ROBDD import ROBDDStructure
from BDD import BDDStructure

class BDDThreshold(BDDStructure):
    def __init__(self,w,wsum,th):
        super().__init__(len(w))
        self.weights=w
        self.weightsum=wsum
        self.threshold=th
    def selectPivotIndex(self):
        max_w=-1
        max_i=-1
        for i in range(self.order):
            if self.weights[i]>max_w:
                max_w=self.weights[i]
                max_i=i
        self.pivotIndex=max_i

    def restriction(self):
        w=[]
        for i in range(self.order):
            if i !=self.pivotIndex:
                w.append(self.weights[i])
        wsum=self.weightsum-self.weights[self.pivotIndex]
        struct=BDDThreshold(w,wsum,self.threshold)
        for i in range(self.order):
            if i != self.selectPivotIndex:
                struct=BDDThreshold(w,wsum,self.threshold)
        for i in range(self.order):
            if i !=self.pivotIndex:
                struct.addComponent(self.components[i])
        return struct
    
    def contraction(self):
        w=[]
        for i in range(self.order):
            if i !=self.pivotIndex:
                w.append(self.weights[i])
        wsum=self.weightsum-self.weights[self.pivotIndex]
        struct=BDDThreshold(w,wsum,self.threshold)
        for i in range(self.order):
            if i != self.selectPivotIndex:
                struct=BDDThreshold(w,wsum,self.threshold-self.weights[self.pivotIndex])
        for i in range(self.order):
            if i !=self.pivotIndex:
                struct.addComponent(self.components[i])
        return struct

    def isFunctioning(self):
        return self.threshold <=0
    def isFailed(self):
        return self.threshold>self.weightsum

class ROBDDThreshold(ROBDDStructure):
    def __init__(self,w,wsum,th):
        super().__init__(len(w))
        self.weights=w
        self.weightsum=wsum
        self.threshold=th

    def restriction(self):
        w=[]
        for i in range(1,self.order):
            w.append(self.weights[i])
        wsum=self.weightsum-self.weights[0]
        return(ROBDDThreshold(w,wsum,self.threshold))
    
    def contraction(self):
        w=[]
        for i in range(1,self.order):
            w.append(self.weights[i])
        wsum=self.weightsum-self.weights[0]
        return ROBDDThreshold(w,wsum,self.threshold-self.weights[0])
    
    def isFunctioning(self):
        return self.threshold<=0
    def isFailed(self):
        return self.threshold>self.weightsum

    def isEquivalentTo(self,s):
        return self.threshold == s.threshold
