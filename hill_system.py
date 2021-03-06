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
            encryptedMatrix = self.matrixOps.matrixMult(key, [[self.letToInt(char, zeroSystem)] for char in block])
            for encryptedRow in encryptedMatrix:
                cipherInt = encryptedRow[0] % 26
                
                # cover the 'z' case
                if cipherInt == 0 and not zeroSystem:
                    cipherInt = 26
                encryptedMsg += self.intToLet(cipherInt, zeroSystem)
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
        return filter(lambda tup: (a1*tup[0] + b1*tup[1]) % 26 == c1 and (a2*tup[0] + b2*tup[1]) % 26 == c2, [(x,y) for x in range (26) for y in range(26)])               
        
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
        return sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)
    
    def letToInt(self, let, zeroSystem=False):
        return ord(let.lower()) - 96 - (1 if zeroSystem else 0)
        
    def intToLet(self, int, zeroSystem=False):
        return chr(int+96 + (1 if zeroSystem else 0))
    
    ## psuedo algorithm/code for discovering the potential key matrices
    # find the most frequent digraph
    #   assume the digraph maps to 'th'
    #   create a set of constants for the linear equations using the numeric values of
    #       each letter
    #   i.e. 'OT' mapping to 'th' would produce (14, 19, 19) and (14, 19, 7) using a zero_system
    # get the list of digraphs that follow the most frequent digraph
    #   create a list of constants tuples assuming that these digraphs map to 'e*'
    #   i.e. 'GW' mapping to 'e*' would produce (6, 22, 4) using the zero_system
    # solve for x,y in the pairs of linear equations for ax + by = c where c is the integer
    # representation of 't' or 'e' depending on the equation
    #   these are the potential solutions mapping the first letter of the digraph
    #   to 't' and assuming that 'e' follows the letter after 't'
    # from all of the possible keys, if the same key shows up as a solution to each
    # equation, or it simply shows up more frequently than other keys for (a, b) then
    #   use that key for a and b
    # get a list of possible keys for cx + dy = e where e is the integer representation of 'h'
    # run through the 1 or 2 best keys for a, b and all of the keys for c, d and decipher
    # the ciphertext using them.
    # Look at the output and try to find the english one
    def super_decrypt(self, msg, digraphOverride=None, zeroSystem=False):
        diFreq = DigraphFrequency()
        letFreq = LetterFrequency()
        if digraphOverride is None:
            (mfd, mfdf) = diFreq.getFrequencies(msg)[1][0]
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
        mostLikelyABValues = self.mostFreqIntPairs(abPossibleValues)
        bestABValues = []
        for abValue, count in mostLikelyABValues:
            # if the abValue works for all equations, it is very likely
            # that it is the correct values for a and b
            if count == len(followingDigraphConstants):
                bestABValues.append(abValue)
        # if there are still no abValues 
        #   (i.e. no a, b pair works for all of the equations
        #   created by assuming that the digraphs following the mfd correspond to 'e*')
        # then just pick the top 2        
        if not bestABValues:
            bestABValues = mostLikelyABValues[:2]
            
        # if there are two a,b pairs to try out, do the following
        if len(bestABValues) > 1:
            # of the two most likely values for both a and b, go through every digraph in the message
            # and determine the int value of a1x+b1y, and a2x + b2y where x and y are the two letters
            # in the digraph and a1,b1 and a2,b2 are the abValues
            # convert the resulting int values to letters, and see which key pair produced the more
            # frequent letter
            # keep a running tally of the more frequent letters for each pair to see which one is
            # more likely to be the actual key
            key1 = bestABValues[0][0]
            key2 = bestABValues[1][0]
            msgDigraphs = diFreq.getUniqueDigraphs(msg)
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
            # try the more likely key first!
            abKeys = [key1, key2] if key1MoreFreqCounter > key2MoreFreqCounter else [key2, key1]
            print "Key %s is the more likely of the keys %s and %s" % (abKeys[0], key1, key2)
        # there is only one AB value, so it must be the correct key pair for a,b!!!
        else:
            abKeys = bestABValues
            
        # find possible values for c and d that solve the equation
        cdConsts = mfdConsts[1]
        cdKeys = self.solveLinEqu(cdConsts)
        
        ## print out a description of the progress thus far
        if digraphOverride is None:
            print "\nThe most frequent digraph (MFD) in the message was:\n\t%s' with frequency %0.2f%%" % (mfd, mfdf)
        else:
            print "\nThe most frequent digraph (MFD) in the message was manually set as:\n\t%s'" % (mfd)
            
        print "\nMapping '%s' to 'th' resulted in the following equations:\n\t%da + %db = %d\n\t%dc + %dd = %d" % (mfd, abConsts[0], abConsts[1], abConsts[2], cdConsts[0], cdConsts[1], cdConsts[2])
        print "\nLooking at digraphs following '%s' resulted in the following digraphs:\n\t%s" % (mfd, followingDigraphs)
        print "\nMapping the above digraphs to 'e*' resulted in the following equations:"
        for fdc in followingDigraphConstants:
            print "\t%da + %db = %d" % (fdc[0], fdc[1], fdc[2])        
        print "\nSolving for 'a' and 'b' in these equations resulted in the following most\nlikely key(s):"
        for abKey in abKeys:
            print "\ta = %d, b = %d" % (abKey[0], abKey[1])
        print "\nSolving for 'c' and 'd' in the original set of equations resulted in the\nfollowing most likely key(s):"
        for cdKey in cdKeys:
            print "\tc = %d, d = %d" % (cdKey[0], cdKey[1])        
        print "\nThese keys as matrices in the form [[a, b], [c, d]] will now be brute forced so \nthat the user can attempt to spot the correct deciphering of the ciphertext.\n\n"
            
        for abKey in abKeys:
            for cdKey in cdKeys:
                key = [list(abKey), list(cdKey)]
                print "Trying decryption key: %s, encryption key %s" % (key, self.matrixOps.invertMatrix(key))
                print self.decrypt(msg, key, False, zeroSystem)
                #print "DKEY: %s, EKEYy %s  -> %s" % (key, self.matrixOps.invertMatrix(key),self.decrypt(msg, key, False, zeroSystem))
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
    
    msg = args.msg.replace(' ', '').upper()
    
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
        print "Decrypting message:\n%s\n" % msg
        print "Note:\n\tIf the program fails, it MAY work if you add a '-z' flag to the program call"
        cryptoSystem.super_decrypt(msg, args.mfd, args.zero_system)
        