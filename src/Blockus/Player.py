'''
Created on Nov 27, 2020

@author: ian
'''

import psutil
import time
from enum import Enum
from copy import copy
from random import randint
from  Piece import Piece
from  Square import Color
from  PieceDefinitions import createPieces
from  Board import Board
from Tree import Node


MAX_TIMEOUT = 30 # seconds
MIN_FREE_MEM = 100 * 1024 * 1024 # 100 Megabytes
EXPLORATION_CONSTANT = 0.7
NUM_CORES = 4

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
        self.opponent = None
        self.moveNum = 1
        
    
    def agentMove(self, board, isFirst):
        if (self.agentType == AgentType.HUMAN):
            pass
        
        
        elif (self.agentType == AgentType.MCTS_NORM):
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                move = self.mctsNormal(board)
                if move == None:
                    return None
                return self.makeMove(board, move)
        
        
        
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
    

    def getPiecesNotIn(self, l):
        pieces = []
        for p in self.pieces:
            if p not in l:
                pieces.append(p)
        return pieces
        
    
    
    def playoutRandomGame(self, node):
        whosTurn = node.turnColor.opp() #opposite because turnColor is who moved to make this state
        piecesUsed = copy(node.piecesUsed) #only adding not modifying
        ourMove = -1 # start with not None so loop executed once for sure
        theirMove = -1
        boardCopy = node.state.duplicate()
        #print(boardCopy)
        while(True):
            if whosTurn == self.color:
                useable_pieces = self.getPiecesNotIn(piecesUsed)
                valid_moves = boardCopy.getAllValidMoves(useable_pieces)
                if valid_moves == []:
                    ourMove = None
                else:
                    i = randint(0, len(valid_moves) - 1)
                    ourMove = valid_moves[i]
                    piecesUsed.append(ourMove[0])
                    boardCopy.makeMoveOnBoard(ourMove[1], ourMove[2], ourMove[3])
                    
                whosTurn = whosTurn.opp()
            
            if whosTurn != self.color:
                useable_pieces = self.opponent.getPiecesNotIn(piecesUsed)
                valid_moves = boardCopy.getAllValidMoves(useable_pieces)
                if valid_moves == []:
                    theirMove = None
                else:
                    i = randint(0, len(valid_moves) - 1)
                    theirMove = valid_moves[i]
                    piecesUsed.append(theirMove[0])
                    boardCopy.makeMoveOnBoard(theirMove[1], theirMove[2], theirMove[3])
                    
               
                whosTurn = whosTurn.opp()
                
            if ourMove == None and theirMove == None:
                #game over
                break
        
        ourScore = boardCopy.evaluateScore(self.color)
        theirScore = boardCopy.evaluateScore(self.color.opp())
        #print(boardCopy)
        
        if ourScore > theirScore:
            return 1
        if ourScore < theirScore:
            return 0
        else:
            return 0.5
        
    
    def mctsNormal(self, board):
        root = Node(board, None, None, self.opponent.color)
        # set initial child layer
        initial_moves = board.getAllValidMoves(self.pieces)
        if initial_moves == []:
            return None
        for move in initial_moves:
            b = board.duplicate()
            b.makeMoveOnBoard(move[1], move[2], move[3])
            #consider using piece size as first play urgency as initialVal
            child = Node(b, root, move, self.color, initialVal = move[0].size())
            child.piecesUsed.append(move[0])
            root.addChild(child)
        
        
        num_simulations = 0
        startTime = time.perf_counter()
        while(self.resourcesAvailable(startTime)):
            #selection phase
            currentNode = Node.getMctsLeaf(root)
            #print(currentNode)
           
            
            #expansion phase
            useable_pieces = []
            if currentNode.turnColor == self.color:
                # opponents turn, use their pieces
                useable_pieces = self.opponent.getPiecesNotIn(currentNode.piecesUsed)
                
            else:
                #our turn, use our pieces
                useable_pieces = self.getPiecesNotIn(currentNode.piecesUsed)
            
            
            valid_moves = currentNode.state.getAllValidMoves(useable_pieces)
            if valid_moves == []:
                #game in terminal state for this player
                pass
            else:
                # add all substates
                for move in valid_moves:
                    b = currentNode.state.duplicate()
                    b.makeMoveOnBoard(move[1],move[2],move[3])
                    child = Node(b, currentNode, move, move[0].color)
                    child.piecesUsed += currentNode.piecesUsed
                    child.piecesUsed.append(move[0])
                    currentNode.addChild(child)
            
            #simulation phase
            res = self.playoutRandomGame(currentNode)
            num_simulations += 1
            
            #backpropogate
            currentNode.backpropogate(res)
        
        
        #select move
        node = Node.getMaxFirstLayer(root)
        move = node.move
        #Node.delTree(root)
        print(num_simulations, " simulations executed")
        return move
         

class AgentType(Enum):
    HUMAN = 1
    MCTS_NORM = 2
    MCTS_HEURISTIC_CONST = 3
    MCTS_HEURISTIC_DIFF = 4
    MCTS_ALT = 5
    RANDOM = 6   
    


if __name__ == "__main__":
    t = time.perf_counter()
    board = Board(14)
    playerBlue = Player(Color.BLUE, AgentType.MCTS_NORM)
    playerRed = Player(Color.RED, AgentType.RANDOM)
    playerBlue.opponent = playerRed
    playerRed.opponent = playerBlue
    
    playerBlue.agentMove(board, True)
    redm = playerRed.agentMove(board, True)
    print(board)
    playerBlue.agentMove(board, False)
    print(board)
    t2 = time.perf_counter()
    print("program time:", t2-t)
    print(Board.TIME_IN_VALID, " seconds in valid")
    print(Board.TIME_IN_DUP, " seconds in dup")
    
   
#     for i in range(100):
#         print(playerBlue.playoutRandomGame(node))




    
    
    