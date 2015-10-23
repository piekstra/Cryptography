import argparse
from common.frequency_analysis import LetterFrequency, DigraphFrequency

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Decrypt a message that was encrypted using a monoalphabetic cipher.')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to decrypt.', 
                       required=True)
    parser.add_argument('--mfc', dest='mfc', action='store', nargs=2, type=str,
                       help='The two most frequent ciphertext letters.', required=False)
    parser.add_argument('--mfp', dest='mfp', action='store', nargs=2, type=str,
                       help='The two (most frequent) plaintext letters that the ciphertext letters are expected to be decrypted to based on frequency analysis.', 
                       required=False, default=['e', 't'])

    args = parser.parse_args()
    
    #ciphertext = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"
    
    print "Attempting to decipher:\n", ciphertext, "\n"

    # get the letter frequencies
    letFreq = LetterFrequency()
    (freqDict, freqTuples) = letFreq.getFrequencies(ciphertext)
    print "Letter Frequencies:\n", freqTuples, "\n"

    # If most frequent letters in ciphertext were override by manual
    # user arguments then use those user-specified letters
    if args.mfc is not None:
        # most frequent letter in ciphertext
        cMostFreq1 = args.mfc[0]
        cMostFreq2 = args.mfc[1]
    # set most and second most frequent letter in ciphertext
    else:
        cMostFreq1 = frequencies[0][0]        
        cMostFreq2 = frequencies[1][0]

    print "Most frequent letter in ciphertext:", cMostFreq1
    print "\twith frequency: %.2f%%" % frequencies[0][1]
    print "Second most frequent letter in ciphertext:", cipherLetter2
    print "\twith frequency: %.2f%%\n" % frequencies[1][1]

    # assume that the two most frequent letters are 'e' and 't' respectively
    # unless manual guesses are specified via command line
    if len(sys.argv) <= 1:
        mostFreq = 'e'
        secondMostFreq = 't'
    else:
        mostFreq = sys.argv[1]
        secondMostFreq = sys.argv[2]

    print "Assuming that", cipherLetter1, "is equivalent to", mostFreq
    print "Assuming that", cipherLetter2, "is equivalent to", secondMostFreq, "\n"

    # quick lookup table of multiplicative inverses for integers mod 26
    multiplicativeInverse = {
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

    # initialize the variables to the mod 26 equivalents of the letters
    # plaintext characters
    p1 = ord(mostFreq) - 96
    p2 = ord(secondMostFreq) - 96
    # ciphertext characters
    c1 = ord(cipherLetter1.lower()) - 96
    c2 = ord(cipherLetter2.lower()) - 96

    lhs = (p2 - p1)
    rhs = (c2 - c1) % 26

    s = -1
    for multKey in multiplicativeInverse.keys():
        if lhs * multKey % 26 == rhs:
            s = multKey
            break
    if s == -1:
        print "ERROR: could not find multiplicative key"
        sys.exit(-1)
        
    rhs = c1 - s*p1%26
    if rhs < 0:
        rhs += 26

    r = -1
    for addKey in range (0, 26):
        if addKey * s % 26 == rhs:
            r = addKey
            break
    if r == -1:
        print "ERROR: could not find additive key"
        sys.exit(-1)

    # key is s, r
    key = (s, r)
    print "Key:", key, "\n"

    plaintext = ""
    for ch in ciphertext.lower():
        if ch == ' ':
            continue
        else:
            cipherInt = ((ord(ch) - 96)*multiplicativeInverse[key[0]] - key[1]) % 26
            # cover the 'z' case
            if cipherInt == 0:
                cipherInt = 26
            plaintext += chr(cipherInt + 96)

    print "Plaintext:\n", plaintext



