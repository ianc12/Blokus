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
    TIME_IN_CHECK = 0
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
    
    def unaddFill(self, square):
        if square.fillColor == Color.RED:
            self.filledRed.remove(square)
            
        if square.fillColor == Color.BLUE:
            self.filledBlue.remove(square)
        
        self.openSquares.append(square)
        square.fillColor = None
        
    
    
    def isValidMove(self, piece, x, y):
        t = time.perf_counter()
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
        t2 = time.perf_counter()
        Board.TIME_IN_CHECK += t2-t
        return touches_corner
                
    
    def makeFirstMove(self, move):
        squares = []
        piece  = move[1]
        x = move[2]
        y = move[3]
        for (px,py) in piece.points:
            squares.append((x + px, y + py))

        # must cover (4,4) on first agentMove
        if piece.color == Color.BLUE:
            for (px,py) in piece.points:
                s = self.getSquare(x + px, y + py)
                if s == None or s.fillColor != None:
                    return False
            if (4,4) in squares:
                self.makeMoveOnBoard(move)
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
                self.makeMoveOnBoard(move)
                return True
            
            
    
             
    def makeMoveOnBoard(self, move):
        #TODO: remove valid agentMove check for optimization     
        #if self.isValidMove(perm, x, y):
        for (px,py) in move[1].points:
            square = self.getSquare(move[2] + px, move[3] + py)
            square.fillColor = move[1].color
            self.addFill(square)
        return True
    
    
    
    
#     # 'agentMove' in form of (perm, permutation, x, y)
    def unmakeMove(self, agentMove):
        for (x,y) in agentMove[1].points:
            square = self.getSquare(x + agentMove[2], y + agentMove[3])
            if square != None:
                self.unaddFill(square)
                
                
    
   
    def makeMovesInStack(self, stack):
        for move in stack:
            self.makeMoveOnBoard(move)

    def unmakeMovesInStack(self, stack):
        for move in stack:
            self.unmakeMove(move)
        
#     # valid agentMove returned in the form of (perm, permutation, x, y)
#     def getAllValidMoves(self, pieces):
#         t = time.perf_counter()
#         valid_moves = []
#         #num_considerations = 0
#         for piece in pieces:
#             for perm in piece.permutations:
#                 for x in range(self.size - (perm.width - 1)): # dont check squares that are not possible
#                     for y in range(self.size - (perm.height - 1)):
#                         #TODO: optimize square checking
#                         #num_considerations += 1
#                         if self.isValidMove(perm, x, y):
#                             valid_moves.append((piece, perm, x, y))
#                         
#                          
#         t2 = time.perf_counter()
#         Board.TIME_IN_VALID += t2-t
#         return valid_moves

    # valid move returned in the form of (perm, permutation, x, y)
    def getAllValidMoves(self, pieces):
        t = time.perf_counter()
        valid_moves = []
        #num_considerations = 0
        for x in range(self.size):
            for y in range(self.size):
                square = self.getSquare(x, y)
                for piece in pieces:
                    minDim = min(piece.width, piece.height)
                    maxDim = max(piece.width, piece.height)
                    if (x + minDim) >= self.size:
                        continue
                    if (y + minDim) >= self.size:
                        continue
#                     #check if played square within the max dimension of the piece
#                     if piece.color == Color.RED:
#                         within = False
#                         for fr in self.filledRed:
#                             if fr.within(square, maxDim, maxDim):
#                                 within = True
#                                 break
#                         if not within:
#                             continue
#                     elif piece.color == Color.BLUE:
#                         within = False
#                         for fb in self.filledBlue:
#                             if fb.within(square, maxDim, maxDim):
#                                 within = True
#                                 break
#                         if not within:
#                             continue
                    for perm in piece.permutations:
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
            for square in self.filledRed:
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
    b.makeMoveOnBoard((p[0],p[0], 0, 0))
    p.remove(p[0])
    valid_moves = b.getAllValidMoves(p)
    print(len(valid_moves))
#     idx = randint(0, len(valid_moves) - 1)
#     agentMove = valid_moves[idx]
#     b.makeMoveOnBoard(agentMove, False)
    #print(b.evaluateCorners(Color.BLUE))
#     print(b)
#     print(b.evaluateCorners(Color.BLUE), " corners")
#     
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
                
                
                
                
                
                
                
                
                
                
                
                