import argparse, string
from common.letter_counts import LetterCounts

class VigenereCipher:

    def __init__(self):
        self.letCounter = LetterCounts()
        self.ic = { "english" : 0.065, "equiprobable" : 0.038}
        # ic of english language
        self.engIC = 0.065
        # ic of perfectly random message (all letters equiprobable)
        self.ranIC = 0.038
        self.vigenereSquare = self.constructVigenereSquare()

    ## clearMsg
    #
    # cleans up the ciphertext so that it only contains
    # A-Z characterws
    #
    def clearMsg(self, msg):
        return msg.replace(' ', '')
    
    ## Index of Coincidence (IC)
    # The IC of the English Language is 0.065
    # The IC of a text written where all letters are
    # equiprobable is 0.038
    #
    # IC is equivalent to the sum from i=1 to 26
    # of c**2/n**2 where n is the length of the
    # string and c is the count of the letter 
    # (corresponding letter of the alphabet) in
    # the message
    #
    def calcIC(self, msg):
        # Determine the letter counts in the message
        counts = self.letCounter.getCounts(msg)
        
        # Determine the squared length of the message
        n = len(msg)**2
        
        # The IC (results from a summation)
        ic = 0
        for letter,num in counts:
            # Since some of the counts could be 0, skip those
            if num == 0:
                continue
            ic += num**2/float(n)
        
        return ic
     
    ## isMonoalphabetic
    # 
    # determines if the IC is closer to the English Language
    # IC or to the IC of text with equiprobable letter occurrence
    #
    # return: whether the IC is closer to english IC or not
    def isMonoalphabetic(self, ic):
        deltaEng = abs(self.ic["english"] - ic)
        deltaEqui = abs(self.ic["equiprobable"] - ic)
        
        return deltaEng > deltaEqui
    
    ## constructVigenereSquare
    #
    # The Vigenere Square is a mapping of the simple shifts performed
    # when encrypting a message using a Vigenere cipher keyword
    # 
    # In other words, keyword 'a' shifts letters by 0
    # so vigengereSquare['a']['c'] = 'C'
    def constructVigenereSquare(self): 
        alphabet = list(string.ascii_uppercase)
        lowerbet = list(string.ascii_lowercase)
        
        vigenereSquare = {}
        for shift, rowLet in enumerate(lowerbet):
            vigenereSquare[rowLet] = {}
            for idx, colLet in enumerate(lowerbet):
                vigenereSquare[rowLet][colLet] = alphabet[(idx+shift)%len(alphabet)]            
        return vigenereSquare
    
    ## vigenereSquareDecrypt
    #
    # c is the cipher letter (i.e. 'N')
    # p is the plaintext letter that the cipher letter
    #   is expected to correspond to (i.e. 'e')
    #
    def vigenereSquareDecrypt(self, c, p='e'):    
        for key, value in self.vigenereSquare[p].items():
            if value == c:
                return key
        return None
        
    ## vigenereSquareLookup
    #
    # k is the keyword letter (i.e. 'j')
    # p is the plaintext letter to encrypt (shift)
    # c is the ciphertext letter found via table lookup
    #
    def vigenereSquareLookup(self, k, p, printTable=False):
        return self.vigenereSquare[k][p]

    def encrypt(self, msg, key, printTable=False):
        keyLen = len(key)
        encryptedMsg = ""
        if printTable:
            print " __________________________________"
            print "| Keyword | Plaintext | Ciphertext |"
        for i in range(0, len(msg), keyLen):
            chunk = msg[i:i+keyLen]
            # encrypt using the vigenere square
            for chunkIdx in range(0, len(chunk)):
                keyLet = key[chunkIdx]
                msgLet = chunk[chunkIdx]
                cipherLet = self.vigenereSquareLookup(keyLet, msgLet)
                if printTable:
                    print "|    %s    |     %s     |      %s     | " % (keyLet, msgLet, cipherLet) 
                encryptedMsg += cipherLet
        if printTable:
            print "|__________________________________|"
            
        return encryptedMsg
        
    ## decrypt
    #
    # Decrypts a message using the key and the Vigenere Square
    #
    # msg is the message to decrypt
    # key is the key used to encrypt the message
    #
    def decrypt(self, msg, key, printTable=False):    
        keyLen = len(key)
        decryptedMsg = ""
        if printTable:
            print " __________________________________"
            print "| Keyword | Ciphertext | Plaintext |"
        for i in range(0, len(msg), keyLen):
            # slice out a chunk of the message (len <= size of key)
            chunk = msg[i:i+keyLen]
            # decrypt the chunk using the key
            for chunkIdx in range(0, len(chunk)):
                keyLet = key[chunkIdx]
                msgLet = chunk[chunkIdx]
                plainLet = self.vigenereSquareDecrypt(msgLet, keyLet)
                if printTable:
                    print "|    %s    |     %s     |      %s     | " % (keyLet, msgLet, plainLet) 
                decryptedMsg += plainLet
        if printTable:
            print "|__________________________________|"
        return decryptedMsg
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    parser.add_argument('-d', '--decrypt', dest='decrypt', action='store_true',
                       default=False, help='Whether to decrypt the message. \
                       (Default action is to encrypt the message.)')
    parser.add_argument('--st', '--showTable', dest='showTable', action='store_true',
                       default=False, help='Whether to show the entire encryption table for the vigenere square encryption.')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to encrypt or decrypt.', 
                       required=True)
    parser.add_argument('--split', dest='splitN', action='store', type=int,
                       default=5, help='The size of the split for encrypted plaintext.')
    parser.add_argument('--keyword', dest='keyword', action='store',
                       help='The key used to encrypt or decrypt.', 
                       required=False)

    args = parser.parse_args()
    
    args.msg = args.msg.replace(' ', '')
    
    # initialize the vignere cipher
    vigCi = VigenereCipher()
    
    if args.keyword and not args.decrypt:
        # encrypt using vigenere square!
        encryptedMsg = vigCi.encrypt(args.msg, args.keyword, args.showTable)
        print "\nEncrypted message:\n%s\n" % (encryptedMsg)    
    
    elif args.keyword and args.decrypt:
        # encrypt using vigenere square!
        decryptedMsg = vigCi.decrypt(args.msg, args.keyword, args.showTable)
        print "\nDecrypted message:\n%s\n" % (decryptedMsg)   
        
    
    # originalMsg = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"
    
    # msg = vici.clearMsg(originalMsg)
    
    # ic = vici.calcIC(msg)
    
    # isMono = vici.isMonoalphabetic(ic)
    
    # if isMono:
        # ""
    # else:
        # ""
        
    # print "Ciphertext:\n%s\n" % originalMsg
    # print "Index of Coincidence (IC): %0.4f\n" % ic
    # if isMono:
        # print "Message was likely encrypted using a monoalphabetic cipher"
    # else:
        # print "Message was likely encrypted using a polyalphabetic cipher"
    