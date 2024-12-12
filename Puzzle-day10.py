import numpy as np
from numpy import ndarray
import networkx as nx
from collections import OrderedDict, defaultdict

CODE = dict([('.', -100)] + [(str(d), d) for d in range(10)])


       #up    #down  #right   #left
DIR= [(-1,0), (1,0), (0,1), (0,-1)]

def text2mat(text :str, 
             coding = CODE) -> ndarray:
    """ 
    Function to recode a list of str as a matrix with integer values
    """
    return np.array([[coding[x] for x in s] for s in text.split("\n") if len(s) > 0 ], 
                    dtype = int)



test0="""
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
"""

test1="""
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""

test2="""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

def constructGraphDict(mat: ndarray) -> dict[tuple[int,int]:list[tuple[int,int]]]:
    """
    Constructs the graph of all possible links from the matrix of values
    """
    d_edges = defaultdict(list)
    ##We simply iterate over positions
    it = np.nditer(mat, flags = ['multi_index'])
    n,m = mat.shape
    for val in it:
        i,j = it.multi_index
        u = (i,j)
        for row,col in DIR:
            if i+row < n and j+col < m and mat[i+row, j+col] == val+1:
                v = (i+row, j+col)
                d_edges[(i,j)].append(v)
    return d_edges

def GraphDictEnumeratePaths(mat: ndarray,
                            d_graph: dict[tuple[int,int]:list[tuple[int,int]]]) -> tuple[int,int]:
    """
    Returns the number of paths from 0 to 9 in the matrix mat 
    and 
    """
    a_starts = np.argwhere(mat == 0)
    a_ends = np.argwhere(mat == 9)
    G = nx.DiGraph(d_graph)
    npaths_pos = 0 
    npaths_tot = 0
    for s_l in a_starts:
        s = tuple(s_l)
        for e_l in a_ends:
            e = tuple(e_l)
            ncpath = len(list(nx.all_simple_paths(G, s, e))) 
            if ncpath > 0:
                npaths_pos += 1 
                npaths_tot += ncpath
    return npaths_pos, npaths_tot

mat0 = text2mat(test0)
d_mat0 = constructGraphDict(mat0)
print("N paths on mat0: ", GraphDictEnumeratePaths(mat0, d_mat0))

mat2 = text2mat(test2)
d_mat2 = constructGraphDict(mat2)
print("N paths on mat2: ", GraphDictEnumeratePaths(mat2, d_mat2))


###Reading the file
filename = "./inputs/input-day10.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()
matfull =text2mat(textfull)
d_matfull = constructGraphDict(matfull)

print("N paths on matfull: ", GraphDictEnumeratePaths(matfull, d_matfull))








