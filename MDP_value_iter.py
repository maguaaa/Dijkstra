import numpy as np

# transitional probability matrix for each state
P1 = np.array([[0.6, 0.2, 0.2],
               [0, 0.6, 0.4]])
P2 = np.array([[0.4, 0, 0.6]])
P3 = np.array([[0.4, 0, 0.6],
              [0, 0.5, 0.5]])
P = [P1, P2, P3]
reward = [2, -2, -4]
N = 10000
S = 3
rate = 0.85 #lambda
# rate = 0.6
e = 0.01 

V = np.zeros((N,S))
policy = {}

for t in np.arange(1,N,1):
    print(f"========================iteration {t}========================")
    print(f'V[t-1]={V[t-1]}')

    for s in range(S):
        print(f'********** state=S{s+1} **********')
        v_next = rate * (P[s] @ V[t-1]) # |s| vector
        r = np.array([reward[s]] * v_next.shape[0]).reshape(v_next.shape)
        q = v_next + r # |s| vector
        print(f'v_n+1=Lv_n = {q.max()}')

        # if q.max() > V[t][s]:
        V[t][s] = q.max()  # find the maximum entry, and update the current best value
        ind = np.unravel_index(np.argmax(q, axis=None), q.shape)
        policy[f'(iter{t},S{s+1})'] = f'a{s+1}{ind[0]+1}' # update action
        print(f"action({t},S{s+1}) = {policy[f'(iter{t},S{s+1})']}")
        # print(V)

    # check stopping criteria
    norm_v = max(abs(V[t] - V[t-1]))
    print(f'norm_v = {norm_v}')
    print(f'V[t={t}]={V[t]}')
    if norm_v < e*(1-rate)/(2*rate):
        break

print("************************* FINAL SOLUTION *************************")
print(f'iteration = {t}')
print(f'final reward = {V[t]}')
print(f'policy = {policy}')
