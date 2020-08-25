# import dataset
# calculate the transition probabilities
# and the emission probabilties
# stored in nested maps

from google.colab import drive
drive.mount('/content/gdrive')

tfile = open('/content/gdrive/My Drive/Colab Notebooks/CSE415 Project/Training Data/Mouse vs. Beaver.txt', 'r')
allLines = tfile.readlines()
allLines[44] = allLines[44][:-1]
tfile.close()
tfile = open('/content/gdrive/My Drive/Colab Notebooks/CSE415 Project/Training Data/Mouse vs. Guinea pig.txt', 'r')
allLines += tfile.readlines()
allLines[90] = allLines[90][:-1]
tfile.close()
tfile = open('/content/gdrive/My Drive/Colab Notebooks/CSE415 Project/Training Data/Mouse vs. Hamster.txt', 'r')
allLines += tfile.readlines()
allLines[136] = allLines[136][:-1]
tfile.close()
tfile = open('/content/gdrive/My Drive/Colab Notebooks/CSE415 Project/Training Data/Mouse vs. Hedgehog.txt', 'r')
allLines += tfile.readlines()
allLines[182] = allLines[182][:-1]
tfile.close()
tfile = open('/content/gdrive/My Drive/Colab Notebooks/CSE415 Project/Training Data/Mouse vs. Squirrel.txt', 'r')
allLines += tfile.readlines()
tfile.close()
allLines[228] = allLines[228][:-1]

for i in range(len(allLines)):
  line = allLines[i][:-1]
  allLines[i] = line

mouse_seq = [] # TRPA1 protein sequence of mouse x 5
others_seq = [] # TRPA1 protein sequence of other mouse family animals (5) combined

for i in range(len(allLines)):
  line = allLines[i]
  if i%2 == 0:
    mouse_seq += list(line)
  else:
    others_seq += list(line)

mouse_new = []
others_new = []
for i in range(len(mouse_seq)):
  mouse_char = mouse_seq[i]
  others_char = others_seq[i]
  if not(mouse_char == ' '):
    mouse_new.append(mouse_char)
  if not(others_char == ' '):
    others_new.append(others_char)

print('Length of mouse_seq', len(mouse_new))
print('Length of others_seq', len(others_new))

match = 0
total = len(mouse_new)
for i in range(len(mouse_new)):
  if mouse_new[i] == others_new[i]:
    match += 1
print('Similarity (entire dataset):', match/total, '%')

# others observation
# mouse hidden states
# use others to compute transition probability
# compare and compute emission probability

dic_1 = {}
for i in range(len(others_new) - 1):
  first = others_new[i]
  second = others_new[i + 1]
  if first in dic_1:
    dic_2 = dic_1.get(first)
    if second in dic_2:
      dic_2[second] += 1
    else:
      dic_2[second] = 1
  else:
    dic_1[first] = {}
    dic_1[first][second] = 1

transition_key = ['-','a','c','d','e','f','g','h','i','k','l','m','n','p','q','r','s','t','v','w','y']
for key1 in dic_1:
  dictionary = dic_1[key1]
  for key2 in transition_key:
    if not (key2 in dictionary):
      dictionary[key2] = 0

# convert to probabilities
for key1 in dic_1:
  dictionary = dic_1[key1]
  summ = 0
  for key2 in dictionary:
    summ += dictionary[key2]
  for key3 in dictionary:
    dictionary[key3] = dictionary[key3] / summ
transition_dict = dic_1
transition_dict

emission_dict = {}
emission_keys = ['-','a','c','d','e','f','g','h','i','k','l','m','n','p','q','r','s','t','v','w','y']
for key in emission_keys:
  emission_dict[key] = {}
  for key2 in emission_keys:
    emission_dict[key][key2] = 0

for i in range(len(mouse_new)):
  mouse_aa = mouse_new[i]
  others_aa = others_new[i]
  if mouse_aa in emission_dict:
    dic_2 = emission_dict.get(mouse_aa)
    if others_aa in dic_2:
      dic_2[others_aa] += 1
    else:
      dic_2[others_aa] = 1
  else:
    emission_dict[mouse_aa] = {}
    emission_dict[mouse_aa][others_aa] = 1

for key in emission_dict:
  curr_dict = emission_dict[key]
  curr_total = 0
  for key2 in emission_dict[key]:
    curr_total += emission_dict[key][key2]
  for key2 in emission_dict[key]:
    emission_dict[key][key2] /= curr_total
emission_dict

###############################################################################
#                            Viterbi Algorithm                                #
###############################################################################
import numpy as np
#Test example for Viterbi Algorithm
# Transition matrix
transition_matrix = {'F':{'F':0.6, 'L':0.4}, 'L':{'F':0.4, 'L':0.6}}
# Emission matrix
emission_matrix = {'F':{'H':0.5, 'T':0.5}, 'L':{'H':0.8, 'T':0.2}}
# Initial probabilities
initial_prob = {'F':0.5, 'L':0.5}
# Observation
observations = ['T', 'H', 'T', 'H', 'H', 'H', 'T', 'H', 'T', 'T', 'H']

def viterbi(transition_matrix, emission_matrix, initial_prob, observations):
    # Initialize returning objects
    prediction_seq = []
    prediction_prob = 0
    # Initialize a dictionary for scores of each states
    scores = {i : [] for i in list(transition_matrix.keys())}
    # Fill in first scores column (start state to transition states probability)
    max_score = 0
    best_key = ''
    for key in scores:
        curr_observation = observations[0]
        score = emission_matrix[key][curr_observation]*initial_prob[key]
        scores[key].append(score)
        if score > max_score:
            max_score = score
            best_key = key
    prediction_seq.append(best_key)
    # Update the rest of the scores
    for i in range(1, len(observations)): # For every column
        curr_observation = observations[i]
        for key in scores: # For every row
            state_scores = []
            for key2 in scores: # Finds all the cross probabilities
                previous_score = scores[key2][i-1]
                state_scores.append(previous_score*transition_matrix[key2][key]*emission_matrix[key][curr_observation])
            scores[key].append(max(state_scores))
        # Adds the state to the prediction sequence
        max_score = 0
        best_key = ''
        for key in scores:
            score = scores[key][i]
            if score > max_score:
                max_score = score
                best_key = key
        prediction_seq.append(best_key)
    for key in scores:
        prob = scores[key][-1]
        if prob > prediction_prob:
            prediction_prob = prob
    #print(scores)
    return prediction_seq, prediction_prob

print('Predicted Sequence:', viterbi(transition_matrix, emission_matrix, initial_prob, observations)[0])
print('Probability:', viterbi(transition_matrix, emission_matrix, initial_prob, observations)[1])

###############################################################################
# Predicted Sequence: ['F', 'L', 'F', 'L', 'L', 'L', 'F', 'L', 'F', 'F', 'L'] #
# Probability: 2.86654464e-06                                                 #
###############################################################################
