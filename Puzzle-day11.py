import numpy as np
from numpy import ndarray
from collections import OrderedDict

CODE = dict([('.', 0), ('#', 1),
             ('^', -2),('X', -1)])

def text2mat(los = list[str], 
             coding = CODE) -> ndarray:
    """ 
    Function to recode a list of str as a matrix with integer values
    """
    return np.array([[coding[x] for x in s] for s in los if len(s) > 0 ], 
                    dtype = int)


test="""
"""


###Reading the file
filename = "./inputs/input-dayXX.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()
