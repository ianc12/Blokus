'''
Created on Nov 27, 2020

@author: ian

'''
from Blockus.Piece import Piece
from Blockus.Square import Color

def createPieces(color):
    pieces = []
    # 1
    points = [(0,0)]
    w = 1
    h = 1
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    #p.addSymmetry(Symmetry.VERTICAL)
    #p.addSymmetry(Symmetry.ROTATIONAL)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #2
    points = [(0,0), (1,0)]
    w = 2
    h = 1
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    #p.addSymmetry(Symmetry.VERTICAL)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #I3
    points = [(0,0), (1,0), (2,0)]
    w = 3
    h = 1
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    #p.addSymmetry(Symmetry.VERTICAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #I4
    points = [(0,0), (1,0), (2,0), (3,0)]
    w = 4
    h = 1
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    #p.addSymmetry(Symmetry.VERTICAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #I5
    points = [(0,0), (1,0), (2,0), (3,0), (4,0)]
    w = 5
    h = 1
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    #p.addSymmetry(Symmetry.VERTICAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #L4
    points = [(0,0), (0,1), (1,0), (2,0)]
    w = 3
    h = 2
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #L5
    points = [(0,0), (0,1), (1,0), (2,0), (3,0)]
    w = 4
    h = 2
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #Y
    points = [(0,0), (1,0), (1,1), (2,0), (3,0)]
    w = 4
    h = 2
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # N
    points = [(0,0), (1,0), (1,1), (2,1), (3,1)]
    w = 4
    h = 2
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # Z4
    points = [(0,0), (1,0), (1,1), (2,1)]
    w = 3
    h = 2
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # Z5
    points = [(0,0), (1,0), (1,1), (1,2), (2,2)]
    w = 3
    h = 3
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # Square, O
    points = [(0,0), (1,0), (1,1), (0,1)]
    w = 2
    h = 2
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.ROTATIONAL)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    #p.addSymmetry(Symmetry.VERTICAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # +, X
    points = [(0,1), (1,1), (2,1), (1,2), (1,0)]
    w = 3
    h = 3
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.ROTATIONAL)
    #p.addSymmetry(Symmetry.VERT_HORIZ)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    #p.addSymmetry(Symmetry.VERTICAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # T4
    points = [(0,0), (1,0), (2,0), (1,1)]
    w = 3
    h = 2
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # T5
    points = [(0,0), (1,0), (2,0), (1,1), (1,2)]
    w = 3
    h = 3
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #V3
    points = [(0,0), (0,1), (1,0)]
    w = 2
    h = 2
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #V5
    points = [(0,0), (0,1), (1,0), (0,2), (2,0)]
    w = 3
    h = 3
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
  
    #U
    points = [(0,0), (0,1), (1,0), (2,0), (2,1)]
    w = 3
    h = 2
    p = Piece(points, w, h, color)
    #p.addSymmetry(Symmetry.HORIZONTAL)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #W
    points = [(0,0), (1,0), (1,1), (2,1), (2,2)]
    w = 3
    h = 3
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    # P
    points = [(0,0), (1,0), (1,1), (0,1), (0,2)]
    w = 2
    h = 3
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    #F
    points = [(0,0), (0,1), (1,1), (2,1), (1,2)]
    w = 3
    h = 3
    p = Piece(points, w, h, color)
    p.permutations = p.permute(Piece.copy)
    pieces.append(p)
    
    
    return pieces


    
    
if __name__ == "__main__":
    p = createPieces(Color.BLUE)
    
    for x in p:
        for y in x.permutations:
            print(y)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    