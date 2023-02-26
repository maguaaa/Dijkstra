import numpy as np

demand = [4, 3, 4, 3]
n =len(demand)
h = float(0.3)
K = 2
M = np.array([0]*(n**2)).reshape(n,n).astype(float)

def wagner_witin(demand, h, K):
    """
    parameters
    ----------
    demand: list
    h: int
        unit holding cost
    K: int
        fixed cost of production

    returns
    -----------
    int: optimal_cost
    """

    n = len(demand)

    v = [0]*(n+1)

    M = np.array([0]*(n**2)).reshape(n,n).astype(float)
    for i in range(n):
        for j in range(n):
            dif = j-i
            c = K # initialize the production fee
            if dif>0: # compute path from i to j, for all i!=j
                for x in range(dif):
                    c += demand[i+x+1]*(x+1)*h #holding cost
                M[i][j] = c
            elif dif==0:
                M[i][j] = c
    print(M)
    print(f"start with V{n+1} = 0\n")
    for i in range(n-1,-1,-1):# iter from the last stage to the first stage, n-1, n-2, ..., 0
        print(f"stage {i+1}")
        dif = n-i #number of items in min{}, n=len(demand)
        min_lst=[]
        print(f"\tV{i+1} = ","min{")
        for x in range(dif):
        # min{M[i-1]}
            min_lst.append(v[i+x+1]+M[i][i+x])
            print(f"\t\tc_{i+1}{x}+V{i+x+2}={v[i+x+1]+M[i][i+x]}")
        print("}")
        v[i] = min(min_lst) # update the value of stage, backward
        print(f"**update** V{i+1} = {v[i]}\n")
    optimal_cost = v[0]
    print(f"optimal cost = {optimal_cost}")
    return optimal_cost


wagner_witin(demand, h, K)
