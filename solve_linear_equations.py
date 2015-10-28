
# The parameters are tuples of the constants
# for each equation in the form
# ax + by = c(mod 26)
# where a, b, and c are the constants in the 
# parameter tuples
def solveLinEquPair(equConstants1, equConstants2):
    (a1, b1, c1) = equConstants1
    (a2, b2, c2) = equConstants2
    
    xySols = []
    for x in range(0, 26):
        for y in range(0, 26):
            if (a1*x + b1*y) % 26 == c1 and (a2*x + b2*y) % 26 == c2:
                xySols.append((x, y))
                
    return xySols
    
    
constants1 = (14, 19, 19)
constants2 = (6, 22, 4)   
constants3 = (18, 4, 4)   
constants4 = (9, 24, 4)   
constants5 = (7, 14, 4) 

print solveLinEquPair(constants1, constants2)
print solveLinEquPair(constants1, constants3)
print solveLinEquPair(constants1, constants4)
print solveLinEquPair(constants1, constants5)