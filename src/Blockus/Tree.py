'''
Created on Dec 19, 2020

@author: ian
'''

from math import log,sqrt
from copy import copy

'''
MCTS tree node
'''
class Node():
    

    '''
    Picks path with highest ucb_value, returns highest val leaf along that path
    '''
    @staticmethod
    def getMctsLeaf(root):
        root.visits += 1 
        if root.children == []:
            return root
        max = float('-inf')
        maxChild = None
        for child in root.children:
            if child.ucb_val > max:
                max = child.ucb_val
                maxChild = child
        return Node.getMctsLeaf(maxChild)

    @staticmethod
    def getMaxFirstLayer(root):
        max = float('-inf')
        maxChild = None
        for child in root.children:
            #print(child)
            if child.ucb_val > max and child.visits > 0:
                max = child.ucb_val
                maxChild = child
        return maxChild
    
#     @staticmethod
#     def delTree(root):
        
        
    
    '''
    Constructor
    '''
    def __init__(self, move, parent, turnColor, initialVal=float('inf')):
        if parent != None:
            self.moveStack = copy(parent.moveStack).append(move)
        else:
            self.moveStack = []
        if self.moveStack == None:
            self.moveStack = [move]
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.turnColor = turnColor # denotes who made the move to get to this moveStack
        self.ucb_val = initialVal
    
    def addChild(self, child):
        self.children.append(child)
        
    def calculateUCB(self):
        if self.visits == 0:
            self.ucb_val = float('inf')
            return
        winP = self.wins/self.visits
        explore = sqrt((2 * log(self.parent.visits)) / self.visits)
        self.ucb_val = winP + explore
        
    
    def backpropogate(self, res):
        self.wins += res
        for child in self.children:
            if child.visits > 0:
                child.calculateUCB()
        if self.parent == None:
            return
        else:
            self.parent.backpropogate(res)
    
    
        
    def __str__(self):
        s = ""
        s += str(self.moveStack[-1][1]) 
        s+= "\n"
        s += "visits:{}, wins:{}".format(self.visits, self.wins)
        s += "val"
        return s
    

        
    
if __name__ == "__main__":
    n = Node(None,None,None,None)
    n.C = 6
    x = Node(None,None,None,None)
    x.C = 9
    print(x.C, n.C)
#     root = Node(0,None,None)
#     for i in range(1, 101):
#         n = Node(i, root, None)
#         n.ucb_val = i
#         for x in range(0,101):
#             nc = Node(i+x, n, None)
#             nc.ucb_val = 2*x + i
#             n.addChild(nc)
#         root.addChild(n)
#         
#     root.children[56].ucb_val = 1000
#     c = Node.getMctsLeaf(root)
#     print(c.ucb_val)
#     print(float('inf') > float('inf'))    