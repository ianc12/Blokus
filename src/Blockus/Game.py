'''
Created on Nov 27, 2020

@author: ian
'''
from Player import Player, AgentType
from Board import Board
from Square import Color
import sys
import multiprocessing


CORES = 4

def printUsage():
    print('''Usage: run with 3 args - \n
        boardSize: length of board (borad is a square)\n
        BluePlayerAgentType: member of AgentTypes\n
        RedPlayerAgentType: member of AgentTypes\n
        AgentTypes: human, random, mctsNorm, mctsHeuristicFirst, mctsHeuristicAlways''')
           

def getAgentType(string):
    if string == "human":
        return AgentType.HUMAN
    elif string == "random":
        return AgentType.RANDOM
    elif string == "mctsNorm":
        return AgentType.MCTS_NORM
    elif string == "mctsHeuristicFirst":
        return AgentType.MCTS_HEURISTIC_FIRST
    elif string == "mctsHeuristicAlways":
        return AgentType.MCTS_HEURISTIC_ALWAYS
#     elif string == "mctsAlt":
#         return AgentType.MCTS_ALT
    else:
        print("Unknown agent type, using RANDOM")
        return AgentType.RANDOM

def main():
    args = sys.argv
    if len(args) < 4:
        printUsage()
        sys.exit()
    
    
    board = Board(int(args[1]))

    # Blue Goes First
    playerBlue = Player(Color.BLUE, getAgentType(args[2]), 30)
    playerRed = Player(Color.RED, getAgentType(args[3]), 30)
    playerBlue.opponent = playerRed
    playerRed.opponent = playerBlue
    
    playerBlue.agentMove(board, True)
    playerRed.agentMove(board, True)
    print(board)
    print("\n\n\n")
    print("_________________________________________________________________________")
    print("\n\n\n")
    while(True):
        blueMove = playerBlue.agentMove(board, False)
        redMove = playerRed.agentMove(board, False)
        print(board)
        if blueMove == None and redMove == None:
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
        
        
def play(blueAgent, redAgent, thinkTime):
    board = Board(14)

    # Blue Goes First
    playerBlue = Player(Color.BLUE, blueAgent, thinkTime)
    playerRed = Player(Color.RED, redAgent, thinkTime)
    playerBlue.opponent = playerRed
    playerRed.opponent = playerBlue
    
    playerBlue.agentMove(board, True)
    playerRed.agentMove(board, True)
    
    while(True):
        blueMove = playerBlue.agentMove(board, False)
        redMove = playerRed.agentMove(board, False)
        if blueMove == None and redMove == None:
            break;
    
    blueScore = playerBlue.evaluateScore(board)
    redScore = playerRed.evaluateScore(board)
    return (blueScore, redScore)



def experiment(expNo, games, blueAgent, redAgent, thinkTime):
    fname = "expNO{}_{}_vs_{}_think_{}.txt".format(expNo, str(blueAgent), str(redAgent), thinkTime)
    f = open(fname, "w")
    blueWins = 0
    redWins = 0
    ties = 0
    blueTotalScore = 0
    redTotalScore = 0
    for i in range(games):
        results = None
        blueScore = 0
        redScore = 0
        if i%2 == 0:
            results = play(blueAgent, redAgent, thinkTime)
            blueScore = results[0]
            redScore = results[1]
        else:
            results = play(redAgent, blueAgent, thinkTime)
            blueScore = results[1]
            redScore = results[0]
        
        blueTotalScore += blueScore
        redTotalScore += redScore
        if blueScore > redScore:
            blueWins += 1
        elif blueScore < redScore:
            redWins += 1
        else:
            ties += 1
    
        f.write("Game {}: blueScore:{} \t redScore:{}\n".format(i, blueScore, redScore))
        
    
    
    
    f.write("_________FINAL RESULTS____________\n")
    f.write("Blue({}) win percent: {}\n".format(str(blueAgent), blueWins/games))
    f.write("Red({}) win percent: {}\n".format(str(redAgent), redWins/games))
    f.write("Ties:{}\n".format(ties))
    f.write("Blue average score: {}\n".format(blueTotalScore/games))
    f.write("Red average score: {}\n".format(redTotalScore/games))
    f.close()


def test():
    jobs = []
    x = multiprocessing.Process(target=experiment, args=(1, 2, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_FIRST, 2,))
    jobs.append(x)
    x.start()
    x = multiprocessing.Process(target=experiment, args=(1, 2, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_ALWAYS, 2,))
    jobs.append(x)
    x.start()
    
    for j in jobs:
        j.join()
    print("done")

def full():
    jobs = []
    # 10 second think times
#     x = multiprocessing.Process(target=experiment, args=(1, 30, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_FIRST, 10,))
#     jobs.append(x)
#     x.start()
#     
#     x = multiprocessing.Process(target=experiment, args=(2, 30, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_ALWAYS, 10,))
#     jobs.append(x)
#     x.start()
#     
#     x = multiprocessing.Process(target=experiment, args=(3, 30, AgentType.MCTS_FIRST, AgentType.MCTS_HEURISTIC_ALWAYS, 10,))
#     jobs.append(x)
#     x.start()
#     
#     # 20 second think times
#     x = multiprocessing.Process(target=experiment, args=(4, 30, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_FIRST, 20,))
#     jobs.append(x)
#     x.start()
#     
#     x = multiprocessing.Process(target=experiment, args=(5, 30, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_ALWAYS, 20,))
#     jobs.append(x)
#     x.start()
#     
#     x = multiprocessing.Process(target=experiment, args=(6, 30, AgentType.MCTS_FIRST, AgentType.MCTS_HEURISTIC_ALWAYS, 20,))
#     jobs.append(x)
#     x.start()
    
    #30 second think times
    x = multiprocessing.Process(target=experiment, args=(7, 30, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_FIRST, 30,))
    jobs.append(x)
    x.start()
    
#     x = multiprocessing.Process(target=experiment, args=(7, 30, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_ALWAYS, 30,))
#     jobs.append(x)
#     x.start()
    
    x = multiprocessing.Process(target=experiment, args=(9, 30, AgentType.MCTS_HEURISTIC_FIRST, AgentType.MCTS_HEURISTIC_ALWAYS, 30,))
    jobs.append(x)
    x.start()
    
#     x = multiprocessing.Process(target=experiment, args=(1, 2, AgentType.MCTS_NORM, AgentType.MCTS_HEURISTIC_FIRST, 2,))
#     jobs.append(x)
#     x.start()
    for j in jobs:
        j.join()
    print("done")



if __name__ == '__main__':
    #full()
    sys.setrecursionlimit(10000)
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    