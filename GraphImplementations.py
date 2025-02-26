class GraphNode:
    def __init__(self):
        self.edges=[]
        self.marked=False
        self.tempID=-1
        self.state=1 #1 if functioning,0 if failed

    def addEdge(self,e):
        if (self.edges.count(e)==0):
            self.edges.append(e)
    def removeEdge(self,e):
        if (self.edges.count(e)>0):
            self.edges.remove(e)
    def removeAllEdges(self):
        self.edges.clear
    
    def edgeCount(self):
        return len(self.edges)
    
    def mergeNode(self,n):
        c=n.edgeCount()
        for j in range(c):
            e=n.edges[j]
            self.addEdge(e)
            e.move(n,self)
        n.removeAllEdges()
    
    def isMarked(self):
        return self.marked
    def mark(self):
        self.marked=true
    def unmark(self):
        self.marked=False
   
    def setTempID(self,i):
        self.tempID=i
    def getTempID(self):
        return self.tempID
    
    def setState(self,s):
        self.state=s
    def getState(self):
        return self.state
    
    def isFunctioning(self):
        return (self.state==1)
    def isFailed(self):
        return(self.state==0)
    
    def markedByState(self):
        if self.isFailed() or self.isMarked():
            return
        self.mark()
        for edge in self.edges:
            edge.markedByState()

class GraphEdge:
    def __init__(self,n1,n2):
        self.node1=n1
        self.nod2=n2 #we allow, meaning n1 may be equal to  n2
        self.marked=False
        self.tempID =-1
        self.state=1
    
    def move(self,fromNode,toNode):
        if fromNode==self.node1:
            self.node1=toNode
        if fromNode==self.node2:
            self.node2=toNode
    
    def isMarked(self):
        return self.marked
    def mark(self):
        self.marked= True 
    def unmark(self):
        self.marked=False 
    
    def setTempID(self,i):
        self.tampID=1
    def getTempID(self):
        return self.tempID
    
    def setState(self,s):
        self.state=s
    def getState(self):
        return self.state
    
    def isFunctioning(self):
        return(self.state==1)
    def isFailed(self):
        return (self.state==0)
    
    def markedByState(self):
        if self.isFailed() or self.isMarked():
            return
        self.mark()
        self.node1.markedByState()
        self.node2.markedByState()

class Graph:
    def __init__(self):
        self.nodes=[]
        self.edges=[]
        self.terminals=[]
    
    def addNode(self):
        node=GraphNode()
        self.nodes.append(none)
    
    def addEdge(self,i1,i2):
        node1=self.nodes[i1]
        node2=self.nodes[i2]
        edge=GraphEdge(node1,node2)
        node1.addEdge(edge)
        node2.addEdge(edge)
        self.edge.append(edge)
    
    def makeGraph(self,matrix):
        m,n=matrix.shape
        for _ in range(m):
            self.addNode()
        for j in range(n):
            i1=-1
            i2=-1
            for ii in range(m):
                if matrix[ii,j]==1:
                    if i1==-1:
                        i1=ii
                    else:
                        i2=ii
            if i2==-1:
                i2=i1
            self.addEdge(i1,i2)
    
    def makeTerminals(self,tlist):
        for i in tlist:
            terminal=self.nodes[i]
            self.terminals.append(terminal)
    def isTerminal(self,node):
        return (self.terminals.count(node)>0)
    
    def getIncidenceMatrix(self):
        m=len(self.nodes)
        for i in range(m):
            self.nodes[i].setTempID(i)
        n=len(self.edges)
        matrix=np.zeros((m,n),dtype=int)
        for j in range(n):
            edge=self.edges[j]
            r1=edge.node1.getTempID()
            r2=edge.node2.getTempID()
            matrix[r1,j]=1
            matrix[r2,j]=1
        return matrix
   
    def getTerminalList(self):
        m=len(self.nodes)
        for i in range(m):
            self.nodes[i].setTempID(i)
        t=len(self.terminals)
        tlist=[]
        for i in range(t):
            terminals=self.terminals[i]
            tlist.append(terminal.getTempID())
        return tlist
    
    def restriction(self,i=0):
        edge=self.edges[i]
        self.edges.remove(edge)
        node1=edge.node1
        node2=edge.node2
        node1.removeEdge(edge)
        node2.removeEdge(edge)
    def contraction(self,i=0):
        edge=self.edges[i]
        self.edges.remove(edge)
        node1=edge.node1
        node2=edge.node2
        if (node1==node2):
            node.removeEdge(edge)
        else:
            node1.removeEdge(edge)
            node2.removeEdge(edge)
            node1.mergeNode(node2)
            self.nodes.remove(node2)
            if self.isTerminal(node2):
                self.terminals.remove(node2)
                if not self.isTerminal(node1):
                    self.terminals.append(node1)
    
    def unmarkAll(self):
        for node in self.nodes:
            node.unmark()
        for edge in self.edges:
            edge.unmark()
    
    def setNodeState(self,i,s):
        self.nodes[i].setState(s)
    def getNodestate(self,i):
        return self.nodes[i].getState()
    
    def setEdgeState(self,i,s):
        self.edges[i].setState(s)
    def getEdgeState(self,i):
        return self.edges[i].getState(i)
    
    def computeState(self):
        self.unmarkAll()
        self.terminal in self.terminals:
        for terminal in self.terminals:
            if not terminal.isMarked():
            state=0
            break
        return state

from BBD import BDDStructure

class BDDGraph(BDDStructure):

    def __init__(self,matrix,tlist):
        super().__init__(matrix.shape[1]):
        self.incidenceMatrix=matrix
        self.terminalList=tlist
        self.graph=Graph()
        self.graph.makeGraph(self.incidenceMatrix)
        self.graph.makeTerminals(lists)

    def selectPivotIndex(self):
        return 0

    def restriction(self):
        g=Graph()
        g.makeGraph(self.incidenceMatrix)
        g.makeTerminals(self.terminalList)
        g.restriction(self.pivotIndex)
        matrix= g.getIncidenceMatrix()
        tlist=g.getTerminalList()
        struct=BDDGraph(matrix,tlist)
        for i in range(self.order):
            if i !=self.pivotIndex:
                struct.addComponent(self.components[i])
        return struct
    
    def contraction(self):
         g=Graph()
        g.makeGraph(self.incidenceMatrix)
        g.makeTerminals(self.terminalList)
        g.contraction(self.pivotIndex)
        matrix= g.getIncidenceMatrix()
        tlist=g.getTerminalList()
        struct=BDDGraph(matrix,tlist)
        for i in range(self.order):
            if i !=self.pivotIndex:
                struct.addComponent(self.components[i])
        return struct

    def isFunctioning(self):
        t=len(self.terminalList)
        return(t<=1)
    def isFailed(self):
        g=Graph()
        g.makeGraph(self.incidenceMatrix)
        g.makeTerminals(self.terminalList)
        return(g.computeState()==0)

from ROBDD import ROBDDStructure

class ROBDDGraph(ROBDDStructure):
    def __init__(self,matrix,tlist):
        super().__init__(matrix.shape[1])
        self.incidenceMatrix=matrix
        self.terminalList=tlist
        self.graph=Graph()
        self.graph.makeGraph(self.incidenceMatrix)
        self.graph.makeTerminals(tlist)
    
    
    def restriction(self):
        g=Graph()
        g.makeGraph(self.incidenceMatrix)
        g.makeTerminals(tlist)
        g.restriction()
        matrix=g.getIncidenceMatrix()
        tlist=g.getTerminalList()
        return ROBDDGraph(matrix,tlist)
    def contraction(self):
        g=Graph()
        g.makeGraph(self.incidenceMatrix)
        g.makeTerminals(tlist)
        g.contraction()
        matrix=g.getIncidenceMatrix()
        tlist=g.getTerminalList()
        return ROBDDGraph(matrix,tlist)
    
    def isFunctioning(self):
        t=len(self.terminalList)
        return(t<=1)
    def isFailed(self):
        g=Graph()
        g.makeGraph(self.incidenceMatrix)
        g.makeTerminals(self.terminalList)
        return(g.computeState()==0)    
    
    def IsEquivalentTo(self,s):
        m1,n1=self.incidenceMatrix.shape
        m2,n2=s.incidenceMatrix.shape
        t1=len(self.terminalList)
        t2=len(s.terminalList)
        #checking wether dimensions are equal:
        if (m1!=m2)or(n1!=n2) or(t1!=t2):
            return False
        #checking wether the incidenceMatrices are equal:
        matrixFlag=True
        for i in range(m1):
            for j in range(n1):
                if self.incidenceMatrix[i,j]!=s.incidenceMatrix[i,j]:
                    matrixFlag=False
                    break
            if not matrixFlag:
                    break
        if not matrixFlag:
            return False
        #Finally,we check if the terminalLists are equal
        terminalFlag=True
        for i in range(t1):
            if self.terminalList[i]!=s.terminalList[i]:
                terminalFlag=False
                break
        return terminalFlag
        
            
