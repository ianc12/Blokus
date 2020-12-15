'''
Created on Nov 27, 2020

@author: ian
'''
from enum import Enum
from Blockus.Piece import Piece
from Blockus.PieceDefinitions import createPieces

class Player():
    '''
    Represents a player, and holds algorithms to play or is a human
    '''


    def __init__(self, color, agentType):
        self.color = color
        self.agentType = agentType
        self.pieces = createPieces(self.color)
    
    def move(self):
        if (self.agentType == AgentType.HUMAN):
            pass
        elif (self.agentType == AgentType.MCTS_NORM):
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_CONST):
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_DIFF):
            pass
        elif (self.agentType == AgentType.RANDOM):
            pass
        else:
            print("unknown agent type, making random move")

    



















class AgentType(Enum):
    HUMAN = 1
    MCTS_NORM = 2
    MCTS_HEURISTIC_CONST = 3
    MCTS_HEURISTIC_DIFF = 4
    RANDOM = 5
    
    
    
    