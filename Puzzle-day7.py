import numpy as np
from numpy import ndarray
from collections import OrderedDict

def str_and_concatenate(a: int, b: int) -> int:
    """
    converts a and b to str, concatenates them and returns the int
    """
    return int(str(a) + str(b)) 

##Our list of operators indexed
L_OP = [int.__add__ , int.__mul__, str_and_concatenate]
l_opstr = ["+", "*"]

L_OP_STR = ["+", "*", "||"]


def text2Tuple(text: str) -> list[tuple[int, list[int]]]:
    """ 
    Function to read all the records and store them as lists of integers
    """
    lres = []
    for l in text.split("\n"):
        if len(l) > 0:
            res, ints = l.split(":")
            res = int(res.strip())
            ints = [int(x.strip()) for x in ints.strip().split(" ")]
            lres.append((res, ints))
    return lres

def bitfield(n: int, nfield: int):
    return [n >> i & 1 for i in range(nfield-1,-1,-1)]

def increment_ternary(l: list[int])-> list[int] : 
    """
    increment by 1 the encoding writen in the list
    """
    i = 1
    l_out=l[:]
    l_out[-i] += 1
    while l_out[-i]== 3:
        l_out[-i] = 0
        i += 1
        l_out[-i] += 1
    return l_out

def compute_value(op_use: list[int], loi: list[int]) -> int:
    """
    Computes the operation with op_use and loi
    """
    res = loi[0]
    ### I could do a reduce instead of the for loop here
    for i,o in enumerate(op_use):
        res = L_OP[o](res,loi[i+1])
    return res


def checkOperation(res: int, loi: list[int]) -> int:
    """
    checks if it is possible to obtain res by combining the elements of loi 
    using only '+' or '*' 
    The operations are evaluated from left to right (no precedence)
    """
    noperands = len(loi) - 1
    noperations = 1 << noperands
    nequals = 0
    for i in range(noperations):
        operand_use = bitfield(i, noperands)
        if compute_value(operand_use, loi) == res:
            return 1
            ##nequals += 1
            ##old version that was counting the number of combinations
    return 0

def checkOperationTernary(res: int, loi: list[int]) -> int:
    """
    Same as checkOperation but considers three possible operators
    +, * and || 
    """
    noperands = len(loi) - 1
    noperations = 3**noperands
    operand_use = [0] * noperands
    for i in range(noperations-1):
        if compute_value(operand_use,loi) == res:
            return 1
        operand_use = increment_ternary(operand_use)
        #last value
    if compute_value(operand_use,loi) == res:
        return 1
    return 0


test="""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

lt = text2Tuple(test)
l_nres = [checkOperationTernary(lt[x][0], lt[x][1]) for x in range(len(lt))]
print(np.sum([lt[i][0] for i,x in enumerate(l_nres) if x > 0]))

###Reading the file
filename = "./inputs/input-day7.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

lfull = text2Tuple(textfull)
print("Checking with 2 operators")

l_nresfull = [checkOperation(lfull[x][0], lfull[x][1]) for x in range(len(lfull))]

print(np.sum([lfull[i][0] for i,x in enumerate(l_nresfull) if x > 0]))
print("Now checking with 3 operators")
l_nresfull_3 = [checkOperationTernary(lfull[x][0], lfull[x][1]) for x in range(len(lfull))]
print(np.sum([lfull[i][0] for i,x in enumerate(l_nresfull_3) if x > 0]))