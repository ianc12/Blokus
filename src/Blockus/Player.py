'''
Created on Nov 27, 2020

@author: ian
'''
from enum import Enum
from random import randint
from  Piece import Piece
from  Square import Color
from  PieceDefinitions import createPieces
from  Board import Board


    


        

class Player():
    '''
    Represents a player, and holds algorithms to play or is a human
    '''


    def __init__(self, color, agentType):
        self.color = color
        self.agentType = agentType
        self.pieces = createPieces(self.color)
        
    
    def agentMove(self, board, isFirst):
        if (self.agentType == AgentType.HUMAN):
            pass
        elif (self.agentType == AgentType.MCTS_NORM):
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_CONST):
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_DIFF):
            pass
        elif (self.agentType == AgentType.RANDOM):
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                m = self.selectRandomMove(board)
                if m is None:
                    return None
                return self.makeMove(board, m)
        else:
            print("unknown agent type, making random move")
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                m = self.selectRandomMove(board)
                if m is None:
                    return None
                return self.makeMove(board, m)

    
    #move in form (piece, permutation, x, y)
    def makeMove(self, board, move):
        board.makeMoveOnBoard(move[1], move[2], move[3])
        self.pieces.remove(move[0])
        return move[0]
        
    
    #TODO: add extra 5 if last piece is single square and played all pieces
    def evaluateScore(self, board):
        score = board.evaluateScore(self.color)
        print(self.color, ": {} Tiles Played".format(score))
        if len(self.pieces) == 0:
            #15 bonus points if you play all pieces
            score += 15
        else:
            for p in self.pieces:
                #subtract size of any pieces leftover
                score -= len(p.points)
                
        return score
                
    
    # select a random move out of the size 5 pieces to begin the game
    def makeRandomFirstMove(self, board):
        fives = []
        for p in self.pieces:
            if len(p.points) == 5:
                fives.append(p)
        while(True):
            i = randint(0, len(fives) - 1)
            p = fives[i]
            for perm in p.permutations:
                if self.color == Color.RED:
                    #TODO: investigate disadvantage for RED or elimintate based on center control
                    if board.makeFirstMove(perm, board.size - 5, board.size - 5):
                        self.pieces.remove(p)
                        print("GLHF!")
                        return p
                else:
                    if board.makeFirstMove(perm, 4, 4):
                        self.pieces.remove(p)
                        print("GLHF!")
                        return p
             
            
    
    def selectRandomMove(self, board):
        valid_moves = board.getAllValidMoves(self.pieces)
        if valid_moves == []:
            # cannot make a move
            return None
        idx = randint(0, len(valid_moves) - 1)
        return valid_moves[idx]
        

class AgentType(Enum):
    HUMAN = 1
    MCTS_NORM = 2
    MCTS_HEURISTIC_CONST = 3
    MCTS_HEURISTIC_DIFF = 4
    MCTS_ALT = 5
    RANDOM = 6   
    


if __name__ == "__main__":
    pass




    
    
    