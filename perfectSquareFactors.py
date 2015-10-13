import math

number = 2**5*3**5*5**2

# holds the number of factors of number
numFactors = 0
# holds the number of factors of number that are perfect squares
numPerfSqrFactors = 0

for i in range(1, number+1):
    # make sure it's a factor
    if number % i != 0:
        continue
    numFactors += 1
    # calculate the square root and truncate the decimal
    sqrt = int(math.sqrt(i))    
    # make sure the truncated value squared is the original i
    if sqrt**2 == i:
        numPerfSqrFactors += 1
    	print i, '\t\t=', sqrt, '*', sqrt
                
print "\nFound:\t\t%d factors\n\t\t%d factors are perfect squares" % (numFactors, numPerfSqrFactors)

