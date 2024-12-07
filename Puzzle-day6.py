import numpy as np
from numpy import ndarray
from tqdm import tqdm

CODE = dict([('.', 0), ('#', 1),
             ('^', -2),('X', -1), ('Y', -5)])

def text2mat(los = list[str], 
             coding = CODE) -> ndarray:
    """ 
    Function to recode a list of str as a matrix with integer values
    """
    return np.array([[coding[x] for x in s] for s in los if len(s) > 0 ], 
                    dtype = int)

def withinBoundaries(pos: tuple[int,int], shape: tuple[int,int]) -> bool:
    """
    check if the value pos is within the boundaries given by shape
    """
    return pos[0] >= 0 and pos[0] < shape[0] and pos[1] >= 0 and pos[1]< shape[1]

def move(pos : tuple[int, int], dir: str,  matmap: ndarray) -> (tuple[int,int], str):
    """
    moves the cursor from pos to the next one, using the matrix and the direction
    given by str
    """
    npos = None
    sh = matmap.shape
    if dir == "u":
        npos = (pos[0] -1, pos[1])
        if withinBoundaries(npos, sh) and matmap[npos] == CODE['#']:
            npos = pos
            dir = "r"
    elif dir == "d":
        npos = (pos[0] +1, pos[1])
        if withinBoundaries(npos, sh) and matmap[npos] == CODE['#']:
            npos = pos
            dir = "l"
    elif dir == "l":
        npos = (pos[0], pos[1] -1 )
        if withinBoundaries(npos, sh) and matmap[npos] == CODE['#']:
            npos = pos
            dir = "u"
    elif dir == "r":
        npos = (pos[0], pos[1] + 1)
        if withinBoundaries(npos, sh) and matmap[npos] == CODE['#']:
            npos = pos
            dir = "d"
    return (npos, dir)

def fillMatrix(mat:ndarray, start_pos: tuple[int,int], 
               start_dir: str = "u") -> tuple[ndarray, bool]:
    """
    Starting from start_pos makes the gard move onto mat until it reaches one border
    of the map
    """
    cpos = start_pos
    cdir = start_dir
    shape = mat.shape
    mat_fill = np.copy(mat)
    mat_dir = [[None] * shape[1] for x in range(shape[1])]
    mat_dir[cpos[0]][cpos[1]] = cdir
    inCycle = False
    lpath_max = shape[0] * shape[1] * 4
    lpath = 0
    while withinBoundaries(cpos, shape) and not inCycle:
        lpath +=1 
        if (mat_fill[cpos] == CODE["X"] and
            cdir == mat_dir[cpos[0]][cpos[1]]):
                inCycle = True
                #print("found cycle")    
        mat_dir[cpos[0]][cpos[1]] = cdir 
        mat_fill[cpos] = CODE["X"]
        cpos,cdir = move(cpos, cdir, mat)
        if lpath > lpath_max:
            print(f"Error with this one we are looping and not detecting it")
            return mat_fill, True
    return mat_fill, inCycle

def testNewObstacles(mat: ndarray) -> int :
    """
    Tries to put a new obstacle on every "X" position on the matrix
    and then returns the number of obstacles that generate a cycle
    """
    start_pos = tuple(np.argwhere(mat == CODE["^"])[0])
    matfill, isCycle = fillMatrix(mat, start_pos)
    path = [tuple(x) for x in 
            list(np.argwhere(matfill == CODE["X"]))]
    nvalid_obstacles = 0
    #print("the path", path)
    mtest = np.copy(mat)
    for obstacle in tqdm(path):
        #print("Testing obstacle", obstacle)
        mtest[obstacle] = CODE["#"]
        mtest_fill, isCycle = fillMatrix(mtest, start_pos)
        if isCycle: 
            #print("found cycle for obstacle at", obstacle)
            nvalid_obstacles += 1
        mtest[obstacle] = CODE["."]
    return nvalid_obstacles


test="""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

mtest = text2mat(test.split("\n"))
start = tuple(np.argwhere(mtest == CODE["^"])[0])
print("Start test", start)
mtest_fill, cycle_test = fillMatrix(mtest, start)

print("Test obstacles, found ncycles:", testNewObstacles(mtest))

print("Total:", np.sum(mtest_fill == CODE["X"]))
###Reading the file
filename = "./inputs/input-day6.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

mfull = text2mat(textfull.split("\n"))

startfull = tuple(np.argwhere(mfull == CODE["^"])[0])
print("Start", startfull)
mfull_fill, cycle_full = fillMatrix(mfull, startfull)

print("Total:", np.sum(mfull_fill == CODE["X"]))
print("Test obstacles full, found ncycles:", testNewObstacles(mfull))