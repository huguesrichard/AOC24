import numpy as np
from numpy import ndarray
from collections import OrderedDict

CODE = dict([('.', 0), ('#', 1),
             ('^', -2),('X', -1)])

def text2mat(text:str) -> ndarray:
    """ 
    Function to recode str as a matrix with integer values
    we use the ord function here
    """
    return np.array([[ord(x) for x in s] for s in text.split("\n") if len(s) > 0 ], 
                    dtype = int)


test="""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

test2="""
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
"""

def list_antennapairs(mat: ndarray) -> ndarray:
    """
    gets the list of pairs of antinodes from a matrix mat
    """
    l_antennapairs = []
    for val in np.unique(mat):
        if val != ord("."):
            val_occ = np.argwhere(mat == val)
            nvocc = len(val_occ)
            for i in range(nvocc):
                for j in range(i+1, nvocc):
                    a1 = tuple(val_occ[i])
                    a2 = tuple(val_occ[j])
                    l_antennapairs.append((a1, a2))
    return np.array(l_antennapairs)

def get_antinodes(mat_pairs: ndarray) -> ndarray:
    """
    returns the 2 possible antinodes for two nodes n1 and n2 (for 1st star)
    """
    diff1 = np.diff(mat_pairs, axis = 1)
    diff2 = np.copy(-diff1)
    moves = np.concatenate((diff2, diff1), axis = 1)
    antinodes = mat_pairs + moves
    ##Now just reorder the antinodes
    npairs = mat_pairs.shape[0]*2
    m_antinodes = np.reshape(antinodes, (npairs,2))
    return np.unique(m_antinodes,axis =0)

def get_antinodes_harmonic(mat_pairs: ndarray, nmult: int) -> ndarray:
    """
    Returns the possible antinodes for two nodes n1 and n2 (2nd star)
    It proposes positions from 1 to nmult dist between the 2 nodes
    """
    lmpairs = len(mat_pairs)
    diff1 = np.diff(mat_pairs, axis = 1)
    diff2 = np.copy(-diff1)
    diff1_mult_tmp = np.dot(np.array([range(nmult)]).transpose() ,diff1)
    dfms = diff1_mult_tmp.shape
    diff1_mult = np.zeros((dfms[1], dfms[0], dfms[2]))
    diff2_mult = np.zeros((dfms[1], dfms[0], dfms[2]))
    diff2_mult_tmp = np.dot(np.array([range(nmult)]).transpose() , diff2)
    #Here I not fluent enough with Tensor so I have to do a for loop
    it = np.nditer(diff1_mult_tmp, flags = ['multi_index'])
    for x in it:
        i,j,k = it.multi_index
        diff1_mult[j,i,k] = x
        diff2_mult[j,i,k] = diff2_mult_tmp[i,j,k]
    mulmat = np.vstack((np.tile(np.array([1,0]), (nmult,1)),
                        np.tile(np.array([0,1]), (nmult,1))))
    mat_pairs_mult = np.array([ np.dot(mulmat, x) for x in mat_pairs])
    moves_mult = np.concatenate((diff2_mult, diff1_mult), axis = 1)
    antinodes_harmonic = mat_pairs_mult + moves_mult
    ##Now just reorder the antinodes
    #return mat_pairs_mult, moves_mult, antinodes_harmonic
    npairs = antinodes_harmonic.shape[0] * antinodes_harmonic.shape[1]
    m_antinodes_harm = np.reshape(antinodes_harmonic, (npairs,2))
    return np.unique(m_antinodes_harm,axis =0)

mt2 = text2mat(test2)
mp2 = list_antennapairs(mt2)
m_a_h2 = get_antinodes_harmonic(mp2, nmult =5)
mask_2 = np.logical_and(m_a_h2 >= np.array([0,0]), m_a_h2 < mt2.shape)
m_a_h2 = m_a_h2[np.sum(mask_2, axis =1)>= 2]

mtest = text2mat(test)
m_pairs = list_antennapairs(mtest)
m_antinodes= get_antinodes(m_pairs)

m_a_harm = get_antinodes_harmonic(m_pairs, nmult= 10)
mask_pairs = np.logical_and(m_antinodes >= np.array([0,0]), m_antinodes < mtest.shape)
mask_pairs_harm = np.logical_and(m_a_harm >= np.array([0,0]), m_a_harm < mtest.shape)

print("N. positive", np.sum(np.sum(mask_pairs, axis =1)>= 2))
print("N. positive harmonic", np.sum(np.sum(mask_pairs_harm, axis =1)>= 2))

###Reading the file
filename = "./inputs/input-day8.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

mfull = text2mat(textfull)
m_pairsfull = list_antennapairs(mfull)
m_antinodesfull= get_antinodes(m_pairsfull)

mask_pairs_full = np.logical_and(m_antinodesfull >= np.array([0,0]), 
                                 m_antinodesfull < mfull.shape)

print("N. positive full", np.sum(np.sum(mask_pairs_full, axis =1)>= 2))
m_a_harm_full = get_antinodes_harmonic(m_pairsfull, nmult= mfull.shape[0])
mask_pfull_harm = np.logical_and(m_a_harm_full >= np.array([0,0]), m_a_harm_full < mfull.shape)
print("N. positive harmonic full", np.sum(np.sum(mask_pfull_harm, axis =1)>= 2))
