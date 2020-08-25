'''
Hamming Heuristic implemented by Qiubai Yu
student number: 1663777
uwnetid: qiubay

 EightPuzzleWithHamming.py
This file augment EightPuzzle with heuristic information,
so this can be used for A* implementation.
The particular heuristic is the hamming
--- the number of tiles that are out of their places

INTENDED USAGE:
Python3 Astar.py EightPuzzleWithHamming [YOUR EXAMPLE]
'''

from EightPuzzle import *

def h(s):
    goal = [[0,1,2],[3,4,5],[6,7,8]]
    cur = s.b
    count = 0
    for i in range(3):
        for j in range(3):
            if (cur[i][j] != 0) and (cur[i][j] != goal[i][j]):
                count = count + 1
    return count