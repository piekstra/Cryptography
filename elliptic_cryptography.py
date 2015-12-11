import sys, argparse

class EllipticCurve:    

    def __init__(self, A, B, modp):
        # check to make sure it is a valid elliptic curve
        if 4*A**3 + 27*B**2 == 0:
            print "y^2 = x^3 + %dx + %d over Z_%d is NOT an elliptic curve" % (A, B, modp)
            sys.exit(-1)            
        print "y^2 = x^3 + %dx + %d over Z_%d is a valid elliptic curve" % (A, B, modp)
       
        self.INF = (float("inf"), float("inf"))
        self.A = A
        self.B = B
        self.modp = modp
    

    def onCurve(self, P):
        x, y = P
        return self.mod(y**2) == self.mod(x**3 + self.A*x + self.B)
    
    
    def getAllPoints(self):
        return sorted([(x, y) for x in range(self.modp) for y in range(self.modp) if self.onCurve((x, y))], key=lambda p: p[1])
        
        
    ## multiplicative inverse
    def multInv(self, num):
        for i in range(self.modp):
            if self.mod(num*i) == 1:
                return i
        # not a unit
        return -1
        
        
    ## additive inverse of a number
    def addInv(self, num):
        return self.modp - num
        
        
    ## additive inverse of a point (also known as the 'negative' of a point)
    def addInvP(self, P):
        x, y = P
        return (x, self.mod(-y))
    
    
    def mod(self, num):
        if num < 0:
            return self.addInv((-num) % self.modp)
        return num % self.modp
            
            
    def addPoints(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = self.INF
            
        if x1 != x2:
            m = self.mod((y2 - y1) * self.multInv(x2 - x1))        
        elif p1 == p2 and y1 != 0:
            m = self.mod((3*x1**2 + self.A) * self.multInv(2*y1))
        else:
            return self.INF
            
        x3 = m**2 - x1 - x2
        y3 = -(y1 + m*(x3 - x1))
        
        return (self.mod(x3), self.mod(y3))        
    
    
    def discreteLog(self, base, point):
        newP = base
        for i in range(1,self.modp):
            if newP == point:
                return i
            newP = self.addPoints(newP, base)
        return -1
    
    
    def nP(self, n, P):
        return reduce(self.addPoints, [P]*n)
        
##
#   Running the program!
#       Required Parameters: 
#           --A       in the curve y^2 = x^3 + Ax + B
#           --B       in the curve y^2 = x^3 + Ax + B
#           --modp    F_p or Z_p where p is prime
#
#       Calculator Options (Optional Parameters): 
#
#           Is valid elliptic curve?
#               NO EXTRA PARAMETERS    
#           All Points on curve
#               NO EXTRA PARAMETERS    
#
#           Additive Inverse / Negative of POINT
#               --point     Point POINT
#           Is POINT on the elliptic curve?
#               --point     Point POINT
#
#           P + Q
#               --P     Point P
#               --Q     Point Q
#           nP
#               --n     The number of times to add P to itself
#               --P     Point P
#
#           discrete log of POINT with base BASE
#               --base     Base BASE
#               --point    Point POINT
#
##            
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Elliptic Curve Cryptography!')
    parser.add_argument('--modp', dest='modp', action='store', type=int,
                       help='The modulo prime (Field size F_p || Integers modulo p Z_p)', 
                       required=True)
    parser.add_argument('--A', dest='A', action='store', type=int,
                       help='The A in the curve: y^2 = x^3 + Ax + B', 
                       required=True)
    parser.add_argument('--B', dest='B', action='store', type=int,
                       help='The B in the curve: y^2 = x^3 + Ax + B', 
                       required=True)
    parser.add_argument('--base', dest='base', action='store', nargs=2, type=int,
                       help='The base (for finding the discrete logarithm of a point)', 
                       required=False)
    parser.add_argument('--point', dest='point', action='store', nargs=2, type=int,
                       help='The point to find the discrete logarithm of (need a base)', 
                       required=False)
    parser.add_argument('--P', dest='P', action='store', nargs=2, type=int,
                       help='A point on the elliptic curve (for adding two points)', 
                       required=False)
    parser.add_argument('--Q', dest='Q', action='store', nargs=2, type=int,
                       help='A point on the elliptic curve (for adding two points)', 
                       required=False)
    parser.add_argument('--n', dest='n', action='store', type=int,
                       help='A value to calculate nP (P + P + P + ... + P) n-times', 
                       required=False)

    args = parser.parse_args()     
    if args.base: args.base = tuple(args.base)
    if args.point: args.point = tuple(args.point)
    if args.P: args.P = tuple(args.P)
    if args.Q: args.Q = tuple(args.Q)
    
    print ""
    ec = EllipticCurve(args.A, args.B, args.modp)   
    print ""
    
    if args.base:
        if args.point:
            print "The discrete log of %s with base %s is %d" % (args.point, args.base, ec.discreteLog(args.base, args.point))
    elif args.point:
            print "The additive inverse of %s is %s" % (args.point, ec.addInvP(args.point)) 
            print "P is %son the elliptic curve" % ("" if ec.onCurve(args.point) else "NOT ")
    elif args.P:        
        if args.Q:
            print "P%s + Q%s = R%s" % (args.P, args.Q, ec.addPoints(args.P, args.Q))
        elif args.n:
            print "nP where n = %d and P = %s is: %s" % (args.n, args.P, ec.nP(args.n, args.P))
    else:
        print "All points on the curve y^2 = x^3 + %dx + %d over Z_%d:" % (args.A, args.B, args.modp)   
        for point in ec.getAllPoints():
            x, y = point
            print "\ty = %d and x = %d" % (y, x)