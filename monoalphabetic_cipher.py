import argparse
from common.frequency_analysis import LetterFrequency, DigraphFrequency

class MonoalphabeticCipher:

    ## __init__
    #
    # The constructor
    #
    def __init__(self):
        self.multInv = {
            1:1,
            3:9,
            5:21,
            7:15,
            9:3,
            11:19,
            15:7,
            17:23,
            19:11,
            21:5,
            23:17,
            25:25
        }        
    
    def letToInt(self, let):
        return ord(let.lower()) - 96

    ## getAffineKey
    #
    # Using the algorithm from "Cryptological Mathematics" by 
    # Robert Edward Lewand on page 38
    #
    # Suppose it is known for an affine cipher with additive key r 
    # and multiplicative key s, that plaintext position p1 maps into
    # ciphertext position c1 and plaintext position p2 maps into 
    # ciphertext position c2. 
    # 
    # Then: s(r + p1) = c1(mod 26) and s(r + p2) = c2(mod 26)
    # => s(r + p1 - r1 - p2) = c1 - c2(mod 26)
    # => s(p1 - p2) = c1 - c2(mod 26)
    #
    def getAffineKey(self, p1, p2, c1, c2):
        lhs = (p2 - p1)
        rhs = (c2 - c1) % 26
        
        s = -1
        for multKey in self.multInv.keys():
            if lhs * multKey % 26 == rhs:
                s = multKey
                break
        if s == -1:
            print "ERROR: could not find multiplicative key\n"
            return None
            
        rhs = c1 - s*p1%26
        if rhs < 0:
            rhs += 26

        r = -1
        for addKey in range (0, 26):
            if addKey * s % 26 == rhs:
                r = addKey
                break
        if r == -1:
            print "ERROR: could not find additive key\n"
            return None

        # key is s, r
        key = (s, r)
        print "Key:", key, "\n"
        return key
        
    ## decrypt
    #
    # @param self - The object pointer
    # @param msg - The message to decrypt
    # @param mfc - The two most frequent ciphertext letters
    # @param mfp - The two most frequent plaintext letters
    #
    def decrypt(self, msg, mfc=None, mfp=None, verbose=False, showDigraphFrequencies=False):
        # remove spaces from the message
        msg = ''.join(msg.split())        
        if verbose: print "Attempting to decipher:\n", msg, "\n"
        
        # get the message and default letter frequencies
        letFreq = LetterFrequency()
        (freqDict, freqTuples) = letFreq.getFrequencies(msg)
        (stdDict, stdTuples) = letFreq.getStandardFrequencies()
        
        # if the mfc or mfp are None, use the top two most frequent letters
        # in the ciphertext and english language respectively as defaults
        mfc = tuple(mfc) if mfc else (freqTuples[0][0], freqTuples[1][0])        
        mfp = tuple(mfp) if mfp else (stdTuples[0][0], stdTuples[1][0])      
        
        if verbose: 
            print "Ciphertext Letter Frequencies:\n%s\n" % freqTuples
            print "English Language Letter Frequencies:\n%s\n" % stdTuples 
            if showDigraphFrequencies:
                diFreq = DigraphFrequency()
                diFreqTuples = diFreq.getFrequencies(msg)[1]
                diStdTuples = diFreq.getStandardFrequencies()[1]
                print "Ciphertext Digraph Frequencies:\n%s\n" % diFreqTuples
                print "English Language Digraph Frequencies:\n%s\n" % diStdTuples 
                
            print "Using letter in ciphertext: %s" % mfc[0]
            print "\twith frequency: %.2f%%" % freqDict[mfc[0]]
            print "Using letter in ciphertext: %s" % mfc[1]
            print "\twith frequency: %.2f%%\n" % freqDict[mfc[1]]

            print "Assuming that", mfc[0], "is equivalent to", mfp[0]
            print "Assuming that", mfc[1], "is equivalent to", mfp[1], "\n"
        
        # get the affine key using the mfc letters and mfp letters
        key = self.getAffineKey(*tuple(map(self.letToInt, mfp+mfc)))
        
        if key is None:
            print "Unable to decipher using '%s'->'%s' and '%s'->'%s'\n" % (mfc[0], mfp[0], mfc[1], mfp[1])
            return None
        
        # Use the key to decrypt
        plaintext = ""
        for ch in msg.lower():
            cipherInt = ((ord(ch) - 96)*self.multInv[key[0]] - key[1]) % 26
            # cover the 'z' case
            if cipherInt == 0:
                cipherInt = 26
            plaintext += chr(cipherInt + 96)
        
        return plaintext
        
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Decrypt a message that was encrypted using a monoalphabetic cipher.')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to decrypt.', 
                       required=True)
    parser.add_argument('--mfc', dest='mfc', action='store', nargs=2, type=str,
                       help='The two most frequent ciphertext letters.', required=False, default=None)
    parser.add_argument('--mfp', dest='mfp', action='store', nargs=2, type=str,
                       help='The two (most frequent) plaintext letters that the ciphertext letters are expected to be decrypted to based on frequency analysis.', 
                       required=False, default=['e', 't'])
    parser.add_argument('--sdf', dest='sdf', action='store_true', 
                       help="Whether to show the digraph frequencies of the ciphertext and the English Language.", 
                       required=False, default=False)
                       
    args = parser.parse_args()
    
    #ciphertext = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"
    
    monCi = MonoalphabeticCipher()
    plaintext = monCi.decrypt(args.msg, args.mfc, args.mfp, verbose=True, showDigraphFrequencies=args.sdf)
    if plaintext:
        print "Plaintext:\n", plaintext
    else:
        print "Could not decrypt the message"


