import numpy as np
import re 

patt=r'XMAS'

test="""
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

def reverse_strings(los: list[str]) -> list[str]:
    """
    reverses all the strings in the list
    """
    return [x[::-1] for x in los]

def rotate_strings_90(los : list[str]) -> list[str]: 
    """
    Rotates a list of strings by 90 degres clockwise
    and returns a list of strings
    Hypothesis: all string are of the same length
    """
    assert len(set([len(x) for x in los])) == 1, "Error all str must have same length"
    nrow = len(los)
    ncol = len(los[0])
    los_rotated = []
    for i in range(ncol):
        los_rotated.append("".join([ los[j][i] for j in range(nrow-1, -1,-1)]))
    return los_rotated


def diagonal_indexes(start: tuple[int,int], nrow: int, ncol:int)->list[tuple[int,int]]:
    """
    Given a rectangle with nrow rows adn ncol cols ,and starting from position 
    start = (i,j), returns the diagonal values obtained by going down on the
    right
    """
    istart, jstart = start
    if istart >= nrow or jstart >= ncol: return None
    lpos = []
    while istart < nrow and jstart < ncol:
        lpos.append((istart, jstart))
        istart += 1
        jstart += 1
    return lpos


def rotate_strings_45(los: list[str]) -> list[str]:
    """
    Rotates the list of strings by 45 degrees by taking the diagonals
    """
    assert len(set([len(x) for x in los])) == 1, "Error all str must have same length"
    nrow = len(los)
    ncol = len(los[0])
    los_rotated = []
    for icol in range(ncol):
        cindexes = diagonal_indexes((0, icol), nrow, ncol)
        clstr = [los[i][j] for i,j in cindexes]
        los_rotated.append("".join(clstr))
    for irow in range(1, nrow):
        cindexes = diagonal_indexes((irow, 0), nrow, ncol)
        clstr = [los[i][j] for i,j in cindexes]
        los_rotated.append("".join(clstr))
    return los_rotated

def search_xmas(los: list[str]) -> int:
    """
    searches for the occurrences of xmas in a list of string and returns
    the amount of hits
    """
    nocc = 0
    for s in los:
        nocc += len(re.findall(patt, s))
    return nocc 


def search_xmas_all_rotations(los: list[str]) -> int:
    """
    does the same after rotating the list 8 times.
    """
    nocc_tot = 0

    nocc = search_xmas(los)
    noccr = search_xmas(reverse_strings(los))
    los45 = rotate_strings_45(los)
    nocc45 = search_xmas(los45)
    nocc45r = search_xmas(reverse_strings(los45))

    ##The same on the 90 degree rotated
    rlos = rotate_strings_90(los)
    noccrot = search_xmas(rlos) 
    noccrotr = search_xmas(reverse_strings(rlos))
    rlos45 = rotate_strings_45(rlos)
    noccrot45 = search_xmas(rlos45)
    noccrot45r = search_xmas(reverse_strings(rlos45))
    l_nocc = [nocc, noccr, nocc45, nocc45r, noccrot, noccrotr, noccrot45, noccrot45r]
    nocc_tot = sum(l_nocc)
    return (nocc_tot, l_nocc)

##Star n. 2 
## Find the As and search for 2 M and 2 S around it at positions
## (-1,-1), (+1, -1), (-1,1) , (1,1)

def check_motif_at_pos(los: list[str], pos: tuple[int,int]) -> int:
    """
    checks the motifs around a given position and returns 
    1 if we have 2 'M' and 2 'A'
    0 otherwise
    """
    assert len(set([len(x) for x in los])) == 1, "Error all str must have same length"
    nrow = len(los)
    ncol = len(los[0])
    l_shifts = [(-1,-1), (1,-1), (-1,1), (1,1)]
    l_pos = [(pos[0]+x, pos[1]+y) for x,y in l_shifts]
    letters = []
    for x,y in l_pos:
        if x >= 0 and x < nrow and y >= 0 and y < ncol :
            letters.append(los[x][y])
        else:
            #print(f"Drop for ({x},{y})")
            return 0
    #print(letters)
    ## un peu brutal, la flemme d'écrire une fonctin de hashage
    if (letters == ["M", "M", "S", "S"] or 
        letters == ["M", "S", "M", "S"] or
        letters == ["S", "S", "M", "M" ] or
        letters == ["S", "M", "S", "M"]
    ):
        return 1
    else:
        return 0 

def count_motifs(los: list[str]) -> int:
    """
    Counts the number of motifs in the list of strings
    """
    nmotifs = 0
    for i,lr in enumerate(los):
        for m in re.finditer("A", lr):
            j = m.start()
            res= check_motif_at_pos(los, (i,j))
            #print(f"checking {i},{j}, resultat: {res}")
            nmotifs += res
    return nmotifs


l_test = [x for x in test.split("\n") if len(x) > 0]

print(search_xmas_all_rotations(l_test))

###Reading the file
filename = "./inputs/input-day4.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

l_full = [x for x in textfull.split("\n") if len(x) > 0]
print(search_xmas_all_rotations(l_full))

print("Now star n. 2")
print(count_motifs(l_test))
print(count_motifs(l_full))
