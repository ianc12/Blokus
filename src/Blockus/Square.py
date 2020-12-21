'''
Created on Nov 20, 2020

@author: ian
'''
from enum import Enum
import math

class Square():
    '''
    classdocs
    '''
    def __init__(self, x, y):
        self.fillColor = None
        self.x = x # x board coordinate
        self.y = y # y board coordinate
        self.sideNeighbors = [] # list of squares to the side 
        self.cornerNeighbors = [] # list of squares at corners
        
    def filled(self):
        return self.fillColor != None

    def within(self, other, xdist, ydist):
        withinx = abs(self.x - other.x) <= xdist
        withiny = abs(self.y - other.y) <= ydist
        return withinx and withiny
        
        


class Color(Enum):
    RED = 1
    BLUE = 2
    def __str__(self):
        if self == Color.RED:
            return "Red"
        else:
            return "Blue"
    def opp(self):
        if self == Color.RED:
            return Color.BLUE
        else:
            return Color.RED



if __name__ == "__main__":
    s = Square(0,0)
    s1 = Square(3,2)
    print(s.within(s1,2,2))
    
    l = [(s,6), (s1,9)]
    l.remove((s,6))
    print(l)
#     l = [i for i in range(50)]
#     print(l)
#     l = [Color.RED]
#     for c in l:
#         print(c)
#     #print (len(Color))