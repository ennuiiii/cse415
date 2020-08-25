'''leonz_TTS_agent.py.py


If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py

'''

from TTS_State import TTS_State
import time
from random import choice

USE_CUSTOM_STATIC_EVAL_FUNCTION = False
ROW_DIM = 0
COL_DIM = 0
K = 0
MY_SIDE = ''
OPP_NAME = ''

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    board = self.board
    twf = 0
    tbf = 0
    #ROW_DIM = len(board)
    #COL_DIM = len(board[0])
    for i in range(ROW_DIM): # i = row number
      for j in range(COL_DIM): # j = column number
        if board[i][j] == ' ':
          check = [board[i][(COL_DIM+j+1)%COL_DIM], 
                   board[i][(COL_DIM+j-1)%COL_DIM], 
                   board[(ROW_DIM+i+1)%ROW_DIM][j], 
                   board[(ROW_DIM+i+1)%ROW_DIM][(COL_DIM+j+1)%COL_DIM], 
                   board[(ROW_DIM+i+1)%ROW_DIM][(COL_DIM+j-1)%COL_DIM], 
                   board[(ROW_DIM+i-1)%ROW_DIM][j], 
                   board[(ROW_DIM+i-1)%ROW_DIM][(COL_DIM+j+1)%COL_DIM], 
                   board[(ROW_DIM+i-1)%ROW_DIM][(COL_DIM+j-1)%COL_DIM]]
          for tile in check:
            if tile == 'W':
              twf += 1
            elif tile == 'B':
              tbf += 1
    return twf - tbf

  def custom_static_eval(self):
    # Given an array, return the number of 'W' in a row
    # and 'B' in a row respectively in toroidal topology
    def how_many_in_row(arr):
      countW = 0
      countB = 0
      countEmpty = 0
      maxCountW = 0
      maxCountB = 0
      wEmpty = 0
      bEmpty = 0
      for i in range(2*len(arr)):
        curr = arr[i%len(arr)]
        if curr == 'W':
            countB = 0
            countW += 1
            if countW > maxCountW:
                maxCountW = countW
        elif curr == 'B':
            countW = 0
            countB += 1
            if countB > maxCountB:
                maxCountB = countB
        elif curr == ' ':
            countEmpty += 1
            countW = 0
            countB = 0
        else:
            countW = 0
            countB = 0
        if maxCountW > maxCountB:
            wEmpty = int(countEmpty/2)
        elif maxCountW < maxCountB:
            wEmpty = int(countEmpty/2)
      return maxCountW, wEmpty, maxCountB, bEmpty

    board = self.board

    checkEW = []
    for row in board:
      checkEW.append(row)

    checkNS = []
    for i in range(ROW_DIM):
      col = []
      for j in range(COL_DIM):
        col.append(board[j][i])
      checkNS.append(col)

    checkNW = []

    increments = [(0,0)]
    for i in range(1, int((K+1)/2)):
      increments.append((i, 0))
      increments.append((0, i))
      if K%2 == 0:
        increments.append((int(K/2), 0))

    for increment in increments:
      cross = []
      for i in range(ROW_DIM):
        cross.append(board[(i+increment[0])%ROW_DIM][(i+increment[1])%COL_DIM])
      checkNW.append(cross)

    checkSE = []

    increments = []
    for i in range(K):
      increments.append((0, -1*i))

    for increment in increments:
      cross = []
      for i in range(ROW_DIM):
        cross.append(board[(i)%ROW_DIM][(K-i-1+increment[1])%COL_DIM])
      checkSE.append(cross)
  
    checkList = checkEW + checkNS + checkNW + checkSE
    twf = 0
    tbf = 0
    for check in checkList:
      wCount, wEmpty, bCount, bEmpty = how_many_in_row(check)
      if wCount >= K:
        return 1000000
      elif bCount >= K:
        return -1000000
      else:
        twf += 2**wCount
        tbf += 2**bCount
    
    basic_eval = 0.1*self.basic_static_eval()
    
    return twf - tbf + basic_eval


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
  global ROW_DIM, COL_DIM
  ROW_DIM = len(current_state.board)
  COL_DIM = len(current_state.board[0])

  # Performs mini max search without alpha beta prunning
  def mini_max(state, depth, use_custom_static_eval_function=False):
    state.__class__ = MY_TTS_State
    if depth > 0:
      DATA['N_STATES_EXPANDED'] += 1
      successors = generate_successors(state)
      evals = []
      for successor in successors:
        evals.append(mini_max(successor, depth-1, use_custom_static_eval_function))
      if state.whose_turn == 'W':
        return max(evals)
      else:
        return min(evals)
    DATA['N_STATIC_EVALS'] += 1
    if use_custom_static_eval_function == False:
      return state.basic_static_eval()
    else:
      return state.custom_static_eval()
  
  # Performs mini max search with alpha beta prunning
  def alpha_beta_pruning(state, depth, alpha, beta, use_custom_static_eval_function=False):
    state.__class__ = MY_TTS_State
    if depth > 0:
      currentAlpha = alpha
      currentBeta = beta
      DATA['N_STATES_EXPANDED'] += 1
      successors = generate_successors(state)
      evals = []
      for successor in successors:
        value = alpha_beta_pruning(successor, depth-1, currentAlpha, currentBeta, use_custom_static_eval_function)
        if state.whose_turn == 'W': # W's turn: Update alpha if possible
          if currentAlpha < value:
            currentAlpha = value
        else: # B's turn: Update beta if possible
          if currentBeta > value:
            currentBeta = value
        if currentAlpha >= currentBeta: # Prune if alpha >= beta
          DATA['N_CUTOFFS'] += 1
          break
        evals.append(value)
      if len(evals) == 0:
        if state.whose_turn == 'W':
          return currentAlpha
        else:
          return currentBeta
      else:
        if state.whose_turn == 'W':
          return max(evals)
        else:
          return min(evals)
    DATA['N_STATIC_EVALS'] += 1
    if use_custom_static_eval_function == False:
      return state.basic_static_eval()
    else:
      return state.custom_static_eval()

  # All students, add code to replace these default
  # values with correct values from your agent (either here or below).
  DATA = {}
  DATA['CURRENT_STATE_STATIC_VAL'] = -1000.0
  DATA['N_STATES_EXPANDED'] = 0
  DATA['N_STATIC_EVALS'] = 0
  DATA['N_CUTOFFS'] = 0
  # STUDENTS: You may create the rest of the body of this function here.
  if alpha_beta == False:
    DATA['CURRENT_STATE_STATIC_VAL'] = mini_max(current_state, max_ply)
  else:
    DATA['CURRENT_STATE_STATIC_VAL'] = alpha_beta_pruning(current_state, max_ply, -float('Inf'), float('Inf'))
  # Actually return all results...
  return(DATA)

# Generate successors of current state, returning in a list
def generate_successors(current_state):
  successors = []
  board = current_state.board
  #print('Board:', board)
  turn = current_state.whose_turn
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == ' ':
        #print('i,j:', i, j)
        successor = current_state.copy()
        successor.board[i][j] = turn
        if turn == 'W':
          successor.whose_turn = 'B'
        else:
          successor.whose_turn = 'W'
        #print(successor.board)
        successor.move = [i,j]
        successors.append(successor)
  return successors

def take_turn(current_state, last_utterance, time_limit):
    start_time = time.clock()
    time_left = time_limit - (time.clock() - start_time)

    # Performs mini max search without alpha beta prunning
    def mini_max(state, depth, time_left, use_custom_static_eval_function=False):
      state.__class__ = MY_TTS_State
      time_left = time_limit - (time.clock() - start_time)
      if time_left < 0.05:
        raise 'Time run out'
      if depth > 0:
        successors = generate_successors(state)
        evals = []
        moves = []
        for successor in successors:
          eval_and_move = mini_max(successor, depth-1, time_left, use_custom_static_eval_function)
          evals.append(eval_and_move[0])
          moves.append(eval_and_move[1])
        if state.whose_turn == 'W':
          max_eval = max(evals)
          index = evals.index(max_eval)
          return max(evals), moves[index]
        else:
          min_eval = min(evals)
          index = evals.index(min_eval)
          return min(evals), moves[index]
      if use_custom_static_eval_function == False:
        return state.basic_static_eval(), state.move
      else:
        return state.custom_static_eval(), state.move

    # Performs mini max search with alpha beta prunning
    def alpha_beta_pruning(state, depth, alpha, beta, time_left, use_custom_static_eval_function=False):
      state.__class__ = MY_TTS_State
      time_left = time_limit - (time.clock() - start_time)
      if time_left < 0.05:
        raise 'Time run out'
      if depth > 0:
        currentAlpha = alpha
        currentBeta = beta
        successors = generate_successors(state)
        evals = []
        moves = []
        for successor in successors:
          value, move = alpha_beta_pruning(successor, depth-1, currentAlpha, currentBeta, time_left, use_custom_static_eval_function)
          if state.whose_turn == 'W': # W's turn: Update alpha if possible
            if currentAlpha < value:
              currentAlpha = value
          else: # B's turn: Update beta if possible
            if currentBeta > value:
              currentBeta = value
          if currentAlpha >= currentBeta: # Prune if alpha >= beta
            break
          evals.append(value)
          moves.append(move)
        if len(evals) == 0:
          if state.whose_turn == 'W':
            return currentAlpha, None
          else:
            return currentBeta, None
        else:
          if state.whose_turn == 'W':
            max_eval = max(evals)
            index = evals.index(max_eval)
            return max_eval, moves[index]
          else:
            min_eval = min(evals)
            index = evals.index(min_eval)
            return min_eval, moves[index]
      else:
        if use_custom_static_eval_function == False:
          return state.basic_static_eval(), state.move
        else:
          return state.custom_static_eval(), state.move

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'  
    if who=='B': new_who = 'W'  
    new_state.whose_turn = new_who
    
    # Find the next best move
    iddfsDepth = 0
    location = _find_next_vacancy(new_state.board) # Initialize location
    
    while time_left > 0.5:
      try:
        #print('Depth:', iddfsDepth, 'Time left:', time_left)
        iddfsDepth += 1
        value, location = mini_max(current_state, iddfsDepth, time_left, use_custom_static_eval_function=True)
        #value, location = alpha_beta_pruning(current_state, iddfsDepth, -float('Inf'), float('Inf'), time_left, use_custom_static_eval_function=False)
        #print('Location:', location)
      except:
        location = location
      time_left = time_limit - (time.clock() - start_time)
      #print('Depth:', iddfsDepth, 'Time left:', time_left)
    
    
    #value, location = mini_max(current_state, 3, time_left, use_custom_static_eval_function=True)
    #value, location = alpha_beta_pruning(current_state, 3, -float('Inf'), float('Inf'), time_left, use_custom_static_eval_function=True)
      
    # Place a new tile
    if location==False: return [[False, current_state], "Arf-Arf (I have no moves left!)"]
    new_state.board[location[0]][location[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = location

    # Make up a new remark
    utterance_choices = ["Arf-Arf (I am a angry Yorkie)", 
                     "Woof-Woof (You are stronger than my owner)", 
                     "Ruff-Ruff (Interesting ...)", 
                     "Bow-Wow (I'll let you win if you give me treat)"]
    new_utterance = choice(utterance_choices)

    return [[move, new_state], new_utterance]

def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False

def moniker():
    return "Mika" # Return your agent's short nickname here.

def who_am_i():
    return """My name is Mika, a Yorkie dog owned by Leon.
              I am smarter than my owner, since I can beat 
              him in this game."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
    global MY_SIDE, OPP_NAME, ROW_DIM, COL_DIM, K
    MY_SIDE = who_i_play
    OPP_NAME = player2Nickname
    ROW_DIM = len(initial_state.board)
    COL_DIM = len(initial_state.board[0])
    K = k # Saves the number of pieces in a row needed to win
    return "Woof-Woof (OK)"