from node import *
import maze as mz
import score
import interface
import time
import BT

import numpy as np
import pandas
import time
import sys
import os

def main():
    maze = mz.Maze("data/maze.csv")
    point = score.Scoreboard("data/UID.csv", "team_NTUEE")
    # interf = interface.interface()
    # TODO : Initialize necessary variables
    bt = BT.bluetooth()
    
    k=0
    if (k == 0):#(sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        finish=False
        s=""
        end=maze.getEnds()
        print("ends are: ", end)
        a=1
        give=""
        while end:
            s = bt.SerialReadString()
            if s == "finished":
                end.remove(a)
                a=maze.BFS(maze.getNodeDict()[a])
                give=maze.getStr()
                print(give)
                bt.SerialWrite(give)

        bt.SerialWrite("s")
            
        
        
    elif (sys.argv[1] == '1'):
        print("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.

if __name__ == '__main__':
    main()
