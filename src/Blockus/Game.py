'''
Created on Nov 27, 2020

@author: ian
'''
from Blockus.Player import Player, AgentType
from Blockus.Board import Board
from Blockus.Square import Color
import sys


def printUsage():
    print('''Usage: run with 3 args - \n
        boardSize: length of board (borad is a square)\n
        BluePlayerAgentType: member of AgentTypes\n
        RedPlayerAgentType: member of AgentTypes\n
        AgentTypes: human, random, mctsNorm, mctsHeuristicConst, mctsHeuristicDiff, mctsAlt''')
           

def getAgentType(string):
    if string == "human":
        return AgentType.HUMAN
    elif string == "random":
        return AgentType.RANDOM
    elif string == "mctsNorm":
        return AgentType.MCTS_NORM
    elif string == "mctsHeuristicConst":
        return AgentType.MCTS_HEURISTIC_CONST
    elif string == "mctsHeuristicDiff":
        return AgentType.MCTS_HEURISTIC_DIFF
    elif string == "mctsAlt":
        return AgentType.MCTS_ALT
    else:
        print("Unknown agent type, using RANDOM")
        return AgentType.RANDOM

def main():
    args = sys.argv
    if len(args) < 4:
        printUsage()
        sys.exit()
    
    
    board = Board(int(args[1]))
    playerBlue = Player(Color.BLUE, getAgentType(args[2]))
    playerRed = Player(Color.RED, getAgentType(args[3]))
    
    while(True):
        blueMove = playerBlue.move(board)
        redMove = playerRed.move(board)
        if blueMove == False and redMove == False:
            break;
    
    blueScore = playerBlue.evaluateScore(board)
    redScore = playerRed.evaluateScore(board)
    
    print(board)
    if blueScore > redScore:
        print("Blue Wins {} to {}".format(blueScore, redScore))
    elif blueScore < redScore:
        print("Red Wins {} to {}".format(redScore, blueScore))
    else:
        print("Tie Game {} to {}".format(redScore, blueScore))
    
    
    print("done")
        
        
        
    


if __name__ == '__main__':
    main()