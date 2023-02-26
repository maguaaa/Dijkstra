import numpy as np, numpy.random
import pandas as pd
import time

# get the start time
st = time.time()
# state has to be a list starting from 0 to M with step = 1
# action is a list with discrete values, with "0" action
# demand is seperated to two lists, one is demand value, the other is coresponding probability

# production parameters
M=100 # k kits capacity
T=6 # 6 months
K=50/100 # $/100kits fixed producation cost
P=10 # $ unit price
C=2 # $ production cost per kit
H=1 # $ holing cost per kit

#demand distribution
demand = np.array([15, 25, 50, 70, 80, 90])
demand_p = np.array([0.05, 0.3, 0.25, 0.15, 0.15, 0.1])
#demand_p = np.random.dirichlet(np.ones(20),size=1)[0]
#demand = np.arange(0, M, 3)


# generate possible action based on M
# action = [0, 20, 40, 60, 80, 100]
action = np.arange(0, M+1, 20)

# real state value
# state = [0, 1, 2, ..., 100]
state = np.arange(0, M+1, 1)


# transition probability matrix
tpm = {} # pair of (action, tpm)
dim_s = len(state)
dim_a = len(action)

for a in action:
    p = np.zeros((dim_s, dim_s)) # generate |S|*|S| matrix
    # rows
    for row in range(len(state)):
        current_state = state[row]
        # p[row] is to be updated
        next_state_update = [0] * dim_s
        for di in range(len(demand)):
            if current_state+a<=M:
                next_state_update[max(current_state+a-demand[di],0)] += demand_p[di]
            else:
                pass
        # update TMP
        p[row] = next_state_update
    # print(p)
    tpm.update({a:p})


# expected revenue
    # s+a<=M
exp = []
for m in np.arange(0, M+1, 1):
    df = pd.DataFrame([demand, [m]*len(demand)])
    sale_amt = np.array(list(df.min())) # min{s_t+a_t, d_t}
    exp_rev = (np.dot(sale_amt, demand_p))*P
    exp.append(exp_rev)


# expected lost sale penalty
lost = []
for m in np.arange(0, M+1, 1):
    df = pd.DataFrame([demand-np.array([m]*len(demand)), [0]*len(demand)])
    lost_amt = np.array(list(df.max())) # max{d_t-(s_t+a_t), 0}
    lost_rev = (np.dot(lost_amt, demand_p))*20
    lost.append(lost_rev)


def prod_cost(a):
    if a>0:
        cost = K + C*a
    else:
        cost = 0
    return cost


# reward matrix
rm = np.ones((len(state),len(action))) * np.NINF #initialize with negative infinity
for row in range(len(state)):
    for ai in range(len(action)):
        a = action[ai]
        x = state[row]+a #current_state + action
        if state[row]+a <= M:
            reward_s_a = exp[x] - prod_cost(a) - H*x  - lost[x]
            rm[row][ai] = reward_s_a


# backward induction
optimal_policy = []
value = [[0] * dim_s]

for t in np.arange(T,0,-1):
    update_value = []
    update_action = []
    for si in range(len(state)):
        vsa = []
        for ai in range(len(action)):
            a = action[ai]
            vsa.append(rm[si][ai] + np.dot(tpm[a][si], value[0]))
        update_value.append(max(vsa))
        update_action.append(action[vsa.index(max(vsa))])
    value.insert(0, update_value)
    optimal_policy.insert(0, update_action)


# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('''

OPTIMAL POLICY === 
''')
print(optimal_policy)

print('''

OPTIMAL VALUE === 
''')
print(value)
print('''
''')
print('Execution time:', elapsed_time, 'seconds')


# df1 = pd.DataFrame(optimal_policy)
# df2 = pd.DataFrame(value)
# with pd.ExcelWriter("./project/results_mod.xlsx") as writer:
#     df1.to_excel(writer, sheet_name="OP_base", index=False, header=False)
#     df2.to_excel(writer, sheet_name="V_base", index=False, header=False)
