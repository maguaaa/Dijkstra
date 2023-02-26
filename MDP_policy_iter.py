import numpy as np

# transitional probability matrix for each state
P1 = [[0.6, 0.2, 0.2],
      [0, 0.6, 0.4]]
P2 = [[0.4, 0, 0.6]]
P3 = [[0.4, 0, 0.6],
      [0, 0.5, 0.5]]
P = [P1, P2, P3]
reward = [2., -2., -4.]
N = 10000
S = 3
# rate = 0.85
rate = 0.6
e = 0.01

# V = np.zeros((N,S))
policy = {}

i = 0
while True:
    if i==0: # initialize policy
        Pd_iter = [P1[0], P2[0], P3[0]]
        print(f"========================iteration {i}========================")
        print(f'Initial Policy: d(S1)=a11, d(S2)=a21, d(S3)=a31')
    else:
        Pd_update = Pd_iter.copy()
        for s in range(S): # for later iterations
            q = P[s] @ V_iter # find argmax -> new policy
            ind = np.unravel_index(np.argmax(q, axis=None), q.shape)
            d_iter = ind[0] # row index of matrix P -> action # for each state
            Pd_update[s] = P[s][d_iter] # update Pd matrix
            policy[f'i={i+1},S{s+1}'] = f'a{s+1}{d_iter+1}'
            print(f'policy: d(S{s+1})=a{s+1}{d_iter+1}')

    #solve equation matrix and get V vector
    V_iter = np.linalg.solve((np.identity(S)-np.multiply(Pd_iter,rate)), reward) # (I-lambda*P)v = r
    print(f'v(S1)={V_iter[0]}, v(S1)={V_iter[1]}, v(S1)={V_iter[2]}')

    if i!=0 and Pd_update == Pd_iter:
        break
    else:
        i += 1
        print(f"========================iteration {i}========================")


print("************************* FINAL SOLUTION *************************")
print(f'iterations = {i+1}')
print(f'final reward ={ V_iter}')
print(f'policy = {policy}')


