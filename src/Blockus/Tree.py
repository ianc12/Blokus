'''
Created on Dec 19, 2020

@author: ian
'''

class Node():
    '''
    classdocs
    '''
    @staticmethod
    def getMctsLeaf(root):
        if root.children == []:
            return root
        max = float('-inf')
        maxChild = None
        for child in root.children:
            if child.ucb_val > max:
                max = child.ucb_val
                maxChild = child
        return Node.getMctsLeaf(maxChild)


    '''
    Constructor
    '''
    def __init__(self, state, parent, move, initialVal=float('inf')):
        self.state = state
        self.parent = parent
        self.children = []
        self.move = move
        self.wins = 0
        self.visits = 0
        self.piecesUsed = []
        self.oppPiecesUsed = []
        self.ucb_val = initialVal
    
    def addChild(self, child):
        self.children.append(child)
        
    def calculateUCB(self):
        pass
    
    
if __name__ == "__main__":
    root = Node(0,None,None)
    for i in range(1, 101):
        n = Node(i, root, None)
        n.ucb_val = i
        for x in range(0,101):
            nc = Node(i+x, n, None)
            nc.ucb_val = 2*x + i
            n.addChild(nc)
        root.addChild(n)
        
    root.children[56].ucb_val = 1000
    c = Node.getMctsLeaf(root)
    print(c.ucb_val)
    print(float('inf') > float('inf'))    