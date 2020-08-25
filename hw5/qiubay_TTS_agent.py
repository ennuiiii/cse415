'''qiubay_TTS_agent.py
Homework Assignment 5
Name: Qiubai Yu
Student number: 1663777

'''
import time
import random
from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False
INFINITY = float('inf')

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    TWF = 0
    TBF = 0
    my_board = self.board
    col = len(my_board)
    row = len(my_board[0])
    temp = []
    for i in range(col):
        for j in range(row):
            if my_board[i][j] == ' ':
                # explore all its surrounding tiles
                temp.append(my_board[(i + (col - 1)) % col][j]) #N
                temp.append(my_board[(i + (col + 1)) % col][j]) #S
                temp.append(my_board[i][(j + (row - 1)) % row]) #W
                temp.append(my_board[i][(j + (row + 1)) % row]) #E
                temp.append(my_board[(i + (col - 1)) % col][(j + (row - 1)) % row]) #NW
                temp.append(my_board[(i + (col - 1)) % col][(j + (row + 1)) % row]) #NE
                temp.append(my_board[(i + (col + 1)) % col][(j + (row - 1)) % row]) #SW
                temp.append(my_board[(i + (col + 1)) % col][(j + (row + 1)) % row]) #SE
    TWF += temp.count('W')
    TBF += temp.count('B')
    return TWF - TBF
  def custom_static_eval(self):
    #raise Exception("custom_static_eval not yet implemented.")
    my_board = self.board
    col = len(my_board)
    row = len(my_board[0])
    TWF = 0
    TBF = 0
    for i in range(0,row):
        for j in range(0,col):
            if my_board[i][j] == 'W':
                temp = []
                temp.append(my_board[(i + (col - 1)) % col][j]) #N
                temp.append(my_board[(i + (col + 1)) % col][j]) #S
                temp.append(my_board[i][(j + (row - 1)) % row]) #W
                temp.append(my_board[i][(j + (row + 1)) % row]) #E
                temp.append(my_board[(i + (col - 1)) % col][(j + (row - 1)) % row]) #NW
                temp.append(my_board[(i + (col - 1)) % col][(j + (row + 1)) % row]) #NE
                temp.append(my_board[(i + (col + 1)) % col][(j + (row - 1)) % row]) #SW
                temp.append(my_board[(i + (col + 1)) % col][(j + (row + 1)) % row]) #SE
                TWF += temp.count('W')
            elif my_board[i][j] == 'B':
                temp = []
                temp.append(my_board[(i + (col - 1)) % col][j]) #N
                temp.append(my_board[(i + (col + 1)) % col][j]) #S
                temp.append(my_board[i][(j + (row - 1)) % row]) #W
                temp.append(my_board[i][(j + (row + 1)) % row]) #E
                temp.append(my_board[(i + (col - 1)) % col][(j + (row - 1)) % row]) #NW
                temp.append(my_board[(i + (col - 1)) % col][(j + (row + 1)) % row]) #NE
                temp.append(my_board[(i + (col + 1)) % col][(j + (row - 1)) % row]) #SW
                temp.append(my_board[(i + (col + 1)) % col][(j + (row + 1)) % row]) #SE
                TBF += temp.count('B')
    return TWF - TBF
            
                
                
            
            
    
    

# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs)

def parameterized_minimax(
       current_state=None,
       max_ply=2,
       alpha_beta=False, 
       use_custom_static_eval_function=False):

  # All students, add code to replace these default
  # values with correct values from your agent (either here or below).
    DATA = {}
    DATA['CURRENT_STATE_STATIC_VAL'] = -1000.0
    DATA['N_STATES_EXPANDED'] = 0
    DATA['N_STATIC_EVALS'] = 0
    DATA['N_CUTOFFS'] = 0
  # STUDENTS: You may create the rest of the body of this function here.

    # base on player's turn
    # return the minimum or the maximum of childs static eval
    # use recursion to build a game tree with certain level of depth
    # do minimax search without alpha_beta pruning
    # @current_state {TTS_State object} - the current stage game we are exploring (convert to MY_TTS_State)
    # @depth {int} - the remaining depth of tree we could explore
    # @use_custom_static_function {boolean} - a boolean indicates whether or not to use custom static eval
    # @turn {character} - a character of 'W' or 'B' indicating whose turn
    def recursion(current_state, depth, use_custom_static_function, turn):
        current_state.__class__ = MY_TTS_State
        if depth == 0:
            DATA['N_STATIC_EVALS'] += 1
            if not (use_custom_static_eval_function):
                return current_state.basic_static_eval()
            else:
                return current_state.custom_static_eval()
        else:
            depth = depth - 1
            temp = []
            childs = find_child(current_state)
            DATA['N_STATES_EXPANDED'] += 1
            if turn == 'W':
                #playing max
                for i in range(len(childs)):
                    temp.append(recursion(childs[i], depth, use_custom_static_eval_function, 'B'))
                return max(temp)
            else:
                #playing min
                for i in range(len(childs)):
                    temp.append(recursion(childs[i], depth, use_custom_static_function, 'W'))
                return min(temp)
    
    # has the same parameter as the function recursion
    # @alpha {int} - best max value, initialized as negative infinity
    # @beta {int} - best min value, initialized as positive infinity
    def pruning(current_state, depth, use_custom_static_eval_function, turn, alpha, beta):
        current_state.__class__ = MY_TTS_State
        if depth == 0:
            DATA['N_STATIC_EVALS'] += 1
            if not (use_custom_static_eval_function):
                return current_state.basic_static_eval()
            else:
                return current_state.custom_static_eval()
        else:
            depth -= 1
            childs = find_child(current_state)
            DATA['N_STATES_EXPANDED'] += 1
            best_max = alpha
            best_min = beta
            temp = []
            if turn == 'W':
                # max player
                # only update alpha
                for i in range(len(childs)):
                    child_value = pruning(childs[i], depth, use_custom_static_eval_function, 'B', best_max, best_min)
                    if best_max < child_value:
                        best_max = child_value
                    if best_max >= best_min:
                        # alpha >= beta, prune the rest branches
                        DATA['N_CUTOFFS'] += 1
                        break
                    temp.append(child_value)
                if len(temp) == 0:
                    return best_max
                else: return max(temp)
            else:
                # min player
                # only update beta
                for i in range(len(childs)):
                    child_value = pruning(childs[i], depth, use_custom_static_eval_function, 'W', best_max, best_min)
                    if best_min > child_value:
                        best_min = child_value
                    if best_max >= best_min:
                        DATA['N_CUTOFFS'] += 1
                        break
                    temp.append(child_value)
                if len(temp) == 0:
                    return best_min
                else: return min(temp)

            
    # a helper function for minimax 
    # @current_state : {state object}
    # return all the possible next states as a list of states
    def find_child(current_state):
        #find all the vacancy in current state and put W or B on it
        temp = []
        b = current_state.board
        turn = current_state.whose_turn
        if turn == 'W':
            child_turn = 'B'
        else:
            child_turn = 'W'
        for i in range(len(b)):
            for j in range(len(b[0])):
                if b[i][j] == ' ':
                    child = current_state.copy()
                    child.board[i][j] = turn
                    child.whose_turn = child_turn
                    temp.append(child)
        return temp
    if not (alpha_beta):
        DATA['CURRENT_STATE_STATIC_VAL'] = recursion(current_state, max_ply, use_custom_static_eval_function, current_state.whose_turn)
    else:
        DATA['CURRENT_STATE_STATIC_VAL'] = pruning(current_state, max_ply, use_custom_static_eval_function, current_state.whose_turn, -10000000, 10000000)
  # Actually return all results...
    return(DATA)

def minimax(state, max_depth, current_depth, move, time_left):
    start_time = time.time()
    def find_child_move(current_state):
        temp = []
        b = current_state.board
        turn = current_state.whose_turn
        child_turn = ''
        if turn == 'W':
            child_turn = 'B'
        else:
            child_turn = 'W'
        for i in range(len(b)):
            for j in range(len(b[0])):
                if b[i][j] == ' ':
                    child = current_state.copy()
                    child.board[i][j] = turn
                    child.whose_turn = child_turn
                    move = [i,j]
                    child.__class__ = MY_TTS_State
                    elem = [child, move]
                    temp.append(elem)
        return temp
    if current_depth == max_depth:
        return [state.basic_static_eval(), move]
        #return state.custom_static_eval()
    else:
        current_depth += 1
        # childs[i] = [state, move]
        childs = find_child_move(state)
        temp = []
        if state.whose_turn == 'W':
            # max player
            # only update alpha
            for i in range(len(childs)):
                # child_value = [best_value, move]
                child_value = minimax(childs[i][0], max_depth, current_depth, childs[i][1], time_left - (time.time() - start_time))
                #print("1the child_value is ", child_value)
                #print(temp)
                if (time_left < 0.5):
                    break
                temp.append(child_value)
            if len(temp) == 0:
                #print("-10000000 is passed")
                return [1000000,[5,5]]
            else: 
                max = -10000
                move = [-1,-1]
                for i in range(len(temp)):
                    if temp[i][0] > max:
                        max = temp[i][0]
                        move = temp[i][1]
                return [max, move]
        else:
            # min player
            # only update beta
            for i in range(len(childs)):
                child_value = minimax(childs[i][0], max_depth, current_depth, childs[i][1], time_left - (time.time() - start_time))
                #print("2the child_value is ", child_value)
                #print(temp)
                if time_left < 0.5:
                    break
                temp.append(child_value)
            if len(temp) == 0:
                #print("100000 is passed")
                return [-1000000, [6,6]]
            else: 
                min = 10000
                move = 0
                for i in range(len(temp)):
                    if temp[i][0] < min:
                        min = temp[i][0]
                        move = temp[i][1]
                return [min,move]
# state - {state object} : the current state that being explored
# max_depth - {int} : the maximum depth for IDDFS
# current_depth - {int} : the current depth level
# alpha - {int} : best max
# beta - {int} : best min
# time_left - {time} : the rest time
# return [currently_best_value, move]
def search(state, max_depth, current_depth, alpha, beta, move, time_left):
    start_time = time.time()
    def find_child_move(current_state):
        temp = []
        b = current_state.board
        turn = current_state.whose_turn
        child_turn = ''
        if turn == 'W':
            child_turn = 'B'
        else:
            child_turn = 'W'
        for i in range(len(b)):
            for j in range(len(b[0])):
                if b[i][j] == ' ':
                    child = current_state.copy()
                    child.board[i][j] = turn
                    child.whose_turn = child_turn
                    move = [i,j]
                    child.__class__ = MY_TTS_State
                    elem = [child, move]
                    temp.append(elem)
        return temp
    if current_depth == max_depth:
        return [state.custom_static_eval(), move]
        #return state.custom_static_eval()
    else:
        current_depth += 1
        # childs[i] = [state, move]
        childs = find_child_move(state)
        best_max = alpha
        best_min = beta
        temp = []
        if state.whose_turn == 'W':
            # max player
            # only update alpha
            for i in range(len(childs)):
                # child_value = [best_value, move]
                child_value = search(childs[i][0], max_depth, current_depth, best_max, best_min, childs[i][1], time_left - (time.time() - start_time))
                #print("1the child_value is ", child_value)
                #print(temp)
                if best_max < child_value[0]:
                    best_max = child_value[0]
                if best_max >= best_min or (time_left < 0.5):
                    break
                temp.append(child_value)
            if len(temp) == 0:
                #print("-10000000 is passed")
                return [INFINITY,None]
            else: 
                max = -INFINITY
                move = None
                for i in range(len(temp)):
                    if temp[i][0] > max:
                        max = temp[i][0]
                        move = temp[i][1]
                return [max, move]
        else:
            # min player
            # only update beta
            for i in range(len(childs)):
                child_value = search(childs[i][0], max_depth, current_depth, best_max, best_min, childs[i][1], time_left - (time.time() - start_time))
                #print("2the child_value is ", child_value)
                #print(temp)
                if best_min > child_value[0]:
                    best_min = child_value[0]
                if best_max >= best_min or time_left < 0.5:
                    break
                temp.append(child_value)
            if len(temp) == 0:
                #print("100000 is passed")
                return [-INFINITY, None]
            else: 
                min = INFINITY
                move = None
                for i in range(len(temp)):
                    if temp[i][0] < min:
                        min = temp[i][0]
                        move = temp[i][1]
                return [min,move]   

def take_turn(current_state, last_utterance, time_limit):
    # the time
    start_time = time.time()

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  
    if who=='B': new_who = 'W'  
    new_state.whose_turn = new_who
    
    # Place a new tile
    location = _find_next_vacancy(new_state.board)
    if location==False: return [[False, current_state], "I don't have any moves!"]
    ########################new_state.board[location[0]][location[1]] = who

    # set a initial maximum depth
    current_max_depth = 2
    current_result = [-10, location]
    # if still have time, keep exploring
    while time_limit - 0.5 > time.time() - start_time:
        #print("asdkflasdfnasdlkfnasdlfknadf", time_limit - (time.time() - start_time))
        current_result = search(new_state, current_max_depth, 0, -100000000, 100000000, [-1,-1], (time_limit - (time.time() - start_time)))
        #current_result = minimax(new_state, current_max_depth, 0, [3,3], time_limit - (time.time() - start_time))
        current_max_depth += 1
    
    # after the while loop
    # current result should be comprised of [static eval of current_state, the optimal move]
    # based on the current state static eval, determine the utterance
    score = current_result[0]
    move = current_result[1]
    if move is None:
        move = location
    new_state.board[move[0]][move[1]] = who

    neg_utterance = ["I'll think harder next time",
                    "I love to win but I love to lose almost as much.",
                    "Das es nicht gut.",
                    "まずいですね",
                    "Pas très bien"]
    pos_utterance = ["Cheer up, kid.",
                    "Take this.",
                    "Vous allez perdre",
                    "Du verlierst",
                    "あなたは負けます"]
    
    new_utterance = "I'll think harder in some future game. Here's my move"
    if score >= 0:
        # randomly use pos_utterance
        new_utterance = random.choice(pos_utterance)
    else:
        # randomly use neg_utterance
        new_utterance = random.choice(neg_utterance)
       
    return [[move, new_state], new_utterance]

def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False

def moniker():
    return "Ai$"

def who_am_i():
    return """My name is u ashe me soraka, created by Q.
I'm just playing this game randomly. But you still cannot
beat me. LOLLLLLLLLLLLL"""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
    return "OK"
