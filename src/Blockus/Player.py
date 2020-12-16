'''
Created on Nov 27, 2020

@author: ian
'''
from enum import Enum
from random import randint
from Blockus.PieceDefinitions import createPieces
from Blockus.Board import Board


    


        

class Player():
    '''
    Represents a player, and holds algorithms to play or is a human
    '''


    def __init__(self, color, agentType):
        self.color = color
        self.agentType = agentType
        self.pieces = createPieces(self.color)
        
    
    def move(self, board):
        if (self.agentType == AgentType.HUMAN):
            pass
        elif (self.agentType == AgentType.MCTS_NORM):
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_CONST):
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_DIFF):
            pass
        elif (self.agentType == AgentType.RANDOM):
            move = self.selectRandomMove(board)
            pass
        else:
            print("unknown agent type, making random move")

    
    def makeMove(self, board, move):
        pass
    
    
    def selectRandomMove(self, board):
        valid_moves = board.getAllValidMoves(self.pieces)
        # cannot make a move
        if valid_moves == []:
            return None
        idx = randint(0, len(valid_moves))
        return valid_moves(idx)
        

class AgentType(Enum):
    HUMAN = 1
    MCTS_NORM = 2
    MCTS_HEURISTIC_CONST = 3
    MCTS_HEURISTIC_DIFF = 4
    MCTS_ALT = 5
    RANDOM = 6   
    


if __name__ == "__main__":
    print(randint(0,3))




    
    
    