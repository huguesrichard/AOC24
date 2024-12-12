import numpy as np
from numpy import ndarray
from collections import OrderedDict


##From SO very practical
def rindex_notNone(lst: list[int]) -> int:
    for i in range(len(lst)-1, -1, -1):
        if lst[i] is not None :
            return i
    return None

def codeBlocks(seq:str) -> list[int]:
    """
    reads the string and construct a list with the mapping of blocs 
    with either ID value as an int or None if it is free space
    """
    l_blocs = []
    cid = 0
    for i, c in enumerate(seq):
        cval = int(c)
        if i%2 == 0:
            lvals = [cid] * cval 
            cid +=1
        else:
            lvals = [None] * cval
        l_blocs += lvals
    return l_blocs

def codeBlocksAsReversedTuples(seq:str) -> list[tuple[int,int, int]]:
    """
    return the Blocks as a list of ID and size and position on the big list
    """
    t_tuples = [(i%2, i//2, int(c)) for i,c in enumerate(seq)]
    pos = 0
    b_tuples = []
    for m, id, val in t_tuples:
        if m%2 == 0:
            b_tuples.append( (id, val, pos) )
        pos += val
    return list(reversed(b_tuples))


def getSpaceBlocs(blocs : list[int]) -> list[tuple[int,int]]:
    """
    gets the list of spaces with their starting index and their size 
    """
    spaces = [x is None for x in blocs]
    ix = [ i for i,a in enumerate(zip(spaces[:-1], spaces[1:])) if a[1]-a[0] != 0 ]
    lsizes = [ (ix[i]+1, ix[i+1] - ix[i]) for i in range(0, len(ix), 2) ]
    return lsizes

def fillLeft(id: int, size: int, id_pos: int, spaces: list[tuple[int,int]]) -> int:
    """
    tries to put a value id of size int in a list of spaces
    - returns the position where the id and int goes
    - updates the list of spaces as a reference
    """
    i = 0
    while i < len(spaces) and spaces[i][1] < size:
        i += 1
    if i < len(spaces) and spaces[i][0] < id_pos:
        pos = spaces[i][0]
        space_size = spaces[i][1] 
        if space_size == size:
            #we take out this space
            spaces.pop(i)
        else:
            spaces[i] = (pos+size, space_size - size)
        ##We also create a space where the 
        return pos
    else:
        return -1

def fillAllblocs(l_blocs: list[int], l_spaces: list[tuple[int,int]], l_ids = list[tuple[int,int,int]]) -> list[int]:
    """
    fills All the blocs from left to right
    """
    for id, size, id_pos in l_ids:
        pos = fillLeft(id, size, id_pos, l_spaces)
        if pos >= 0:
            for i in range(size):
                l_blocs[pos + i] = id
                l_blocs[id_pos+ i] = None
            #print("moved id:", id)
            #print(writeBlocks(l_blocs))
    return l_blocs



def writeBlocks(l_blocs : list[int]) -> str:
    """
    write function
    """
    def code_letter(c: str) -> str: 
        if c is None:
            return "."
        return str(c)
    return "".join(map(code_letter, l_blocs))

def defrag(l_blocs : list[int]) -> list[int]:
    """
    defragments the bloc with a while loop
    """
    defrag_blocs = l_blocs[:]
    first_space = defrag_blocs.index(None)
    last_bloc = rindex_notNone(defrag_blocs)
    while first_space < last_bloc:
        defrag_blocs[first_space] = defrag_blocs[last_bloc]
        defrag_blocs[last_bloc] = None
        first_space = defrag_blocs.index(None)
        last_bloc = rindex_notNone(defrag_blocs)
        #print(writeBlocks(defrag_blocs))
    return defrag_blocs

def defrag_block(l_blocs: list[int]) -> list[int]:
    """
    Defragmentation with 
    """
    defrag_blocs = l_blocs[:]
    space_sizes = getSpaceBlocs(defrag_blocs)
    #bloc_sizes

def checksum(l_bloc) -> int: 
    """
    computes the checksum for the l_bloc
    """
    return sum([i*v for i, v in enumerate(l_bloc) if v is not None])

test="""2333133121414131402"""

tf = codeBlocks(test)
print(writeBlocks(tf))
tf_defrag = defrag(tf)
spaces = getSpaceBlocs(tf)
blocksID = codeBlocksAsReversedTuples(test)

print("Filling left blocs test:", checksum(fillAllblocs(tf, spaces, blocksID)))

###Reading the file
filename = "./inputs/input-day9.txt"
fin = open(filename, "r")
textfull = fin.read().strip()
fin.close()

print ("full text of length ", len(textfull))
tf_full = codeBlocks(textfull)
spaces_full = getSpaceBlocs(tf_full)
blocksID_full = codeBlocksAsReversedTuples(textfull)

#tf_fulldefrag = defrag(tf_full)
#print("Checksum:", checksum(tf_fulldefrag))

print("Filling left blocs full:", checksum(fillAllblocs(tf_full, spaces_full, blocksID_full)))