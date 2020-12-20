'''
Created on Nov 27, 2020

@author: ian
'''
from enum import Enum
import psutil
import time
from random import randint
from  Piece import Piece
from  Square import Color
from  PieceDefinitions import createPieces
from  Board import Board
from Tree import Node


MAX_TIMEOUT = 30 # seconds
MIN_FREE_MEM = 100 * 1024 * 1024 # 100 Megabytes
EXPLORATION_CONSTANT = 0.7 

class Player():
    '''
    Represents a player, and holds algorithms to play or is a human
    '''
    
    
    @staticmethod
    def selectRandomMove(self, board, pieceList):
        valid_moves = board.getAllValidMoves(pieceList)
        if valid_moves == []:
            # cannot make a move
            return None
        idx = randint(0, len(valid_moves) - 1)
        return valid_moves[idx]

    
    @staticmethod
    def resourcesAvailable(start):
        t = time.perf_counter()
        if (t > (start + MAX_TIMEOUT)):
            return False
        mem = psutil.virtual_memory()
        if mem.available <= MIN_FREE_MEM:
            return False
        
        return True


    def __init__(self, color, agentType):
        self.color = color
        self.agentType = agentType
        self.pieces = createPieces(self.color)
        self.oppnent = None
        self.moveNum = 1
        
    
    def agentMove(self, board, isFirst):
        if (self.agentType == AgentType.HUMAN):
            pass
        elif (self.agentType == AgentType.MCTS_NORM):
            move = self.mctsNormal(board)
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_CONST):
            pass
        elif (self.agentType == AgentType.MCTS_HEURISTIC_DIFF):
            pass
        elif (self.agentType == AgentType.RANDOM):
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                m = Piece.selectRandomMove(board, self.pieces)
                if m is None:
                    return None
                return self.makeMove(board, m)
        else:
            print("unknown agent type, making random move")
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                m = Piece.selectRandomMove(board, self.pieces)
                if m is None:
                    return None
                return self.makeMove(board, m)

    
    #move in form (piece, permutation, x, y)
    def makeMove(self, board, move):
        board.makeMoveOnBoard(move[1], move[2], move[3])
        self.pieces.remove(move[0])
        self.moveNum += 1
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
                        self.moveNum += 1
                        print("GLHF!")
                        return p
                else:
                    if board.makeFirstMove(perm, 4, 4):
                        self.pieces.remove(p)
                        print("GLHF!")
                        self.moveNum += 1
                        return p
             
            
    

    
    
    def trim(self, root, f):
        pass
    

    
    def playoutRandomGame(self, board):
        #starts by assuming we have just made a move
        
    
    def mctsNormal(self, board):
        root = Node(board, None, None)
        # set initial child layer
        initial_moves = board.getAllValidMoves(self.pieces)
        if initial_moves == []:
            return None
        for move in initial_moves:
            b = board.duplicate()
            b.makeMoveOnBoard(move)
            #consider using piece size as first play urgency as initialVal
            child = Node(b, root, move)
            child.piecesUsed.append(move[0])
            root.addChild(child)
        root.visits += 1
        
        startTime = time.perf_counter()
        while(self.resourcesAvailable(startTime)):
            #selection phase
            currentNode = root.getMctsLeaf()
            
            #expansion phase
            #opponent must make a move before we caluclate the possible moves
            opp_useable_pieces = []
            for piece in self.opponent.pieces:
                if piece not in currentNode.oppPiecesUsed:
                    opp_useable_pieces.append(piece)
            
            opp_move
            
            useable_pieces = []
            for piece in self.pieces:
                if piece not in currentNode.piecesUsed:
                    useable_pieces.append(piece)
            
            
            valid_moves = currentNode.state.getAllValidMoves(useable_pieces)
            if valid_moves == []:
                #game in terminal state for this player
                pass
            else:
                # add all substates
                for move in valid_moves:
                    b = currentNode.state.duplicate()
                    b.makeMoveOnBoard(move)
                    child = Node(b, currentNode)
                    child.piecesUsed += currentNode.piecesUsed
                    child.piecesUsed.append(move[0])
                    currentNode.addChild(child)
            #simulation phase
            self.playoutRandomGame(currentNode.state)
                
        
        #select move
        
         

class AgentType(Enum):
    HUMAN = 1
    MCTS_NORM = 2
    MCTS_HEURISTIC_CONST = 3
    MCTS_HEURISTIC_DIFF = 4
    MCTS_ALT = 5
    RANDOM = 6   
    


if __name__ == "__main__":
    pass




    
    
    