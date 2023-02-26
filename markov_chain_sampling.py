import numpy as np
from random import randrange, choice
import math
from statistics import mean

# transition probability matrices
P1 = [[0.6, 0.2, 0.2],
      [0.4, 0, 0.6],
      [0.4, 0, 0.6]]
P2 = [[0, 0.6, 0.4],
      [0.4, 0, 0.6],
      [0.4, 0, 0.6]]
P3 = [[0.6, 0.2, 0.2],
      [0.4, 0, 0.6],
      [0, 0.5, 0.5]]
P4 = [[0, 0.6, 0.4],
      [0.4, 0, 0.6],
      [0, 0.5, 0.5]]
P = [P1, P2, P3, P4]
reward = [2., -2., -4.]
N_paths = 500
N = 500 # epochs
rate = 0.85

def markov_sampling(Pd, N_paths, N): #input a transition matrix and a number of epochs
    v_paths = []
    for i in range(N_paths):
        v = 0 #initial value
        state = randrange(len(Pd)) #choose an initial state
        print(f"initial state = S{state+1}")
        for i in range(N):
            next_state_list = Pd[state]
            while True:
                next_state = randrange(len(next_state_list))
                if next_state_list[next_state] != 0:
                    v += reward[state] * math.pow(rate, i+1) #discounted reward
                    state = next_state
                    break
                else:
                    print(f"S{state+1} cannot reach S{next_state+1}")
        v_paths.append(v)
    v_mean = mean(v_paths)

    return v_mean

V_mean_list = []
for Pd in P:
    i = 1
    v_Pd = markov_sampling(Pd, N_paths, N)
    V_mean_list.append(v_Pd)
    print(f"mean discounted total reward for polciy{i} = {v_Pd}")
    i += 1

print(V_mean_list)
