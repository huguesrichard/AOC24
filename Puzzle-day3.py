import numpy as np
import re


test='xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'

test2=r"""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

patt =r'mul\((\d{1,3}),(\d{1,3})\)'
patt2=r'mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don\'t\(\))'

m = re.findall(patt, test)

m2 = re.findall(patt2 ,test2)

print(m)
print("First results:", sum([int(a) * int(b) for a,b in m]))

###Reading the file
filename = "./inputs/input-day3.txt"
fin = open(filename, "r")
textfull = fin.read()
fin.close()

mall = re.findall(patt, textfull)
print("Total:", sum([int(a) * int(b) for a,b in mall]))

mall2 = re.findall(patt2, textfull)

comptest = []
do = True
for l1,l2,do_flag,dont_flag in m2:
    if len(do_flag)> 1:
        do = True
    if len(dont_flag)> 1:
        do = False
    if do and len(l1)>0 and len(l2) > 0:
        comptest.append( (int(l1), int(l2)) )

print("Total star 2 test:", sum([a * b for a,b in comptest]))

comp2 = []
do = True
for l1,l2,do_flag,dont_flag in mall2:
    if len(do_flag)> 1:
        do = True
    if len(dont_flag)> 1:
        do = False
    if do and len(l1)>0 and len(l2) > 0:
        comp2.append( (int(l1), int(l2)) )

print("Total star 2 full:", sum([a * b for a,b in comp2]))
