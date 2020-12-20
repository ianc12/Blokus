'''
Created on Nov 20, 2020

@author: ian
'''

#from Piece import Piece
import time
from  Square import Square, Color
from  PieceDefinitions import createPieces
from random import randint



class Board():
    TIME_IN_VALID = 0
    TIME_IN_DUP = 0
    '''
    represents a blockus board starting from (x,y) = (0,0) in the bottom left corner
    squares are placed in self.board in row major order
    '''
    def __init__(self, size):
        self.size = size
        self.board = [] # list of Square objects representing the board
        self.filledRed = [] #list Square objects which are filled with RED
        self.filledBlue = [] #filled with BLUE
        self.openSquares = []
        # fill the board
        for y in range(size):
            for x in range(size):
                s = Square(x,y)    
                self.board.append(s)
                self.openSquares.append(s)
        # calculate each square's neigbors
        for square in self.board:
            for dX in range(-1,2):
                for dY in range(-1,2):
                    if dX != 0 or dY != 0: # dont add the square itself as a neighbor
                        s = self.getSquare(square.x + dX, square.y + dY) 
                        if s != None:
                            if dX == dY or dX == -dY:
                                square.cornerNeighbors.append(s)
                            else:
                                square.sideNeighbors.append(s)                      
                 
               
    def getSquare(self,x,y):
        if (x < 0 or x >= self.size): 
            return None
        if (y < 0 or y >= self.size):
            return None
        return self.board[(self.size*y) + x]
    
    
    
    def addFill(self, square):
        if square.fillColor == None:
            return
        self.openSquares.remove(square)
        if square.fillColor == Color.RED:
            self.filledRed.append(square)
        elif square.fillColor == Color.BLUE:
            self.filledBlue.append(square)
        else:
            print("unknown color")
    
    
    
    def isValidMove(self, piece, x, y):
        touches_corner = False
        for (px,py) in piece.points:
            square = self.getSquare(x + px, y + py)
            if square is None:
                #piece goes off the edge of the board
                return False
            if square.filled():
                #piece is ovrlapping another piece
                return False
            for neighbor in square.sideNeighbors:
                if neighbor.fillColor == piece.color:
                    #piece goes against the side of another piece of same color
                    return False
            for neighbor in square.cornerNeighbors:
                if neighbor.fillColor == piece.color:
                    touches_corner = True
                    break
        return touches_corner
                
    
    def makeFirstMove(self, piece, x, y):
        squares = []
        for (px,py) in piece.points:
            squares.append((x + px, y + py))

        # must cover (4,4) on first agentMove
        if piece.color == Color.BLUE:
            for (px,py) in piece.points:
                s = self.getSquare(x + px, y + py)
                if s == None or s.fillColor != None:
                    return False
            if (4,4) in squares:
                self.makeMoveOnBoard(piece, x, y)
                return True
            else:
                return False
        # must cover size-5,size-5
        elif piece.color == Color.RED:
            for (px,py) in piece.points:
                s = self.getSquare(x + px, y + py)
                if s == None or s.fillColor != None:
                    return False
            if (self.size - 5, self.size - 5) in squares:
                self.makeMoveOnBoard(piece, x, y)
                return True
            
            
    
             
    def makeMoveOnBoard(self, perm, x, y):
        #TODO: remove valid agentMove check for optimization     
        #if self.isValidMove(perm, x, y):
        for (px,py) in perm.points:
            square = self.getSquare(x + px, y + py)
            square.fillColor = perm.color
            self.addFill(square)
        return True
#         else:
#             print("invalid agentMove")
#             return False  
    
    
    
    
#     # 'agentMove' in form of (perm, permutation, x, y)
#     def unmakeMove(self, agentMove, player):
#         for (x,y) in agentMove[1].points:
#             square = self.getSquare(x + agentMove[2], y + agentMove[3])
#             if square is not None:
#                 square.fillColor = None
#                 player.filledSquares.remove(square)
    
   
    
    # valid agentMove returned in the form of (perm, permutation, x, y)
    def getAllValidMoves(self, pieces):
        t = time.perf_counter()
        valid_moves = []
        #num_considerations = 0
        for piece in pieces:
            for perm in piece.permutations:
                for x in range(self.size - (perm.width - 1)): # dont check squares that are not possible
                    for y in range(self.size - (perm.height - 1)):
                        #TODO: optimize square checking
                        #num_considerations += 1
                        if self.isValidMove(perm, x, y):
                            valid_moves.append((piece, perm, x, y))
                        
                         
        t2 = time.perf_counter()
        Board.TIME_IN_VALID += t2-t
        return valid_moves
    
    
    '''
    returns the number of filled squares for 'color'
    '''
    def evaluateScore(self, color):
        if color == Color.BLUE:
            return len(self.filledBlue)
        elif color == Color.RED:
            return len(self.filledRed)
        else:
            print("unknown color")
            return 0
        
     
    #TODO: make board variable that stores open corners so we dont recalculate every time?
    def evaluateCorners(self, color):
        corners = 0
        
        if color == Color.BLUE:
            for square in self.filledBlue:
                for cornerN in square.cornerNeighbors:
                    # if corner square not filled
                    if cornerN.fillColor is None:
                        validCorner = True
                        for sideN in cornerN.sideNeighbors:
                            if sideN.fillColor == Color.BLUE:
                                validCorner = False
                                break
                        if validCorner:
                            corners += 1
            return corners
        
        elif color == Color.RED:
            for square in self.filledRED:
                for cornerN in square.cornerNeighbors:
                    # if corner square not filled
                    if cornerN.fillColor is None:
                        validCorner = True
                        for sideN in cornerN.sideNeighbors:
                            if sideN.fillColor == Color.RED:
                                validCorner = False
                                break
                        if validCorner:
                            corners += 1
            return corners
        else:
            print("unknown color")
            return 0
                
    
    '''
    duplicates the board with no reference issues
    '''

    def duplicate(self):
        t1 = time.perf_counter()
        
        b = Board(self.size)
        for square in self.board:
            dupSquare = b.getSquare(square.x, square.y)
            dupSquare.fillColor = square.fillColor
            b.addFill(dupSquare)
        t2 = time.perf_counter()
        Board.TIME_IN_DUP += t2-t1
        return b
            
            
            
    def __str__(self):
        st = ""
        for y in range(self.size -1, -1, -1):
            for a in range(self.size):
                st += "------"
            st += '\n'
            for x in range(self.size):
                s = self.getSquare(x, y)
                if s.fillColor == Color.BLUE:
                    st += "| bb |"
                elif s.fillColor == Color.RED:
                    st += "| RR |"
                else:
                    st += "|    |"
            st += '\n'
        return st
            
            
if __name__ == "__main__":
    b = Board(14)        
    p = createPieces(Color.BLUE)
    b.makeMoveOnBoard(p[0], 0, 0, True)
    p.remove(p[0])
    valid_moves = b.getAllValidMoves(p)
    idx = randint(0, len(valid_moves) - 1)
    agentMove = valid_moves[idx]
    b.makeMoveOnBoard(agentMove[1], agentMove[2], agentMove[3], False)
    #print(b.evaluateCorners(Color.BLUE))
    print(b)
    print(b.evaluateCorners(Color.BLUE), " corners")
    
#     valid_moves = b.getAllValidMoves(p)
#     #valid_moves = t[0]
#     f = open("results.txt", "w")
#     for (pc,pm,x,y) in valid_moves:
#         board = deepcopy(b)#Board(14)        
#         board.makeMoveOnBoard(p, p[0], 0, 0, True)
#         board.makeMoveOnBoard(pm, x, y, False)
#         f.write(str(board))
#    # f.write("{} configurations checked".format(t[1]))
#     f.close()
#     print(len(valid_moves), "valid moves found")           
                
                
                
                
                
                
                
                
                
                
                
                