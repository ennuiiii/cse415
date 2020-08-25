''' 
Manhattan Heuristic implemented by Qiubai Yu
student number: 1663777
uwnetid: qiubay

EightPuzzleWithManhattan.py
This file augment EightPuzzle with heuristic information,
so this can be used for A* implementation.
The particular heuristic is the Manhattan distance heuristic
--- Manhattan distance: The number of rows and columns each tile is away from its place
Manhattan distance heuristic: the sum of the Manhattan distance of all 8 tiles

INTENDED USAGE:
Python3 AStar.py EightPuzzleWithManhattan [YOUR EXAMPLE]
'''

from EightPuzzle import *

def indexof(x, lst):
    # directly use 3
    for i in range(3):
        for j in range(3):
            if lst[i][j] == x:
                return [i,j]


def h(s):
    goal = [[0,1,2],[3,4,5],[6,7,8]]
    count = 0
    cur = s.b
    for i in range(1,9):
        index_of_cur = indexof(i,cur)
        index_of_goal = indexof(i,goal)
        count = count + abs(index_of_cur[0] - index_of_goal[0]) + abs(index_of_cur[1] - index_of_goal[1])
    return count
