import numpy as np
from collections import defaultdict

test="""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

mat_test = [[int(x) for x in l.split()] for l in test.split("\n") if len(l)>0 ]

def check_list_consistency(lol):
    """
    checks the matrix for consistency by computing the lags and 
    verifying the conditions
    """
    diff_list = [[b-a for a,b in zip(l[:-1], l[1:])] for l in lol]
    directions = [[x > 0 for x in l] for l in diff_list]
    distances = [[abs(x)>=1 and abs(x)<=3 for x in l] for l in diff_list ]
    same_dir = [len(set(l)) == 1 for l in directions]
    distinscope = [all(l) for l in distances]
    return [a and b for a,b in zip(same_dir, distinscope)]

def n_sign_change(ldir):
    """
    Computes the number of sign changes in a 
    list of True, False
    """
    d = defaultdict(int)
    for x in ldir:
        d[x] += 1
    if len(d) == 1:
        return 0
    else:
        return min(d.values())

def check_max_dist(l):
    """
    checks the max_dist in a list of values
    """
    diffs = [b-a for a,b in zip(l[:-1], l[1:])]  
    distances = [abs(x) >= 1 and abs(x) <= 3 for x in diffs]
    nsigns = [x >0 for x in diffs]
    return(all(distances) and len(set(nsigns)) == 1)

def check_max_sublists(l):
    """
    checks the max_dist criterion on all sublists of l
    """
    return(any([check_max_dist(l[:i] + l[i+1:]) for i in range(len(l))]))



def check_list_cons1fail(lol):
    """
    Second star: allow for at most one error
    """
    diff_list = [[b-a for a,b in zip(l[:-1], l[1:])]  for l in lol]
    #directions = [[x > 0 for x in l] for l in diff_list]
    #distances = [[abs(x)>=1 and abs(x)<=3 for x in l] for l in diff_list ]

    #n_dir_change = [n_sign_change(l)<=1 for l in directions]
    almost_same_distance = [check_max_sublists(l) for l in lol]

    return(almost_same_distance)
    #return [a and b for a,b in zip(same_dir, distinscope)]



toto = check_list_consistency(mat_test)
toto2 = check_list_cons1fail(mat_test)
#print( sum([a and b for a,b in zip(*toto2) ]))

###Reading the file, it has to be a list of lists
filename = "./inputs/input-day2.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

mat_full = [[int(x) for x in l.split()] for l in textfull.split("\n") if len(l)>0 ]
tata = check_list_consistency(mat_full)
tata2= check_list_cons1fail(mat_full)

#print( sum([a and b for a,b in zip(*tata2) ]))