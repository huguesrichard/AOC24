import numpy as np
from numpy import ndarray
import networkx as nx
from collections import OrderedDict, defaultdict


def text2lstr(text: str) -> ndarray:
    """ 
    Function to recode a list of str as a numpy matrix
    with char values
    """
    return np.array([[x for x in s] for s in text.split("\n") if len(s) > 0 ])

def distManhattan(a: tuple[int,int], b: tuple[int,int]) -> int:
    """
    computes the Manhattan distance between 2 coordinates 
    """
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def distManhattanDir(a: tuple[int,int,str], b: tuple[int,int,str]) -> int:
    """
    Computes a Manhattan distance with an additional term on direction

    """
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + int(a[2] != b[2])*100

def groupCoords(l_coords = list[tuple[int,int]],
                f_dist = distManhattan) -> list[list[tuple[int,int]]]:
    """
    from a list of coordinates in 2D performs a grouping by putting together all 
    the coords that have a manhattan distance of 1 between one of their group
    """
    n = len(l_coords)
    d_groups = dict()
    for i in range(n):
        d_groups[i] = []
        for j in range(i+1, n):
            if f_dist(l_coords[i], l_coords[j]) == 1:
                d_groups[i].append(j)
    G= nx.DiGraph(d_groups)
    l_comp = list(nx.weakly_connected_components(G))
    return l_comp
    

def remplirPlot(Ms : ndarray) -> ndarray:
    """
    From a list of list of chars, returns a matrix with a single int ID for each
    contiguous bloc with the same letter
    """
    Mout = np.full(Ms.shape, -1)
    d_lcoords = defaultdict(list)
    for i in range(Ms.shape[0]):
        for j in range(Ms.shape[1]):
            d_lcoords[Ms[i][j]].append((i,j))
    cid = 0
    for x  in d_lcoords:
        l_coords = d_lcoords[x]
        l_components = groupCoords(l_coords)
        for g in l_components:
            for i_coord in g:
                ccoord = l_coords[i_coord]
                Mout[ccoord[0], ccoord[1]] = cid
            cid += 1
    return Mout 

def computeAreaPerimeters(Ms: ndarray) -> dict[int: tuple[int,int]]:
    """
    from an encode Ms ndarray of int, computes the perimeter and 
    the area of each group
    """
    d_lcoords = defaultdict(list)
    d_out = dict()
    for i in range(Ms.shape[0]):
        for j in range(Ms.shape[1]):
            d_lcoords[Ms[i][j]].append((i,j))
    for x, l_coords in d_lcoords.items():
        area = len(l_coords)
        perimeter = computePerimeter(l_coords)
        sides = computeSides(l_coords)
        d_out[x] = (area, perimeter, sides)
    return d_out

def computePerimeter(l_coords: list[tuple[int,int]]) -> int:
    """
    From a list contiguous coordinate, computes its perimeter
    by counting the amount of faces that have no neighbor
    """
    coord_set = set(l_coords)
    perimeter = 0
    for x,y in l_coords:
        perimeter += 4 - len(coord_set.intersection([(x+1, y), (x-1,y), (x,y+1), (x, y-1)]) )
    return perimeter

def computeSides(l_coords: list[tuple[int,int]]) -> int:
    """
    From a list of contiguous coordinate, computes how many side the shape
    has by recording the positions and orientations of each side encountered
    and then merge them
    """
    coord_set = set(l_coords)
    nsides= 0
    l_sides_dir = []
    for x,y in l_coords:
        if (x+1, y) not in coord_set:
            l_sides_dir.append((x,y,"d"))
        if (x-1,y)  not in coord_set:
            l_sides_dir.append((x,y,"u"))
        if (x,y+1) not in coord_set:
            l_sides_dir.append((x,y,"r"))
        if (x, y-1) not in coord_set:
            l_sides_dir.append((x,y,"l"))
    #Lets count the number of sides now.
    l_sides = groupCoords(l_sides_dir, f_dist = distManhattanDir)
    return len(l_sides)
    


test0="""
AAAA
BBCD
BBCC
EEEC
"""

test1="""
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

testE="""
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
ABBA="""
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

m0 = text2lstr(test0)
m1 = text2lstr(test1)
c0 = remplirPlot(m0)
c1 = remplirPlot(m1)
ap0 = computeAreaPerimeters(c0)
ap1 = computeAreaPerimeters(c1)

print("Star 1, m0:", np.sum([a*p for a,p,s in ap0.values()]))

print("Star 2, m0:", np.sum([a*s for a,p,s in ap0.values()]))
###Reading the file
filename = "./inputs/input-day12.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

mfull = text2lstr(textfull)
cfull = remplirPlot(mfull)
apfull = computeAreaPerimeters(cfull)

print("Star 1, mfull:", np.sum([a*p for a,p,s in apfull.values()]))

print("Star 2, mfull:", np.sum([a*s for a,p,s in apfull.values()]))