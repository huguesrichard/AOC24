import numpy as np
from numpy import ndarray
from collections import OrderedDict, Counter
from tqdm import tqdm
import re

CODE = dict([('.', 0), ('#', 1),
             ('^', -2),('X', -1)])


def drawpos(l_pos = list[tuple[int,int]], roomsize = tuple[int,int]) -> str:
    """
    Draw all the robots on a given room
    """
    mat_room = [ ['.'] * roomsize[0] for _ in range(roomsize[1])]
    for x,y in l_pos:
        if mat_room[y][x] == '.':
            mat_room[y][x] = '1'
        else:
            mat_room[y][x] = str(int(mat_room[y][x]) + 1)
    return "\n".join(["".join(l) for l in mat_room])

def computePosAfternSteps(pos: tuple[int,int], 
                          velocity = tuple[int,int], 
                          roomsize = tuple[int,int],
                          nsecs = 100) -> tuple[int,int]:
    """
    Compute the position of a mobile after nsecs given it move at a given
    velocity each second
    """
    new_pos = (pos[0] + nsecs * velocity[0], pos[1] + nsecs * velocity[1])
    new_pos = (new_pos[0] % roomsize[0], new_pos[1] % roomsize[1])
    #cases which are negative, 
    new_pos = (new_pos[0] if new_pos[0] >=0 else roomsize[0] - new_pos[0],
               new_pos[1] if new_pos[1] >=0 else roomsize[1] - new_pos[1])

    return new_pos

def read_infos(text:str) -> list[tuple[tuple[int,int], tuple[int,int]]]:
    """
    reads starting position and velocity from a list separated by newlines
    """
    pattern = r"p\=(\d+,\d+)\s+v=(-?\d+,-?\d+)"
    s_pos_vel = [re.findall(pattern, s)[0] for s in text.split("\n") if len(s) >0]
    pos_vel = []
    for spos, svel in s_pos_vel:
        pos = tuple(int(x) for x in spos.split(","))
        vel = tuple(int(x) for x in svel.split(","))
        pos_vel.append((pos, vel))
    return pos_vel

def n_bots_quadrant(l_pos: list[tuple[int,int]], roomsize : tuple[int,int]) -> list[int]:
    """
    Computes the number of bots in each quadrant
    """
    midvert, midhoriz = roomsize[0]//2, roomsize[1] // 2
    # l_quadrant = []
    # for pos in l_pos:
    #     if pos[0] == midvert or pos[1] == midhoriz :
    #         l_quadrant.append(None)
    #     else:
    #         l_quadrant.append(int(pos[0] > midvert) + 2* int(pos[1] > midhoriz))
    l_quadrant = [int(pos[0] > midvert) + 2* int(pos[1] > midhoriz) for pos in l_pos 
                                   if pos[0] != midvert and pos[1] != midhoriz]
    l_quad_count = [0] * 4
    for p in l_quadrant:
        l_quad_count[p] += 1
    return l_quad_count

### This is not the correct solution, let's implement something with the
### Chinese Rest Theorem
def detectRobotsLine(l_pos: list[tuple[int,int]], 
                     roomsize: tuple[int,int] = (101,103),
                     nsecs_min: int = 1, 
                     nsecs_max: int = 1000000, 
                     line_min_size = 40)-> int:
    """
    moves the robots until it finds a line with at least line_min_size robot on it
    """
    for nsecs in tqdm(range(nsecs_min, nsecs_max+1)): 
        l_poscur = (computePosAfternSteps(p,v, roomsize, nsecs = nsecs) for p,v in l_pos)
        c_row =  Counter(l_poscur)
        if max(c_row.values()) > line_min_size:
            return nsecs 
        nsecs += 1 
    print("Reached max iterations: ")
    return

test="""
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3                      
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

lpv = read_infos(test)
lpv_100secs = [computePosAfternSteps(p,v, (11,7), nsecs = 100) for p,v in lpv]
quad_count = n_bots_quadrant(lpv_100secs, (11,7))


###Reading the file
filename = "./inputs/input-day14.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

lpv_full = read_infos(textfull)
lpv_full_100secs = [computePosAfternSteps(p,v, (101,103), nsecs = 100) for p,v in lpv_full]
quad_count_full = n_bots_quadrant(lpv_full_100secs, (101,103))
