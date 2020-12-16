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
        self.x = x
        self.y = y
        self.sideNeighbors = []
        self.cornerNeighbors = []
        
    def filled(self):
        return self.fillColor != None




class Color(Enum):
    RED = 1
    BLUE = 2

if __name__ == "__main__":
    for c in Color:
        print(c)
    print (len(Color))