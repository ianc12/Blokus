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


MAX_TIMEOUT = 5 # seconds
MIN_FREE_MEM = 100 * 1024 * 1024 # 100 Megabytes
EXPLORATION_CONSTANT = 0.7
NUM_CORES = 4
KEEP_MOVES = 20

class Player():
    '''
    Represents a player, and holds algorithms to play or is a human
    '''
    
    @staticmethod
    def heuristicPre16(points, ourCorners, theirCorners):
        return (points * 1.5) + (ourCorners * 1.5) + (theirCorners * .5)
    
    @staticmethod
    def heuristicPost16(points, ourCorners, theirCorners):
        return (points * .75)+ (2 * ourCorners)  + (3 * theirCorners) 
    
    
    @staticmethod
    def selectRandomMove(board, pieceList):
        valid_moves = board.getAllValidMoves(pieceList)
        if valid_moves == []:
            # cannot make a move
            return None
        idx = randint(0, len(valid_moves) - 1)
        return valid_moves[idx]

    



    def __init__(self, color, agentType, thinkTime):
        self.color = color
        self.agentType = agentType
        self.pieces = createPieces(self.color)
        self.opponent = None
        self.thinkTime = thinkTime
        self.moveNum = 1
        
    
    
    def resourcesAvailable(self, start):
        t = time.perf_counter()
        if (t > (start + self.thinkTime)):
            return False
        mem = psutil.virtual_memory()
        if mem.available <= MIN_FREE_MEM:
            return False
        
        return True
    
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
        
        
        elif (self.agentType == AgentType.MCTS_HEURISTIC_FIRST):
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                move = None
                if self.moveNum < 16:
                    move = self.mctsHeuristicFirst(board, Player.heuristicPre16)
                else:
                    move = self.mctsHeuristicFirst(board, Player.heuristicPost16)
                if move == None:
                    return None
                return self.makeMove(board, move)
        
        elif (self.agentType == AgentType.MCTS_HEURISTIC_ALWAYS):
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                move = None
                if self.moveNum < 16:
                    move = self.mctsHeuristicAlways(board, Player.heuristicPre16)
                else:
                    move = self.mctsHeuristicAlways(board, Player.heuristicPost16)
                if move == None:
                    return None
                return self.makeMove(board, move)
       
        
        elif (self.agentType == AgentType.RANDOM):
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                m = Player.selectRandomMove(board, self.pieces)
                if m is None:
                    return None
                return self.makeMove(board, m)
        else:
            print("unknown agent type, making random move")
            if isFirst:
                return self.makeRandomFirstMove(board)
            else:
                m = Player.selectRandomMove(board, self.pieces)
                if m is None:
                    return None
                return self.makeMove(board, m)

    
    #move in form (piece, permutation, x, y)
    def makeMove(self, board, move):
        board.makeMoveOnBoard(move)
        self.pieces.remove(move[0])
        self.moveNum += 1
        return move[0]
        
    
    #TODO: add extra 5 if last piece is single square and played all pieces
    def evaluateScore(self, board):
        score = board.evaluateScore(self.color)
        #print(self.color, ": {} Tiles Played".format(score))
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
                    if board.makeFirstMove((p, perm, board.size - 6, board.size - 6) ):
                        self.pieces.remove(p)
                        self.moveNum += 1
                        #print("GLHF!")
                        return p
                else:
                    if board.makeFirstMove((p,perm, 4, 4)):
                        self.pieces.remove(p)
                        #print("GLHF!")
                        self.moveNum += 1
                        return p
             
            
    

    
    
    def trim(self, board, moves, f):
        scoredMoves = []
        initRedCorners = board.evaluateCorners(Color.RED)
        initBlueCorners = board.evaluateCorners(Color.BLUE)
        for move in moves:
            board.makeMoveOnBoard(move)
            postRedCorners = board.evaluateCorners(Color.RED)
            postBlueCorners = board.evaluateCorners(Color.BLUE)
            points = move[0].size()
            score = 0
            if move[0].color == Color.RED:
                #in form points, ourcorners, theircorners
                score = f(points, postRedCorners - initRedCorners, initBlueCorners - postBlueCorners)
            else:
                score = f(points, postBlueCorners - initBlueCorners, initRedCorners - postRedCorners )
            scoredMoves.append((move,score))
            board.unmakeMove(move)
            
        if scoredMoves == []:
            return []
        
        finalMoves = []
        if len(scoredMoves) <= KEEP_MOVES:
            for i in range(len(scoredMoves)):
                finalMoves.append(scoredMoves[i][0])
        
            return finalMoves
        
        for i in range(KEEP_MOVES):
            maxScore = float('-inf')
            maxElement = None
            
            for j in range(len(scoredMoves)):
                if scoredMoves[j][1] >  maxScore:
                    maxScore =  scoredMoves[j][1]
                    maxElement = scoredMoves[j][0]
            
            scoredMoves.remove((maxElement,maxScore))
            finalMoves.append(maxElement)
            
        return finalMoves


    def getPiecesNotIn(self, l):
        pieces_used = [l[i][0] for i in range(len(l))]
        pieces_free = []
        for piece in self.pieces:
            if piece not in pieces_used:
                pieces_free.append(piece)
        
        return pieces_free
        
    
    
    def playoutRandomGame(self, node, initialBoard):
        whosTurn = node.turnColor.opp() #opposite because turnColor is who moved to make this state
        ourMove = -1 # start with not None so loop executed once for sure
        theirMove = -1
        #copy stack to add to it
        moveStack = copy(node.moveStack)
        while(True):
            if whosTurn == self.color:
                useable_pieces = self.getPiecesNotIn(moveStack)
                valid_moves = initialBoard.getAllValidMoves(useable_pieces)
                if valid_moves == []:
                    ourMove = None
                else:
                    i = randint(0, len(valid_moves) - 1)
                    ourMove = valid_moves[i]
                    moveStack.append(ourMove)
                    initialBoard.makeMoveOnBoard(ourMove)
                    #print(initialBoard)
                    
                whosTurn = whosTurn.opp()
            
            if whosTurn != self.color:
                useable_pieces = self.opponent.getPiecesNotIn(moveStack)
                valid_moves = initialBoard.getAllValidMoves(useable_pieces)
                if valid_moves == []:
                    theirMove = None
                else:
                    i = randint(0, len(valid_moves) - 1)
                    theirMove = valid_moves[i]
                    moveStack.append(theirMove)
                    initialBoard.makeMoveOnBoard(theirMove)
                    #print(initialBoard)
                    
                whosTurn = whosTurn.opp()
                    
               
                
            if ourMove == None and theirMove == None:
                #game over
                break
        
        ourScore = initialBoard.evaluateScore(self.color)
        theirScore = initialBoard.evaluateScore(self.color.opp())
        
        #return board to initial position
        initialBoard.unmakeMovesInStack(moveStack)
        
        if ourScore > theirScore:
            return 1
        if ourScore < theirScore:
            return 0
        else:
            return 0.5
        
    
    def mctsNormal(self, board):
        root = Node(None, None, None, self.opponent.color)
        # set initial child layer
        initial_moves = board.getAllValidMoves(self.pieces)
        if initial_moves == []:
            return None
        for move in initial_moves:
            #consider using piece size as first play urgency as initialVal
            child = Node(move, root, self.color, initialVal=move[0].size() * 10)
            root.addChild(child)
        
        
        num_simulations = 0
        startTime = time.perf_counter()
        while(self.resourcesAvailable(startTime)):
            #selection phase
            currentNode = Node.getMctsLeaf(root)
            #make board accurate for current state
            board.makeMovesInStack(currentNode.moveStack)
             
            #expansion phase
            useable_pieces = []
            if currentNode.turnColor == self.color:
                # opponents turn, use their pieces
                useable_pieces = self.opponent.getPiecesNotIn(currentNode.moveStack)
                
            else:
                #our turn, use our pieces
                useable_pieces = self.getPiecesNotIn(currentNode.moveStack)
            
            
            valid_moves = board.getAllValidMoves(useable_pieces)
            if valid_moves == []:
                #game in terminal moveStack for this player
                pass
            else:
                # add all substates
                for move in valid_moves:
                    child = Node(move, currentNode, move[0].color, initialVal=move[0].size() * 10 )
                    currentNode.addChild(child)
            
            #simulation phase
            res = self.playoutRandomGame(currentNode, board)
            num_simulations += 1
            #board is returned to initial state
            
            #backpropogate
            currentNode.backpropogate(res)
        
        
        #select highest val node
        node = Node.getMaxFirstLayer(root)
        #Node.delTree(root)
        #print(num_simulations, " simulations executed")
        return node.move
    
    
    
    def mctsHeuristicFirst(self, board, heuristic):
        root = Node(None, None, None, self.opponent.color)
        # set initial child layer
        initial_moves = board.getAllValidMoves(self.pieces)
        initial_moves = self.trim(board, initial_moves, heuristic)
       
        if initial_moves == []:
            return None
        for move in initial_moves:
            #consider using piece size as first play urgency as initialVal
            child = Node(move, root, self.color, initialVal=move[0].size() * 10)
            root.addChild(child)
        
        
        num_simulations = 0
        startTime = time.perf_counter()
        while(self.resourcesAvailable(startTime)):
            #selection phase
            currentNode = Node.getMctsLeaf(root)
            #make board accurate for current state
            board.makeMovesInStack(currentNode.moveStack)
             
            #expansion phase
            useable_pieces = []
            if currentNode.turnColor == self.color:
                # opponents turn, use their pieces
                useable_pieces = self.opponent.getPiecesNotIn(currentNode.moveStack)
                
            else:
                #our turn, use our pieces
                useable_pieces = self.getPiecesNotIn(currentNode.moveStack)
            
            
            valid_moves = board.getAllValidMoves(useable_pieces)
            if valid_moves == []:
                #game in terminal moveStack for this player
                pass
            else:
                # add all substates
                for move in valid_moves:
                    child = Node(move, currentNode, move[0].color, initialVal=move[0].size() * 10 )
                    currentNode.addChild(child)
            
            #simulation phase
            res = self.playoutRandomGame(currentNode, board)
            num_simulations += 1
            #board is returned to initial state
            
            #backpropogate
            currentNode.backpropogate(res)
        
        
        #select highest val node
        node = Node.getMaxFirstLayer(root)
        #Node.delTree(root)
        #print(num_simulations, " simulations executed")
        return node.move
    
    
    def mctsHeuristicAlways(self, board, heuristic):
        root = Node(None, None, None, self.opponent.color)
        # set initial child layer
        initial_moves = board.getAllValidMoves(self.pieces)
        initial_moves = self.trim(board, initial_moves, heuristic)
        
        if initial_moves == []:
            return None
        for move in initial_moves:
            #consider using piece size as first play urgency as initialVal
            child = Node(move, root, self.color, initialVal=move[0].size() * 10)
            root.addChild(child)
        
        
        num_simulations = 0
        startTime = time.perf_counter()
        while(self.resourcesAvailable(startTime)):
            #selection phase
            currentNode = Node.getMctsLeaf(root)
            #make board accurate for current state
            board.makeMovesInStack(currentNode.moveStack)
             
            #expansion phase
            useable_pieces = []
            if currentNode.turnColor == self.color:
                # opponents turn, use their pieces
                useable_pieces = self.opponent.getPiecesNotIn(currentNode.moveStack)
                
            else:
                #our turn, use our pieces
                useable_pieces = self.getPiecesNotIn(currentNode.moveStack)
            
            
            valid_moves = board.getAllValidMoves(useable_pieces)
            valid_moves = self.trim(board, valid_moves, heuristic)
            if valid_moves == []:
                #game in terminal moveStack for this player
                pass
            else:
                # add all substates
                for move in valid_moves:
                    child = Node(move, currentNode, move[0].color, initialVal=move[0].size() * 10 )
                    currentNode.addChild(child)
            
            #simulation phase
            res = self.playoutRandomGame(currentNode, board)
            num_simulations += 1
            #board is returned to initial state by the playout function
            
            #backpropogate
            currentNode.backpropogate(res)
        
        
        #select highest val node
        node = Node.getMaxFirstLayer(root)
        #Node.delTree(root)
        #print(num_simulations, " simulations executed")
        return node.move    

class AgentType(Enum):
    HUMAN = 1
    MCTS_NORM = 2
    MCTS_HEURISTIC_FIRST = 3
    MCTS_HEURISTIC_ALWAYS = 4
    MCTS_ALT = 5
    RANDOM = 6   
    def __str__(self):
        if self == AgentType.HUMAN:
            return "Human"
        if self == AgentType.MCTS_HEURISTIC_FIRST:
            return "MCTS_Heuristic_First"
        if self == AgentType.MCTS_HEURISTIC_ALWAYS:
            return "MCTS_Heuristic_Always"
        if self == AgentType.MCTS_NORM:
            return "MCTS_Norm"
        if self == AgentType.RANDOM:
            return "Rsandom"
        else:
            return "James Bond"
    


if __name__ == "__main__":
    t = time.perf_counter()
    board = Board(14)
    playerBlue = Player(Color.BLUE, AgentType.MCTS_HEURISTIC_ALWAYS)
    #playerBlue = Player(Color.BLUE, AgentType.MCTS_NORM)
    
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
    print(Board.TIME_IN_CHECK, " seconds in check")
    
   
#     for i in range(100):
#         print(playerBlue.playoutRandomGame(node))




    
    
    