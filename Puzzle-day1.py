#import numpy as np
from collections import defaultdict

test="""
3 4
4 3
2 5
1 3
3 9
3 3
"""

def sum_from_text(t: str) -> int: 
    """
    Computes the sum of the lists after sorting them
    """
    lt = t.split("\n")
    all_pairs = [[int(x) for x in l.split()] for l in lt if len(l) > 0]
    l1, l2 = zip(*all_pairs)
    l1 = sorted(l1)
    l2 = sorted(l2)
    total = sum (abs(int(x) - y) for x,y in zip(l1,l2))
    return total

def sum_weight_from_text(t: str) -> int:
    """
    Second star, needs to reweight only on cooccuring elements
    """
    lt = t.split("\n")
    all_pairs = [[int(x) for x in l.split()] for l in lt if len(l) > 0]
    l_left, l_right = zip(*all_pairs)
    d_right = defaultdict(int)
    for n in l_right:
        d_right[n] += 1
    vals = [x * d_right[x] for x in l_left]
    return sum(vals)


###Reading the file
filename = "./inputs/input-day1.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

bigtot = sum_from_text(textfull)
print("total q.1:" , bigtot)

tot_test2 = sum_weight_from_text(test)
print("total q.2 test: ", tot_test2)
tot_full2 = sum_weight_from_text(textfull)
print("test2: ", tot_test2) 
print("tot 2:", tot_full2)