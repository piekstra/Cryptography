import math, argparse

## Combinatorics
#
# Basic operations for 'counting'
# It is important to note that this class does not take
# into account extremely large numbers, so accuracy
# WILL be severely diminished in those scenarios
class Combinatorics:
    def permute(self, n, r, repetition=False):
        # if repeats are allowed, the permutation is simply n^r
        if repetition:
            return n**r
        # if repeats are not allowed, the permutation is simply ( n! / (n - r)! )
        # this is optimized to only multiply n * n-1 * n-2 ... n-r
        # as opposed to calculating both factorials and dividing
        else:
            # holds the solution
            sol = 1
            for i in range(n, n-r, -1):
                sol *= i
            return sol
    def choose(self, n, r, repetition=False):
        if repetition:    
            # holds the solution
            sol = 1        
            # To minimize computations, do either (n + r -1)! / r!
            # or (n + r -1)! / (n-1)! first depending on whether
            # r > n-1
            if r > n-1:
                for i in range(n+r-1, r, -1):            
                    sol *= i
                return sol / math.factorial(n-1)
            else:
                for i in range(n+r-1, n-1, -1):            
                    sol *= i
                return sol / math.factorial(r)
        else:
            # using the fact that n choose r is symmetrical to 
            # n choose n-r, we can do a speed optimization
            # since the permute method is optimized
            if r > n-r:
                r = n-r
            return self.permute(n, r) / math.factorial(r)

## example usage is as follows:
#
#   python combinatorics.py -cm --csv --values 6 2 8 2 3 1
#
#   This is the same as saying: compute C(6,2), C(8,2), and C(3,1)
#   then multiply the results together.
#
#   The program will print 15, 28, 3, and 1,260
#   Note that the large number, 1,260, has a comma in between the 
#   1 and 2, this is due to the --csv flag (comma separated value)
if __name__ == "__main__":   
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    parser.add_argument('-p', '--permute', dest='permute', action='store_true',
                       default=False, help='Whether to compute a permutation.')
    parser.add_argument('-c', '--choose', dest='choose', action='store_true',
                       default=False, help='Whether to compute a combination.')
    parser.add_argument('-r', '--repetition', dest='repetition', action='store_true',
                       default=False, help='Whether repetition is allowed\
                       (Default is false).')
    parser.add_argument('-a', '--add', dest='add', action='store_true',
                       default=False, help='Whether to add the results together at the end.')
    parser.add_argument('-m', '--mult', dest='mult', action='store_true',
                       default=False, help='Whether to multiply the results together at the end.')
    parser.add_argument('--values', dest='values', action='store', nargs='+', type=int,
                       help='The values to compute with the chosen operation.\
                       (Values should be entered in the order: n r )', 
                       required=True)
    parser.add_argument('--csv', dest='csv', action='store_true', default=False, 
                       help='Whether to print out the numbers with commas.')

    args = parser.parse_args()
    
    # initialize the class
    comb = Combinatorics()
    # holds the result of each permutation or combination added together
    allAdded = 0
    # holds the result of each permutation or combination multiplied together
    allMultiplied = 1
    
    for n, r in [(args.values[i], args.values[i+1]) for i in range (0, len(args.values), 2)]:
        msg = ""
        if args.permute:
            ans = comb.permute(n, r, args.repetition)
            print "P(%d,%d):" % (n, r)
        if args.choose:
            ans = comb.choose(n, r, args.repetition)
            print "C(%d,%d):" % (n, r)
        if args.csv:
            print "{:,}".format(ans)
        else:
            print ans
        allAdded += ans
        allMultiplied *= ans
        print ""
    # multiple permutations or combinations computed
    if args.add:
        if args.csv:
            print "All results added together:\n%s\n" % "{:,}".format(allAdded)
        else:
            print "All results added together:\n%d\n" % allAdded
    if args.mult:
        if args.csv:
            print "All results multiplied together:\n%s\n" % "{:,}".format(allMultiplied)
        else:
            print "All results multiplied together:\n%d\n" % allMultiplied
        
    # test code
    # print comb.permute(100000, 2, repetition=False)
    # print comb.choose(100000, 100000-1, repetition=False)
    # print comb.choose(10000, 32, repetition=True)
    