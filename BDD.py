
class BDDSystem:
    def __init__(self,st):
        self.structure=st
        self.order=self.structure.order
        self.components =[]
        for i in range(self.order):
            comp=BDDComponent(self,i)
            self.components.append(comp)
            self.structure.addComponent(comp)
        self.levels=[]
        for i in range(self.order):
            lvl=BDDLevel(self,i)
            self.levels.append(lvl)
        
        self.root=BDDNode(self.levels[0],st)
        self.levels[0].addNode(self.root)
        self.failedNode=BDDNode(None,None,nm='D0')
        self.functioningNode=BDDNode(None,None,nm='D1')
        for i in range(self.order):
            self.levels[i].createLeaves()
    
    
    def getLevel(self,i):
        if i<0:
            return None
        elif i<self.order:
            return self.levels[i]
        else:
            return None
    
    def getRoot(self):
        return self.root

    def getFailedNode(self):
        return self.failedNode
    
    def getFunctioningNode(self):
        return self.functioningNode

    #Calculate reliability when all components have equal reliability
    def calcRel0(self,p):
        for i in range(self.order):
            self.components[i].setProbability(p)
        
        self.root.initializeProbability(1)
        
        for i in range(1,self.order):
            self.levels[i].initializeProbability()
        
        self.failedNode.initializeProbability()
        self.functioningNode.initializeProbability()
      
        
        for i in range(1,self.order):
            self.levels[i].propagateProbability()
        
        return self.failedNode.getProbability(),self.functioningNode.getProbability()
    
    #Calculate reliability for a given vector of component reliabilities 
    #rv=The vector of component reliabilities

    def calcRel1(self,rv):
        
        self.root.initializeProbability(1)
        for i in range(self.order):
            self.components[i].setProbability(rv[i])
        for i in range(1,self.order):
            self.levels[i].initializeProbability()
        
        self.failedNode.initializeProbability()
        self.functioningNode.initializeProbability()
        
        
        for i in range(1,self.order):
            self.levels[i].propagateProbability()
        
        return self.failedNode.getProbability(),self.functioningNode.getProbability()
    
    def printSystem(self):
        for i in range(self.order):
            self.levels[i].printLevel()

class BDDLevel:
    def __init__(self,sys,i):
        self.system=sys
        self.index=i
        self.nodes=[]
    
    def getName(self):
        return 'L' +str(self.index)
    
    def getNextLevel(self):
        return self.system.getLevel(self.index+1)
    
    def getPrevLevel(self):
        return self.system.getLevel(self.index-1)
    
    def getFailedNode(self):
        return self.system.getFailedNode()
    
    def getFunctioningNode(self):
        return self.system.getFunctioningNode()
    
    def addNode(self,nd):
        self.nodes.append(nd)
    
    def getNodeIndex(self,nd):
        return self.nodes.index(nd)
    
    def createLeaves(self):
        k= len(self.nodes)
        for j in range(k):
            self.nodes[j].createLeaves()
    
    def initializeProbability(self):
        k=len(self.nodes)
        for j in range(k):
            self.nodes[j].initializeProbability()
    
    def propagateProbability(self):
        k=len(self.nodes)
        for j in range(k):
            self.nodes[j].propagateProbability()
    
    def printLevel(self):
        print(self.getName(), '[',sep='',end='')
        k=len(self.nodes)
        for j in range(k):
            self.nodes[j].printNode()
            if j<k-1:
                print(', ', sep='', end='')
        print(']')

class BDDComponent:
    def __init__(self,sys,i):
        self.system=sys
        self.index=i
        self.probability=0
    def getName(self):
        return 'C'+str(self.index)
    def setProbability(self,p):
        self.probability=p
    def getProbability(self):
        return self.probability
    
class BDDNode:
    def __init__(self,lv,st,rt=None,nm=''):
        self.level=lv
        self.structure=st
        self.root=rt
        if self.structure !=None:
            self.component=self.structure.getPivotComponent()
        else:
            self.component=None
        self.left=None
        self.right=None
        self.name=nm
        self.probability=0
    
    def getName(self):
        if self.level !=None:
            return 'N' + str(self.level.getNodeIndex(self))
        else:
            return self.name
        
    def isRoot(self):
        return(self.root==None)
    def isLeaf(self):
        return(self.level==None)
    
    def initializeProbability(self,p=0):
        self.probability=p
    
    def addProbability(self,p):
        self.probability+=p
    
    def getProbability(self):
        return self.probability
    
    def createLeaves(self):
        if not self.isLeaf():
            nextLevel=self.level.getNextLevel()
            leftStructure=self.structure.restriction()
            
            if leftStructure.isFailed():
                self.left=self.level.getFailedNode()
            elif nextLevel != None:
                self.left= BDDNode(nextLevel,leftStructure,self)
                nextLevel.addNode(self.left)
            else:
                self.left=self.level.getFailedNode()
            
            rightStructure=self.structure.contraction()

            if rightStructure.isFunctioning():
                self.right=self.level.getFunctioningNode()
            elif nextLevel!=None:
                self.right=BDDNode(nextLevel,rightStructure,self)
                nextLevel.addNode(self.right)
            else:
                self.right=self.level.getFunctioningNode()
    
    def propagateProbability(self):
        if self.component!=None:
            p=self.component.getProbability()
            self.left.addProbability(self.probability *( 1-p))
            self.right.addProbability(self.probability * p)
    def printNode(self):
        if True:
            print(self.getName(), '(',self.getProbability(),')',sep='',end='')
        else:
            print(self.getName(), '()', sep='', end='')

class BDDStructure:
    def __init__(self,n):
        self.order=n
        self.pivotIndex=0
        self.components=[]
    def addComponent(self,comp):
        self.components.append(comp)
    def getPivotComponent(self):
        self.selectPivotIndex()
        return self.components[self.pivotIndex]
    
    def selectPivotIndex(self):
        pass
    def restriction(self):
        pass
    def contraction(self):
        pass
    def isFunctioning(self):
        pass
    def isFailed(self):
        pass



