import numpy as np
from numpy import ndarray
from collections import OrderedDict, defaultdict
from tqdm import tqdm
import re

def blink(n:str) -> str:
    """
    blink on one number given as a string
    """
    ## note we can replace 0*(\d+) by \1 
    if n == "0":
        return "1"
    elif len(n) % 2 == 0:
        mid = len(n) // 2
        return n[:mid] + " " + re.sub(r"0*(\d+)", r"\1", n[mid:])
    else: 
        return str(int(n)*2024)

def blink_seq(seq :str) -> str:
    """
    apply the blink on the sequence seq
    """
    return " ".join((blink(x) for x in seq.split()))

def blink_x_times(seq: str, n_times = 25) -> str:
    """
    apply the blinking ntimes 
    """
    bseq = seq.strip()
    #for _ in tqdm(range(ntimes)):
    for _ in range(n_times):
        bseq = blink_seq(bseq)
    return bseq

test="""0 1 10 99 999"""
test1="""125 17"""

def blink_x_times_cached(seq: str, n_cached = 5, n_times= 25) -> str:
    """
    does the blinking but using a dictionnary of cached str to substitute it 
    directly
    """
    bseq = seq.strip()
    assert n_times % n_cached == 0, "Error n_cached and n_times need to be in line"
    d_cached = defaultdict(lambda c: blink_x_times(c, n_times = n_cached))
    print("Building cache")
    for i in range(200):
         c = str(i)
         d_cached[c] = blink_x_times(c, n_times= n_cached)
    print("done")
    for _ in tqdm(range(n_times // n_cached)):
        for c in bseq.split():
            d_cached.setdefault(c, blink_x_times(c, n_times = n_cached))
        bseq = " ".join([d_cached[c] for c in bseq.split()])
    return bseq

def exploreStates(l_start:list[str] = ["0"]) -> defaultdict[str:list[str]]:
    """
    constructs a dict of all states that are reached from the start state
    The 
    """
    left = l_start[:]
    d_list = dict()
    while len(left) > 0:
        ns = left.pop(0)
        if ns not in d_list:
            ls = blink(ns).split()
            d_list[ns] = ls[:]   
            left += ls
    return d_list
            
def blink_x_time_dict(seq: str, n_times = 25) -> dict[str:int]:
    """
    Now the version with the dict
    """
    l_seq = seq.strip().split()
    d_path = exploreStates(l_seq)
    number_counts = defaultdict(int)
    for x in l_seq:
        number_counts[x] += 1
    for _ in tqdm(range(n_times)):
        
        new_numbers = defaultdict(int)
        for x,count in number_counts.items():
            for i in d_path[x]:
                new_numbers[i] += count
        number_counts = new_numbers.copy()
    return number_counts

toto = blink_x_times(test1)
print("Test:", len(toto.split()))
dtoto = blink_x_time_dict(test1)
print("Test with dict:", sum(dtoto.values()))

###Reading the file
filename = "./inputs/input-day11.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

tata = blink_x_times(textfull)
print("Full:", len(tata.split()))
dtata = blink_x_time_dict(textfull, n_times = 25)
print("Full with dict:", sum(dtata.values()))
#print("Up to 15 times with cache:")
#tutu_cache = blink_x_times_cached(textfull, n_cached=5, n_times=15)
#print("Full 15 cached:", len(tutu_cache.split()))

#print("Up to 10 times now:")
#tutu = blink_x_times(textfull, n_times = 10)
#print("Full 10:", len(tutu.split()))

a = blink_x_time_dict(textfull, n_times = 75)
print("Full 75 dict:", sum(a.values()))
