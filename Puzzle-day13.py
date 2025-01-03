import numpy as np
from numpy import ndarray
from collections import namedtuple
import re
from tqdm import tqdm
import math

Div = namedtuple('Div', 'q r')
Diophantian = namedtuple('Diophantian', 'x0 y0 at bt kmin kmax')

def read_characteristics(infos: str) -> tuple[ndarray, ndarray]:
    """
    reads the information about one claw system
    """
    pattAll = r"X[=+](\d+),\s+Y[=+](\d+)"
    l_infos = [re.findall(pattAll, x) for x in infos.split("\n") if len(x) > 0]
    M = np.array(l_infos[0] + l_infos[1]).astype(int).transpose()
    A = np.array(l_infos[2]).astype(int).transpose()
    return M, A

def isinteger(x):
    return np.equal(np.mod(x, 1), 0)

def isempty_interval(i: tuple[int,int]) -> bool:
    """
    tests for empty interval
    """
    return i[0] > i[1]

def intersect_intervals(i1: tuple[int,int], i2: tuple[int,int]) -> tuple[int,int]:
    """
    intersects 2 intervals [i1[0], i1[1]] with [i2[0], i2[1]]
    Hypothesis: i1[0] <= i1[1] so for instance [1, 0] is the empty set
    """
    ## Need a solution if one of the intervals is empty
    return max(i1[0], i2[0]), min(i1[1], i2[1])

test="""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

def list_Euclid(a: int, b:int) -> list[int]:
    """
    Calcul de la suite des restes à la Euclide
    """
    l_rests = []
    aorig, borig = a,b
    if b > a :
        a,b = b,a
    if b == 1:
        return [Div(a, 0)]
    while b != 0:
        cdiv = Div(a//b, a % b)
        l_rests.append(cdiv)
        a = b
        b = cdiv.r
    return l_rests[:-1]

def find_one_solution_gcd(a: int, b:int) -> tuple[int,int]:
    """
    Uses Bezout identity decomposition to find a solution to the relative integer
    equation a.x + b.y = d where d = gcd(a,b)
    """
    if b > a:
        y0, x0 = find_one_solution_gcd(b,a)
        return (x0, y0)
    l_E = list_Euclid(a, b)
    curdiv = l_E.pop()
    l_prods = [(1, -curdiv.q)]
    while len(l_E) > 0:
        curdiv = l_E.pop()
        c_prod = (l_prods[-1][1], l_prods[-1][0] - l_prods[-1][1]*curdiv.q)
        l_prods.append(c_prod)
    return l_prods[-1]


def get_solution_range(a: int, b: int, c: int) -> list[int]:
    """
    Returns a list of all values of x,y positive integers 
    such that a.x + b.y = c
    """
    d = math.gcd(a, b)

    at, bt, ct = (a // d, b // d, c // d)
    x0, y0 = find_one_solution_gcd(at, bt)
    x0, y0 = x0* ct, y0 * ct
    k_min, k_max = (math.ceil(-x0 / bt), math.floor(y0 / at))
    #print(k_min, k_max)
    ## Not good
    return [(x0 + bt*k, y0 - at*k) for k in range(k_min, k_max+1)]

def get_sol_rangeDiophantian(sol : Diophantian) -> list[int]:
    """
    same as above using the Diophantian 
    """
    return [(sol.x0 + sol.bt * k, sol.y0 - sol.at * k) for k in range(sol.kmin, sol.kmax + 1)]

def get_x_interval(s : Diophantian) -> tuple[int,int]:
    """
    returns x_min and x_max with every a in [x_min, x_max] bein a solution
    """
    return sorted([s.x0 + s.bt * s.kmin , s.x0 + s.bt*s.kmax])

def get_y_interval(s : Diophantian ) -> tuple[int,int]:
    """
    returns y_min and y_max with every a in [y_min, y_max] being a solution
    """
    return sorted([s.y0 - s.at * s.kmin , s.y0 - s.at*s.kmax])

def get_solution_information(a: int, b:int, c:int) -> Diophantian:
    """
    Returns the informations about the set of solutions of the diophantian
    equation a.x + b.y = c
    """
    d = math.gcd(a, b)

    at, bt, ct = (a // d, b // d, c // d)
    x0, y0 = find_one_solution_gcd(at, bt)
    x0, y0 = x0* ct, y0 * ct
    k_min, k_max = (math.ceil(-x0 / bt), math.floor(y0 / at))
    return Diophantian(x0, y0, at, bt, k_min, k_max)

def intersect_two_solutions(sol0 : Diophantian, sol1: Diophantian) -> list[int]:
    """
    From two ranges of solutions from two diophantian equations 
    a0.x + b0.y = c0
    a1.x + b1.y = c1
    returns the sets of x and y that solves it. 
    """
    x0_int = get_x_interval(sol0) 
    x1_int = get_x_interval(sol1)
    x_intint = intersect_intervals(x0_int, x1_int)
    y0_int = get_y_interval(sol0)
    y1_int = get_y_interval(sol1)
    y_intint = intersect_intervals(y0_int, y1_int)
    return(x_intint, y_intint)


def integer_solution_diophantian_eq(M, A) -> set[tuple[int, int]]:
    """
    From a pair of diophantian equations given as M and A, returns the solution
    """
    if not is_solution(M, A):
        return None
    ## Transform the k intervals 
    #sol_0 = get_solution_range(M[0,0], M[0,1], A[0,0])
    #sol_1 = get_solution_range(M[1,0], M[1,1], A[1,0])
    ## Now we need to find the smallest integer solution
    sol_0 = get_solution_information(M[0,0], M[0,1], A[0,0])
    sol_1 = get_solution_information(M[1,0], M[1,1], A[1,0])

    #return (sol_0,sol_1)
    return (sol_0, sol_1)

def solve_diophantian_eq_system(M:ndarray, A: ndarray) -> set[tuple[int,int]]:
    """
    From a system of 2 diophantian equations, solves it in 2 steps 
    and return the lowest value 
    """
    if not is_solution(M,A):
        return None
    sol0, sol1 = integer_solution_diophantian_eq(M, A)
    Mk = np.array([[sol0.bt, -sol1.bt], [sol0.at, -sol1.at] ])
    Ak = np.array([[sol1.x0 - sol0.x0], [sol1.y0 - sol0.y0]])
    if not is_solution(Mk, Ak):
        return None
    k_sol0, k_sol1 = integer_solution_diophantian_eq(Mk, Ak)
    #k_range0 = get_sol_rangeDiophantian(k_sol0)
    #k_range1 = get_sol_rangeDiophantian(k_sol1)
    return(k_sol0, k_sol1)

def get_gcd_and_rest(M: ndarray, A: ndarray) -> tuple[ndarray, ndarray]:
    """
    Get the gcds and rest between 
    """
    gcds = np.array([[math.gcd(M[0,0], M[0,1])] ,  [math.gcd(M[1,0], M[1,1])]])
    rests= np.array([[ A[0]% gcds[0,0], A[1] % gcds[1,0]]])
    return gcds, rests

def is_solution(M: ndarray, A: ndarray) -> bool:
    """
    Uses Bezout lemma to tell if there is an integer solution
    """
    #first check if there is a solution
    gcds, rests = get_gcd_and_rest(M,A)
    return np.all(rests == 0)

def check_solution(M: ndarray, A:ndarray, X:ndarray) -> bool:
    """
    checks if M * X = A 
    """
    return np.all(np.dot(M, X) == A)

def find_solution_easy(M:ndarray, A:ndarray) -> ndarray:
    """
    The easy version of finding the solution of M * X = A
    if there is no solution returns 0
    """
    ##simplifying my life
    a0, b0, c0 = M[0,0], M[0,1], A[0,0]
    a1, b1, c1 = M[1,0], M[1,1], A[1,0]
    x = (c0*b1 - c1*b0) // (a0*b1 - a1*b0)
    y = (a1*c0 - a0*c1) // (b0*a1 - b1*a0)
    X = np.array([[x], [y]])
    if check_solution(M, A, X):
        return X
    else:
        return np.zeros((2,1), dtype = int)


l_infos = test.split("\n\n")
all_mats = list(map(read_characteristics, l_infos))
all_res = [np.linalg.solve(M,A) for M,A in all_mats]
test_keep = [R for R in all_res if np.all(np.isclose(R, R.astype(int))) ]
all_sol_easy = [find_solution_easy(M,A) for M,A in all_mats]

# for M,A in all_mats:
#     print(np.hstack((M,A)))
#     print(integer_solution_diophantian_eq(M,A))

###Reading the file
filename = "./inputs/input-day13.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

l_infos_full = textfull.split("\n\n")
all_mats_full = list(map(read_characteristics, l_infos_full))
all_mats_full_s2 = [(np.copy(M), A+10000000000000) for M,A in all_mats_full]
all_res_full = [(np.linalg.solve(M,A),integer_solution_diophantian_eq(M,A)) for M,A in all_mats_full]
#all_res_full_s2 = [solve_diophantian_eq_system(M,A) for M,A in all_mats_full_s2]
all_res_full_s2_easy = [find_solution_easy(M,A) for M,A in all_mats_full_s2]

# joint_info = [(all_mats_full[i][0],all_mats_full[i][1],all_res_full[i]) for i in range(len(all_res_full))]

#res_keep = [R for R in all_res_full if np.all(np.isclose(R, np.round(R))) and np.all(R <= 100.01) ]
# #res_keep_s2 = [np.round(R) for R in all_res_full_s2 if np.all(np.isclose(R, np.round(R)))  ]

#print("Total: ", np.sum([[3*x[0], x[1]] for x in res_keep]))
print("Total s2: ", np.sum([[3*x[0], x[1]] for x in all_res_full_s2_easy]))
