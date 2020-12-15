'''
Created on Nov 20, 2020

@author: ian
'''

from Blockus.Square import Square, Color
from Blockus.Piece import Piece
from Blockus.PieceDefinitions import createPieces
from Blockus.Player import Player
from copy import deepcopy


class Board():
    '''
    represents a blockus board starting from (x,y) = (0,0) in the bottom left corner
    squares are placed in self.board in row major order
    '''

    def __init__(self, size):
        self.size = size
        self.board = []
        # fill the board
        for y in range(size):
            for x in range(size):
                s = Square(x,y)    
                self.board.append(s)
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
                
                
    def makeMove(self, player, piece, x, y):    
        if self.isValidMove(piece, x, y):
            for (px,py) in piece.points:
                square = self.getSquare(x + px, y + py)
                square.fillColor = piece.color
            return True
        return False    
        
    
    # valid move returned in the form of (piece, permutation, x, y)
    def getAllValidMoves(self, pieces):
        valid_moves = []
        #num_considerations = 0
        for piece in pieces:
            for perm in piece.permutations:
                for x in range(self.size):
                    for y in range(self.size):
                        #TODO: optimize square checking
                        #num_considerations += 1
                        if self.isValidMove(perm, x, y):
                            valid_moves.append((piece, perm, x, y))
                        
                         
     
        return valid_moves
    
    def __str__(self):
        st = ""
        for y in range(self.size -1, -1, -1):
            for a in range(self.size):
                st += "-----"
            st += '\n'
            for x in range(self.size):
                s = self.getSquare(x, y)
                if s.fillColor == Color.BLUE:
                    st += "| B |"
                elif s.fillColor == Color.RED:
                    st += "| R |"
                else:
                    st += "|   |"
            st += '\n'
        return st
            
            
if __name__ == "__main__":
    b = Board(14)        
    p = createPieces(Color.BLUE) 
    b.makeMove(p[0], 0, 0, True)
    valid_moves = b.getAllValidMoves(p)
    #valid_moves = t[0]
    f = open("results.txt", "w")
    for (pc,pm,x,y) in valid_moves:
        board = Board(14)        
        board.makeMove(p[0], 0, 0, True)
        board.makeMove(pm, x, y, False)
        f.write(str(board))
   # f.write("{} configurations checked".format(t[1]))
    f.close()
    print(len(valid_moves), "valid moves found")           
                
                
                
                
                
                
                
                
                
                
                
                