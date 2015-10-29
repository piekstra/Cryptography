import argparse
from polyalphabetic_cipher import PolyalphabeticCipher
from monoalphabetic_cipher import MonoalphabeticCipher
from vigenere_cipher import VigenereCipher
from common.frequency_analysis import LetterFrequency
from common.kasiski_test import KasiskiTest
from hill_system import HillSystem

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fully analyze, classify, and attempt to decrypt a message!')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to analyze.', 
                       required=True)
    parser.add_argument('--kl', dest='keyLen', action='store', type=int,
                       help='The key length (override).', required=False)
    parser.add_argument('--key', dest='key', action='store',
                       help='The key (override).', required=False)
    parser.add_argument('--ldpc', dest='letDispPerCol', action='store', type=int,
                       help='The number of letters displayed per column (override, default 6).', required=False)

    args = parser.parse_args()
    
    polyCi = PolyalphabeticCipher()
    monCi = MonoalphabeticCipher()
    vigCi = VigenereCipher()

    # 1. Find the Index of Coincidence and use it to decide which are most likely monoalphabetic (Note: I have specifically chosen messages so the IC is a good indicator of whether the message is monoalphabetic).
    msg = args.msg.replace(' ', '')
    msgIC = polyCi.calcIC(msg)
    isPoly = polyCi.isPolyalphabetic(msgIC)

    print "\nAnalyzing message: %s\n" % (msg)
    print "Message IC: %.4f" % msgIC
    print "Message is likely %s" % ("polyalphabetic" if isPoly else "monoalphabetic")
    mostLikelyKeyIC = polyCi.getKeywordLength(len(msg), msgIC)
    print "Most likely key length using IC test: %0.4f\n" % (mostLikelyKeyIC)

    # 3. For the ones which you suspect aren't monoalphabetic, they have been encrypted either using a Vignere cipher or Hills system. In order to differentiate, we shall apply the standard Vignere tests for keyword - the messages have specifically been chosen so that a Hills system message will be recognizable by how these tests perform. 
    if isPoly:
        # (a) Find all repeated strings of lengths 3 or more and apply the Kasiski test.
        kt = KasiskiTest()        
        kasiskiFailed = False
        repeatedSubstrs = kt.getRepeatedSubstrs(msg, 3)     
        if repeatedSubstrs:
            print "Repeated substrs of length >= 3:\n%s\n" % repeatedSubstrs
            
            print "Potential keys determined by running Kasiski test on each substring:"
            # print out potential key lengths for every substring
            # for keyLens in kt.getAllPotentialKeyLens(msg, repeatedSubstrs):
                # print keyLens
                
            mostLikelyKeysKasiski = kt.getMostLikelyKeyLens(msg, repeatedSubstrs)
            print "\nMost likely key lengths using Kasiski test:\n%s\n" % (mostLikelyKeysKasiski)
            
            # If the user manually overrode the key length from the command line, use it only
            if args.keyLen:
                mostLikelyKeysKasiski = [args.keyLen]
            # initialize the letter frequency class
            letFreq = LetterFrequency()
            
            # loop through the top 4 most likely key lengths according to the kasiski test
            for keyLen in mostLikelyKeysKasiski[:2]:
                # Split the message into keyLen columns        
                msgColumns = polyCi.msgSplit(msg, keyLen)
                # holds the potential keyword
                keyword = ""
                # perform frequency analysis on each column
                letsPerCol = 6 if not args.letDispPerCol else args.letDispPerCol
                print "Using the Vigenere Square on the top %d most frequent letters in each column assuming that each corresponds to 'e' results in the following options:" % (letsPerCol)       
                for idx, column in enumerate(msgColumns):
                    # get the most frequent letter in the column
                    columnFrequencies = letFreq.getFrequencies(''.join(column))[1]
                    mostFrequentLetTuple = columnFrequencies[0]
                    mostFreqLet = mostFrequentLetTuple[0]
                    # for tuple in columnFrequencies[:4]:
                        # print vigCi.vigenereSquareDecrypt(tuple[0], 'e')
                    # print "options above"
                    print "Column", idx+1, [vigCi.vigenereSquareDecrypt(tuple[0], 'e') for tuple in columnFrequencies[:letsPerCol]]
                    # assuming this letter corresponds to 'e', use the vigenere square
                    # to discover the original keyword letter
                    keywordLet = vigCi.vigenereSquareDecrypt(mostFreqLet, 'e')
                    keyword += keywordLet                
                    # If the user manually overrode the key from the command line, simply use it
                if args.key:
                    keyword = args.key
                print "\nPotential keyword: %s" % keyword
                print "Message deciphered using keyword '%s':\n%s\n" % (keyword, vigCi.decrypt(msg,keyword))
        else:
            print "\nKasiski test failed (no repeated substrings with length >= 3)"
            kasiskiFailed = True
        if kasiskiFailed:
            print "\nAssuming that message was enciphered using a hill cipher."
            HillSystem().super_decrypt(msg, None, zeroSystem=True)
        
    # 2. For the ones which you guess to be monoalphabetic, do the following:
    else:
        # (a) Run frequency analysis to determine which letters most likely correspond to "e" and "t".
        # (b) Use these correspondences to find the key. 
        # (c) Decrypt the message.        
        plaintext = monCi.decrypt(msg, verbose=True)
        print "Decoded monoalphabetic message: %s" % plaintext 