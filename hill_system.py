import string, argparse, math, itertools, operator
from common.matrix_operations import MatrixOperations
from common.frequency_analysis import DigraphFrequency, LetterFrequency

class HillSystem:

    def __init__(self):            
        # initialize a string of chars that cannot be encrypted
        self.illegalChars = string.punctuation + ' ' 
        # initialize the character used to pad messages to fit the blocks
        self.padChar = 'x'
        # create a reference to the matrix operations
        self.matrixOps = MatrixOperations()
        # array of units
        self.units = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
       
    def encrypt(self, msg, key, decrypt=False, zeroSystem=False):
        keyDim = len(key)
        msg = msg.lower().translate(string.maketrans("", ""), self.illegalChars)
        # determine if we need to pad 'x's at the end of the msg to make it fill a block
        numToFill = (keyDim - (len(msg) % keyDim)) % keyDim
        msg += numToFill * self.padChar
        encryptedMsg = ""
        for block in [msg[i:i+keyDim] for i in range(0,len(msg),keyDim)]:
            encryptedMatrix = self.matrixOps.matrixMult(key, [[ord(char)-96] for char in block])
            for encryptedRow in encryptedMatrix:
                cipherInt = (encryptedRow[0] - (1 if zeroSystem else 0)) % 26
                # cover the 'z' case
                if cipherInt == 0:
                    cipherInt = 26
                encryptedMsg += chr(cipherInt+96)
        return encryptedMsg if decrypt else encryptedMsg.upper()
    
    def decrypt(self, msg, key, invertKey=False, zeroSystem=False):
        # remove spaces from the message
        msg = ''.join(msg.split())
        # invert the key for decryption of the msg
        if invertKey:
            return self.encrypt(msg.lower(), self.matrixOps.invertMatrix(key), zeroSystem=zeroSystem, decrypt=True)
        return self.encrypt(msg.lower(), key, zeroSystem=zeroSystem, decrypt=True)
        
    # The parameters are tuples of the constants
    # for each equation in the form
    # ax + by = c(mod 26)
    # where a, b, and c are the constants in the 
    # parameter tuples
    def solveLinEquPair(self, equConstants1, equConstants2):
        (a1, b1, c1) = equConstants1
        (a2, b2, c2) = equConstants2
        
        xySols = []
        for x in range(0, 26):
            for y in range(0, 26):
                if (a1*x + b1*y) % 26 == c1 and (a2*x + b2*y) % 26 == c2:
                    xySols.append((x, y))
                    
        return xySols
        
    # The parameters are tuples of the constants
    # for each equation in the form
    # ax + by = c(mod 26)
    # where a, b, and c are the constants in the 
    # parameter tuples
    def solveLinEqu(self, equConstants):
        (a, b, c) = equConstants
        
        return filter(lambda tup: (a*tup[0] + b*tup[1]) % 26 == c, [(x,y) for x in range (26) for y in range(26)])

    def diAndKeyToLet(self, digraph, key, zeroSystem):
        d1Int = self.letToInt(digraph[0], zeroSystem)
        d2Int =  self.letToInt(digraph[1], zeroSystem)
        letterInt = (d1Int*key[0] + d2Int*key[1]) % 26
        return self.intToLet(letterInt, zeroSystem)
    
    # intPairs is a list of lists of 2-tuples
    def mostFreqIntPairs(self, intPairs):
        flatList = list(itertools.chain(*intPairs))
        # count pair frequencies
        freqDict = {}
        for pair in flatList:
            if pair in freqDict:
                freqDict[pair] += 1
            else:
                freqDict[pair] = 1
        
        return map(lambda x: x[0], sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True))
    
    def letToInt(self, let, zeroSystem=False):
        return ord(let.lower()) - 96
        
    def intToLet(self, int, zeroSystem=False):
        return chr(int+96 + (1 if zeroSystem else 0))
    
    ## psuedo algorithm/code for discovering the potential key matrices
    # find the most frequent digraph
    #       allow command line option to specify the digraph that is 'most frequent'
    # assume the digraph maps to 'th'
    #   create a set of constants for the linear equations using the numeric values of
    #       each letter
    #   i.e. 'OT' mapping to 'th' would produce (14, 19, 19) and (14, 19, 7) using a zero_system
    # get the list of digraphs that follow the most frequent digraph
    #   create a list of constants tuples assuming that these digraphs map to 'e*'
    #   i.e. 'GW' mapping to 'e*' would produce (6, 22, 4) using the zero_system
    # ...
    def super_decrypt(self, msg, digraphOverride=None, zeroSystem=False):
        diFreq = DigraphFrequency()
        letFreq = LetterFrequency()
        if digraphOverride is None:
            mfd = diFreq.getFrequencies(msg)[1][0][0]
        else:        
            # most frequent digraph
            mfd = digraphOverride
        mfdIntsTuple = diFreq.digraphToIntTuple(mfd, zeroSystem)
        mfdConsts = [mfdIntsTuple + (diFreq.letToInt('t', zeroSystem),), 
                    mfdIntsTuple + (diFreq.letToInt('h', zeroSystem),)]   
        followingDigraphs = diFreq.getFollowingDigraphs(msg, mfd)
        followingDigraphConstants = [diFreq.digraphToIntTuple(diTup, zeroSystem) + (diFreq.letToInt('e', zeroSystem),) for diTup in followingDigraphs]
        # the possible values of a and b in the key matrix:
        # a b
        # c d        
        abConsts = mfdConsts[0]
        abPossibleValues = [self.solveLinEquPair(abConsts, folDiConsts) for folDiConsts in followingDigraphConstants]
        twoMostLikelyABValues = self.mostFreqIntPairs(abPossibleValues)[:2]
        # of the two most likely values for both a and b, go through every digraph in the message
        # and determine the int value of a1x+b1y, and a2x + b2y where x and y are the two letters
        # in the digraph and a1,b1 and a2,b2 are the abValues
        # convert the resulting int values to letters, and see which key pair produced the more
        # frequent letter
        # keep a running tally of the more frequent letters for each pair to see which one is
        # more likely to be the actual key
        key1 = twoMostLikelyABValues[0]
        key2 = twoMostLikelyABValues[1]
        msgDigraphs = diFreq.getDigraphs(msg)
        key1Lets = [self.diAndKeyToLet(digraph, key1, zeroSystem) for digraph in msgDigraphs]
        key2Lets = [self.diAndKeyToLet(digraph, key2, zeroSystem) for digraph in msgDigraphs]
        
        englishLetterFrequenciesDict = letFreq.getStandardFrequencies()[0]
        key1MoreFreqCounter = 0
        key2MoreFreqCounter = 0
        for i in range(0, len(key1Lets)):
            if englishLetterFrequenciesDict[key1Lets[i]] > englishLetterFrequenciesDict[key2Lets[i]]:
                key1MoreFreqCounter += 1
            else:
                key2MoreFreqCounter += 1
        abKey = key1 if key1MoreFreqCounter > key2MoreFreqCounter else key2
        print "Key %s is the more likely of the keys %s and %s" % (abKey, key1, key2)
        # find possible values for c and d that solve the equation
        cdConsts = mfdConsts[1]
        cdKeys = self.solveLinEqu(cdConsts)
        for cdKey in cdKeys:
            key = [list(abKey), list(cdKey)]
            print "Trying key: %s" % key
            print self.decrypt(msg, key, False, zeroSystem)
        # brute force the potential keys using the values of [[a, b], [c,d]]
        
        
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    parser.add_argument('-d', '--decrypt', dest='decrypt', action='store_true',
                       default=False, help='Whether to decrypt the message. \
                       (Default action is to encrypt the message.)')
    parser.add_argument('-i', '--invert', dest='invert', action='store_true',
                       default=False, help='Whether to invert the key. \
                       (Default action is to not invert the key.)')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to encrypt or decrypt.', 
                       required=True)
    parser.add_argument('--split', dest='splitN', action='store', type=int,
                       default=5, help='The size of the split for encrypted plaintext.')
    parser.add_argument('--key', dest='key', action='store', nargs='+', type=int,
                       help='The key used to encrypt or decrypt.', 
                       required=False)
    parser.add_argument('--mfd', dest='mfd', action='store', type=str,
                       help="The proposed 'most frequent digraph'. (Allows for an override of the actual most frequent digraph.)", 
                       required=False, default=None)
    parser.add_argument('-z', '--zero', dest='zero_system', action='store_true',
                       default=False, required=False, help='Whether to use a modulo 26 system where a is 0 and z is 25 or where a is 1 and z is 26 the key.')

    args = parser.parse_args()
    
    # Initialize the crypto system
    cryptoSystem = HillSystem()    
    
    msg = args.msg.replace(' ', '')
    
    if args.key:
        #key = [[3,2], [8,5]]
        # the 'dimension' of the array is the square root of the length since it
        # is a square matrix
        arrDim = int(math.sqrt(len(args.key)))
        # Initialize the key (The argument is a 1D array it needs to be converted
        # into a square matrix)
        key = [args.key[i:i+arrDim] for i in range(0, len(args.key), arrDim)]
        
        # Initialize the message to encrypt or decrypt
        #msg = "MUBYA QIQGN AEWOS RZQJI RZQKC LIZAG SXCJA AQFRM HO"
        
        if not args.decrypt:
            print "Encrypting message:\n%s\n" % msg
            print "Using key:\n%s\n" % key
            ciphertext = cryptoSystem.encrypt(msg, key)
            splitText = ' '.join(ciphertext[i:i+args.splitN] for i in range(0, len(ciphertext), args.splitN))
            print "Ciphertext:\n%s\n" % splitText
        else:
            print "Decrypting message:\n%s\n" % msg
            print "Using key:\n%s\n" % key
            plaintext = cryptoSystem.decrypt(msg, key, invertKey=args.invert)
            print "Plaintext:\n%s\n" % plaintext
    else:
        cryptoSystem.super_decrypt(msg, args.mfd, args.zero_system)
        