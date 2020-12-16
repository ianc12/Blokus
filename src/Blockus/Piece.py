'''
Created on Nov 20, 2020

@author: ian
'''
from enum import Enum
from Blockus.Square import Color
from copy import deepcopy

'''
    a piece is a list of origin based (x,y) tuples
'''
class Piece():
    
    '''
        Appends piece to list(l) if a piece with 
        all the same points is not already in the list
        returns true if a piece was appended, false else
    '''
    @staticmethod
    def appendIfNotExists(l, piece, toappend):
        for p in l:
            isSame = True
            for point in piece.points:
                if point not in p.points:
                    isSame = False
                    break
            if isSame:
                return False
        
        l.append(toappend)
        return True

    
    def __init__(self, points, width, height, color):
        self.points = points
        self.width = width
        self.height = height
        self.color = color
        self.permutations = [] # dont permute here so there isnt recursion wackiness
        #self.symmetry = []
        
    
    # TODO: Check for reference weirdness
    def copy(self):
        # dont set permutations on a copy
        p = Piece(deepcopy(self.points), self.width, self.height, self.color);
#         p.symmetry = self.symmetry
        return p
    
#     def addSymmetry(self, symmetry):
#         self.symmetry.append(symmetry)
    
    def size(self):
        return len(self.points)      
        
    def rotateClockwise(self, degrees):
        if degrees == 90:
            # (x,y) -> (y,-x)
            temph = self.height
            self.height = self.width
            self.width = temph
            new_points = []
            for (x,y) in self.points:
                new_points.append((y,-x + (self.height - 1)))
            self.points = new_points
        elif degrees == 180:
            # (x,y) -> (-x,-y)
            new_points = []
            for (x,y) in self.points:
                new_points.append((-x + (self.width - 1) , -y + (self.height - 1)))
            self.points = new_points
        elif degrees == 270:
            # (x,y) -> (-y,x)
            temph = self.height
            self.height = self.width
            self.width = temph
            new_points = []
            for (x,y) in self.points:
                new_points.append((-y + self.width-1, x))
            self.points = new_points
        else:
            print("invalid rotation")
        
            
    
    def rotateCounterclockwise(self, degrees):
        if degrees == 90:
            self.rotateClockwise(270)
        elif degrees == 180:
            self.rotateClockwise(180)
        elif degrees == 270:
            self.rotateClockwise(90)
        else:
            print("invalid rotation")
    
    
    
    def reflectHoriz(self):
        # (x,y) -> (-x,y)
        new_points = []
        for (x,y) in self.points:
            new_points.append((-x + (self.width - 1) , y))
        self.points = new_points
    
    
    
    def reflectVert(self):
        # (x,y) -> (x,-y)
        new_points = []
        for (x,y) in self.points:
            new_points.append((x, -y + (self.height - 1)))
        self.points = new_points
        

    
                    
    '''
    fills the results list with every permutation (rotation, reflection) of the piece
    with no duplicates 
    '''
    def permute(self, f):
        results = []
            
        for i in range(4):
            Piece.appendIfNotExists(results, self, f(self))
            self.rotateClockwise(90)
    # reflect horiz if no symmetry
        self.reflectHoriz()
        for i in range(4):
            Piece.appendIfNotExists(results, self, f(self))
            self.rotateClockwise(90)
        self.reflectHoriz() # return to original position
    # reflect vert if no symmetry
        self.reflectVert() # reflect horiz and vert
        for i in range(4):
            Piece.appendIfNotExists(results, self, f(self))
            self.rotateClockwise(90)
        self.reflectVert() # reset to orig pos
    # reflect both horizontal and vertical
        self.reflectHoriz()
        self.reflectVert()
        for i in range(4):
            Piece.appendIfNotExists(results, self, f(self))
            self.rotateClockwise(90)
        self.reflectHoriz()
        self.reflectVert()
                
        
        return results
    
    
    
    def __str__(self):
        s = "color: {}\n__________\n".format(self.color)
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if (x,y) in self.points:
                    s += "x"
                else:
                    s+= " "
            s += "\n"
        s += "__________\n"    
        return s
    
    
        
        
    
# class Symmetry(Enum):
#     VERTICAL = 1
#     HORIZONTAL = 2
#     ROTATIONAL = 3
#     VERT_HORIZ = 4
    
if __name__ == "__main__":
    points = [(0,0),(0,1),(0,2),(1,2),(1,0)]
    w = 2
    h = 3
    
    points1 = [(0,2),(0,1),(1,1),(2,1),(2,0)]
    w1 = 3
    h1 = 3
    
    
    c = Color.BLUE
    #p = Piece(points, w, h, c)
    p1 = Piece(points1, w1, h1, "red")
    print(p1)
    p1.reflectHoriz()
    p1.reflectVert()
    print(p1)
#     
#     pieces = p1.permute(Piece.copy)
#     for p in pieces:
#         print(p)
#    p.permute(print)
    
#     print(p1)
#     p1.rotateClockwise(90)
#     print(p1)
#     p1.reflectHoriz()
#     print(p1)
#     p1.reflectVert()
#     print(p1)


    print("done")



                