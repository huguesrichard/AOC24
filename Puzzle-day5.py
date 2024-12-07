import numpy as np
from numpy import ndarray
import pandas as pd
import functools
from collections import OrderedDict

def getDataFrame(A: ndarray, d_n : OrderedDict[str:int]) -> pd:
    """
    Output with names
    """
    return pd.DataFrame(A, columns = d_n.keys(), index = d_n.keys())

def min_plus_product(A : ndarray,B: ndarray) -> ndarray:
    """
    Compute the min plus product of two matrices A and B,
    very convenient to compute the min cost of reaching vertex i 
    from vertex j in k step  
    """
    B = np.transpose(B)
    Y = np.zeros((len(B),len(A)))
    for i in range(len(B)):
         Y[i] = (A + B[i]).min(1)
    return np.transpose(Y)

def min_plus_square(A: ndarray) -> ndarray:
    """
    compute the square of A according to the min-plus product
    """
    return min_plus_product(A,A)

def min_plus_product_opt(A: ndarray,B: ndarray, chop: int=None) -> ndarray:
    """
    Optimized version of the min plus product from stackoverflow
    """
    if chop is None:
        # not sure this is optimal
        chop = int(np.ceil(np.sqrt(A.shape[1])))
    B = np.transpose(B)
    Amin = A.min(1)
    Y = np.zeros((len(B),len(A)))
    for i in range(len(B)):
        o = np.argsort(B[i])
        Y[i] = (A[:, o[:chop]] + B[i, o[:chop]]).min(1)
        if chop < len(o):
            idx = np.where(Amin + B[i, o[chop]] < Y[i])[0]
            for j in range(chop, len(o), chop):
                if len(idx) == 0:
                    break
                x, y = np.ix_(idx, o[j : j + chop])
                slmin = (A[x, y] + B[i, o[j : j + chop]]).min(1)
                slmin = np.minimum(Y[i, idx], slmin)
                Y[i, idx] = slmin
                nidx = np.where(Amin[idx] + B[i, o[j + chop]] < Y[i, idx])[0]
                idx = idx[nidx]
    return np.transpose(Y)


def getSuccessorsMatrix(A: ndarray, Nsq_max = 10) -> ndarray:
    """
    do squares of the transformation of an adjacency matrix until convergence
    This is in order to get the set of all successors
    the resulting reachability matrix summarizes the min number of step to 
    go from row i to col j 
    """
    n = 2
    l_Mprod = []
    Msq = np.copy(A).astype(np.float32)
    Msq[Msq == 0] = np.infty
    ##This setup is not working yet
    np.fill_diagonal(Msq, 0)
    r = 1
    #print(Msq)
    Msq_new = min_plus_square(Msq)
    while not np.array_equal(Msq_new, Msq) and r < Nsq_max:
        r += 1
        Msq = np.copy(Msq_new)
        #print(f"Step {r}:")
        #print(Msq)
        Msq_new = min_plus_square(Msq)
    return(Msq_new)

def ConstructMatrixFromText(ldep: list[str]) -> tuple[ndarray, dict[str:int]]:
    """
    Reads the list of dependencies as a list of texts separated 
    """
    lot = [t.split("|") for t in ldep]
    nodes = set([n for ln in lot for n in ln])
    d_nodes = OrderedDict([(n, i) for i,n in enumerate(sorted(nodes))])
    A = np.zeros((len(d_nodes), len(d_nodes)), dtype = int)
    for (u,v) in lot:
        A[d_nodes[u], d_nodes[v]] = 1
    return A, d_nodes

def isAnySuccessor(R: ndarray, u: int, lv: list[int]) -> bool:
    """
    From a node u to a list of node lv and a reachability matrix R 
    tells if any of the nodes in lv is a successor of u
    """
    return any([np.isfinite(R[u,v]) for v in lv])

def isAnyDirectSuccessor(A: ndarray, u: int, lv: list[int]) -> bool:
    """
    From a node u to a list of node lv and an adjacency matrix A
    tells if any of the nodes in lv is a direct successor of u
    """
    return any([A[u,v] == 1 for v in lv])

def CheckSequences(lopages: list[str], A: ndarray, d_nodes: dict[str:int]) -> tuple[list[int], list[int]]:
    """
    Check the list of strings for compatibility with the matrix of adjacency A
    returns the list of lines which are compatible or not with 
    """
    ##Construct the reachability matrix R from the matrix A
    #R = getSuccessorsMatrix(A)
    lres= [0] * len(lopages)
    midvals = [None] * len(lopages)
    for il,l in enumerate(lopages):
        cur_lopages = l.split(",")
        midvals[il] = int(cur_lopages[len(cur_lopages)//2])
        cur_lopages_index = [d_nodes[k] for k in cur_lopages]
        for i, p in enumerate(cur_lopages_index):
            #if isAnySuccessor(R, p ,lopages_index[:i]):
            if isAnyDirectSuccessor(A, p, cur_lopages_index[:i]): 
                lres[il] += 1
    lvals = [midvals[i] for i, b in enumerate(lres) if b]
    return lres, lvals

def searchConflictingUpdate(l_oi: list[int], A: ndarray) -> tuple[int, int]:
    """
    Helper function to check if an Update is compatible with
    the order given in A. 
    return None if the list is ok
    otherwise return a pair of values (u,v) where u is the leftmost index 
    that is not well allocated and v is righmost value after which it could be 
    put   
    """
    for i, u in enumerate(l_oi):
        prev_successors = [v for v in l_oi[:i] if A[u,v] == 1]
        if len(prev_successors) > 0:
            #if the current index appears before one value 
            # indexes for which it is a successor of
            ## we move it to the right of the last one
            return (prev_successors[-1],u)
    return None


def ReorderUpdate(l_oi: list[int], A: ndarray) -> list[int]:
    """
    Gets a list of indexes and the orders between indexes as a Matrix 
    and reorders it to correct inconsistencies
    """
    l_tmp = l_oi[:]
    #print("Starting list:", l_tmp)
    c = searchConflictingUpdate(l_tmp, A)
    i = 1
    while c is not None:
        u,v = c
        #print(f"found {u} and {v} to exchange")
        #Put u after v 
        iu = l_tmp.index(u)
        iv = l_tmp.index(v) + 1
        l_tmp = l_tmp[:iu] + l_tmp[iu+1:iv] + [l_tmp[iu]] + l_tmp[iv:]
        #print(f"After reorganizing, round {i}:", l_tmp)
        c = searchConflictingUpdate(l_tmp, A)
        i+= 1
        #if i>3: break
    return l_tmp


def ReorderSequences(lopages: list[str], A: ndarray, d_nodes: dict[str:int]) -> tuple[int, str, list[list[str]]]:
    """
    from a list of updates, finds the updates with errors 
    and correct them so that they are correct 
    returns the corrected updates as a str and the middle values
    """
    lres, lvals = CheckSequences(lopages, A, d_nodes)
    i2val = [k for k in d_nodes.keys()]
    out = []
    for i in range(len(lopages)):
        if lres[i] > 0:
            lp = lopages[i].split(",")
            lp_index = [d_nodes[x] for x in lp]
            lp_i_ordered = ReorderUpdate(lp_index, A)
            lp_ordered = [i2val[x] for x in lp_i_ordered]
            cres = (i, lp_ordered, lopages[i])
            out.append(cres)
    return(out)


def readText(text: str) -> tuple[list[str], list[str]]:
    """
    reads the text and returns two lists of strings by cutting at the 
    empty line
    """
    ltext = text.split("\n")
    liempty = [i for i,t in enumerate(ltext) if len(t) == 0]
    lcut = [val for i,val in enumerate(liempty) if i != val]
    cut = lcut[0]

    print(lcut)
    return ([ltext[x] for x in range(cut) if len(ltext[x])>0], 
            [ltext[x] for x in range(cut+1,lcut[1]) if len(ltext[x])> 0] )



test="""
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

page_orders, updates = readText(test)
A, d_n = ConstructMatrixFromText(page_orders)
l_seq_correct, l_vals = CheckSequences(updates, A, d_n)
print("Total test:", sum(l_vals))
#R = getSuccessorsMatrix(A)
rtest = ReorderSequences(updates, A, d_n)

###Reading the file
filename = "./inputs/input-day5.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

po_full, u_full = readText(textfull)
Afull, d_nf = ConstructMatrixFromText(po_full)
ls_full, l_v_full = CheckSequences(u_full, Afull, d_nf)
r_full = ReorderSequences(u_full, Afull, d_nf)

print("Total full:", sum(l_v_full))

print("Total reordered", sum([int(x[1][len(x[1])//2]) for x in r_full]))
