'''
Created on Dec 15, 2020

@author: ian
'''

class Node():
    def __init__(self, state):
        self.state = state
        self.nodeValue = 0
        self.visits = 0
        self.simWins = 0
        self.simTies = 0
        self.simLosses = 0
        self.children = []


class Tree():
    
    '''
    Constructor
    '''
    def __init__(self, initialState):
        self.root = Node(initialState)
        
        
        