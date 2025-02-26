
class ROBDDSystem:
    def __init__(self,st):
        self.structure=st
        self.order=self.structure.getOrder()
        self.components=[]

        for i in range(self.order):
            comp=ROBDDComponent(self, i)
            self.components.append(comp)
        
        self.root=ROBDDNode(self.components[0],self.structure)
        self.failedNode=ROBDDNode(None,None,nm='D0')
        self.functioningNode=ROBDDNode(None,None,nm='D1')
        
        for i in range(self.order):
            self.components[i].createLeaves()
            if(i+1)<self.order:
                self.components[i+1].simplify()
    
    def getComponent(self,i):
        if i<0:
            return None
        elif i<self.order:
            return self.components[i]
        else:
            return None

    def getRoot(self):
        return self.root
    
    def getFailedNode(self):
        return self.failedNode
    
    def getFunctioningNode(self):
        return self.functioningNode
    #calculate system reliability if all components have equal reliability, rel is the common reliability
    def calcRel0(self,rel):
        self.root.initializeProbability(1)
        for i in range(1,self.order):
            self.components[i].initializeProbability()
        self.failedNode.initializeProbability()
        self.functioningNode.initializeProbability()
        for i in range(self.order):
            self.components[i].propagateProbability(rel)
        return self.failedNode.getProbability(),self.functioningNode.getProbability()
   
    #Calculate reliability for a given vector of component reliabilities

    def calcRel1(self,rv):
        self.root.initializeProbability(1)
        for i in range(1,self.order):
            self.components[i].initializeProbability()
        self.failedNode.initializeProbability()
        self.functioningNode.initializeProbability()
        for i in range(self.order):
            self.components[i].propagateProbability(rv[i])
        return self.failedNode.getProbability(),self.functioningNode.getProbability()
    
    def printSystem(self):
        for i in range(self.order):
            self.components[i].printComponent()


    
class ROBDDComponent:
    def __init__(self,sys,i):
        self.system=sys
        self.index=i
        self.nodes=[]
    
    def getName(self):
        return 'C' +str(self.index)
    
    def getNextComponent(self):
        return self.system.getComponent(self.index+1)
    def getPrevComponent(self):
        return self.system.getComponent(self.index-1)
    
    def getFailedNode(self):
        return self.system.getFailedNode()
    def getFunctioningNode(self):
        return self.system.getFunctioningNode()
    def addNode(self,nd):
        self.nodes.append(nd)
    def removeNode(self,nd):
        self.nodes.remove(nd)
    
    def getNodeIndex(self,nd):
        return self.nodes.index(nd)
    
    def createLeaves(self):
        k=len(self.nodes)
        for j in range(k):
            self.nodes[j].createLeaves()
    def simplify(self):
        if True:
            k1=len(self.nodes)
            for j1 in range(k1-1):
                i1=k1-2-j1
                n1=self.nodes[i1]
                k2=len(self.nodes)
                for j2 in range(k2-i1-1):
                    i2 =k2-1-j2
                    n2=self.nodes[i2]
                    if n1.isEquivalentTo(n2):
                        n1.mergeNode(n2)
    def initializeProbability(self):
        k=len(self.nodes)
        for j in range(k):
            self.nodes[j].initializeProbability()
   
    def propagateProbability(self,rel):
        k=len(self.nodes)
        for j in range(k):
            self.nodes[j].propagateProbability(rel)
    
    def printComponent(self):
        print(self.getName(), '[',sep='', end='')
        k=len(self.nodes)
        for j in range(k):
            self.nodes[j].printNode()
            if j<k-1:
                print(',', sep='',end='')
        print(']')

class ROBDDNode:
    def __init__(self,cp,st,rt=None,nm=''):
        self.component=cp
        if cp!=None:
            self.component.addNode(self)
        self.structure=st
        if rt==None:
            self.roots=None
        else:
            self.roots=[rt]
        self.left=None
        self.right=None
        self.probability=0
        self.name=nm
    
    def getName(self):
        if self.component!=None:
            return 'N' +str(self.component.getNodeIndex(self))
        else:
            return self.name
    def addRoot(self,rt):
        if self.roots==None:
            self.roots=[rt]
        else:
            self.roots.append(rt)
    def replaceSucc(self,old_nd,new_nd):
        if self.left==old_nd:
            self.left=new_nd
        if self.right ==old_nd:
            self.right=new_nd
    
    def isEquivalentTo(self,nd):
        return self.structure.isEquivalentTo(nd.structure)
    
    def mergeNode(self,nd):
        m=len(nd.roots)
        for j in range(m):
            self.addRoot(nd.roots[j])
            nd.roots[j].replaceSucc(nd,self)
        self.structure.mergeStructure(nd.structure)
        self.component.removeNode(nd)
    
    def isRoot(self):
        return(self.roots==None)
    def isLeaf(self):
        return(self.component==None)
    
    def initializeProbability(self,p=0):
        self.probability=p
    def addProbability(self,p):
        self.probability+=p
    def getProbability(self):
        return self.probability

    def createLeaves(self):
        if not self.isLeaf():
            nextComponent=self.component.getNextComponent()
            leftStructure=self.structure.restriction()
            if leftStructure.isFailed():
                self.left=self.component.getFailedNode()
            elif nextComponent !=None:
                self.left =ROBDDNode(nextComponent,leftStructure,self)
            else:
                self.left=self.component.getFailedNode()
            
            rightStructure=self.structure.contraction()
            if rightStructure.isFunctioning():
                self.right=self.component.getFunctioningNode()
            elif nextComponent !=None:
                self.right =ROBDDNode(nextComponent,rightStructure,self)
            else:
                self.right=self.component.getFunctioningNode()
    def propagateProbability(self,p):
        self.left.addProbability(self.probability*(1-p))
        self.right.addProbability(self.probability*p)
    
    def printNode(self):
        if True:
            print(self.getName(), '(',self.getProbability(),')',sep='',end='' )
        else:
            print(self.getName(), '( )',sep=' ',end=' ')

class ROBDDStructure:
    def __init__(self,n):
        self.order=n
    def getOrder(self):
        return self.order
    def restriction(self):
        return 
    def contraction(self):
        pass
    def isFunctioning(self):
        pass
    def isFailed(self):
        pass
    def isEquivalentTo(self,s):
        pass
    def mergeStructure(self,s):
        pass