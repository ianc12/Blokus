'''
Created on Nov 20, 2020

@author: ian
'''
from enum import Enum

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




class Color(Enum):
    RED = 1
    BLUE = 2
    def __str__(self):
        if self == Color.RED:
            return "Red"
        else:
            return "Blue"

if __name__ == "__main__":
    for c in Color:
        print(c)
    print (len(Color))