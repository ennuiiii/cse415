'''Farmer_Fox.py
by Qiubai Yu
UWNetID: qiubay
Student number: 1663777

Assignment 2, in CSE 415, Autumn 2019.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer and Fox"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHOR = ['Qiubai Yu']
PROBLEM_CREATION_DATE = "07-OCT-2019"

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

import copy

#<COMMON_CODE>
B = 0 #equal to farmer
F = 1
C = 2
G = 3
LEFT = 0
RIGHT = 1
DIC = {0:"boat & farmer ", 1:"fox ", 2:"chicken ", 3:"grain "}

class State():

    def __init__(self, d=None):
        if d==None:
            d = [[],[]]
        self.d = d
    
    def __eq__(self, s2):
        # assume that LEFT + RIGHT = [0,1,2,3], given one side will know the other side
        if sorted(self.d[LEFT]) == sorted(s2.d[LEFT]): return True
        return False

    def __str__(self):
        left_txt = "LEFT: "
        for i in self.d[LEFT]:
            left_txt = left_txt + DIC.get(i)
        left_txt = left_txt + "\n"
        right_txt = "RIGHT: "
        for j in self.d[RIGHT]:
            right_txt = right_txt + DIC.get(j)
        return left_txt + right_txt
    
    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def copy(self):
        news = State({})
        news.d[LEFT] = copy.deepcopy(self.d[LEFT])
        news.d[RIGHT] = copy.deepcopy(self.d[RIGHT])
        return news
    
    def check_side(self, side, c):
        if c == 0:
            if all(elem in side for elem in [1,2]) or all(elem in side for elem in [2,3]): return False
            return True
        elif c in side:
            if c == 1:
                if all(elem in side for elem in [2,3]): return False
                return True
            elif c == 3:
                if all(elem in side for elem in [1,2]): return False
                return True
            else: return True
        return False

    def can_move(self, c):
        '''Tests whether it's legal for the farmer to cross the river
        with choice c'''
        temp = self.d.copy()
        left = temp[LEFT]
        right = temp[RIGHT]
        if 0 in left: 
            return self.check_side(left, c)
        else: 
            return self.check_side(right, c)

    def changeSide(self, left, right, c):
        if 0 in left:
            if c == 0:
                left.remove(0)
                right.append(0)
            else:
                left.remove(0)
                left.remove(c)
                right.append(0)
                right.append(c)
        else:
            #0 in right
            if c == 0:
                right.remove(0)
                left.append(0)
            else:
                right.remove(0)
                right.remove(c)
                left.append(0)
                left.append(c)

    def move(self, c):
    #take nothing, take fox, take chicken, take grain
        news = self.copy()
        left = news.d[LEFT]
        right = news.d[RIGHT]
        self.changeSide(left, right, c)
        news.d = [left, right]
        return news

def goal_test(s):
    '''If everything is on the right, then s is a goal state.'''
    p = s.d[RIGHT]
    return (len(p) == 4)

def goal_message(s):
    return "Congratulations on successfully helping the farmer with the task"
    
class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf
    
    def is_applicable(self, s):
        return self.precond(s)
    
    def apply(self, s):
        return self.state_transf(s)
        
#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d = [[0,1,2,3],[]])
#</INITIAL_STATE>

#<OPERATORS>
#cross river alone, with fox, with chicken, with grain
choices = [0, 1, 2, 3]

OPERATORS = [Operator(
    "Cross the river with " + DIC.get(c),
    lambda s, c1 = c: s.can_move(c1),
    lambda s, c1 = c: s.move(c1))
    for c in choices]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>