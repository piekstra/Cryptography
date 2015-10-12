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

if __name__ == "__main__":   
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    parser.add_argument('-p', '--permute', dest='permute', action='store_true',
                       default=False, help='Whether to compute a permutation.')
    parser.add_argument('-c', '--choose', dest='choose', action='store_true',
                       default=False, help='Whether to compute a combination.')
    parser.add_argument('-r', '--repetition', dest='repetition', action='store_true',
                       default=False, help='Whether repetition is allowed\
                       (Default is false).')
    parser.add_argument('--values', dest='values', action='store', nargs='+', type=int,
                       help='The values to compute with the chosen operation.\
                       (Values should be entered in the order: n r )', 
                       required=True)

    args = parser.parse_args()
    
    # initialize the class
    comb = Combinatorics()
    
    n = args.values[0]
    r = args.values[1]
    
    if args.permute:
        print comb.permute(n, r, args.repetition)
    if args.choose:
        print comb.choose(n, r, args.repetition)
    
    # test code
    # print comb.permute(100000, 2, repetition=False)
    # print comb.choose(100000, 100000-1, repetition=False)
    # print comb.choose(10000, 32, repetition=True)
    