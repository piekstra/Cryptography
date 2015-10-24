import string
from common.letter_frequency import LetterFrequency

class PolyalphabeticCipher:

    def __init__(self):
        # ic of english language
        self.engIC = 0.065
        # ic of perfectly random message (all letters equiprobable)
        self.ranIC = 0.038
        self.vigenereSquare = self.constructVigenereSquare()
    
    ## getLetCounts
    #
    # Gets the counts of each letter of the alphabet in the message
    #
    # returns a dictionary mapping letters to their counts
    #
    def getLetCounts(self, msg):    
        return {ch : msg.count(ch) for ch in string.ascii_uppercase}
    
    ## calcIC
    #
    # The index of coincidence indicates the likelihood of a message
    # being encrypted using a monoalphabetic or polyalphabetic cipher.
    #
    # The IC of the English Language is:
    #   0.065
    # The IC of a message where all letters are equiprobable is:
    #   0.038
    #
    # IC is equivalent to the sum from i=1 to 26 of ni^2/n^2
    #   where n is the length of the message
    #   and ni is the number of times the corresponding letter occurs
    #       n1 is count of a's in the message, 
    #       n2 is count of b's in the message, 
    #       ...
    #       n26 is count of z's in the message, 
    #
    # If the calculated IC is closer to 0.038 then it was likely
    # encrypted using a polyalphabetic cipher.
    # If the calculated IC is closer to 0.065 then it was likely
    # encrypted using a monoalphabetic cipher.
    #
    def calcIC(self, msg):      
        # remove spaces from the message
        msg = ''.join(msg.split())     
        
        # get the squared length of the message as a float
        msgLenSqr = float(len(msg)**2)
        
        # get the letter counts
        letCounts = self.getLetCounts(msg)
        
        # sum each (count divided by the total len of the msg)
        sum = 0
        for count in letCounts.values():
            if count != 0:
                sum += (count**2)/msgLenSqr
                
        # return the calculated IC
        return sum

    ## isPolyalphabetic
    #
    # Determines if the cipher type is more likely to be polyalphabetic
    # or monoalphabetic by checking which IC the value is closer to
    #
    def isPolyalphabetic(self, ic):
        return (abs(ic - self.ranIC) < abs(ic - self.engIC))

    ## getKeywordLength
    #
    # IC test (Friedman Test)
    #
    # n is the length of the message
    # ic is the index of coincidence of the message
    #
    def getKeywordLength(self, n, ic):
        return float((0.027*n)/((n-1.0)*ic - 0.038*n + 0.065))
    
    ## msgSplit
    #
    # Using a known or predicted keyword length, splits the message
    # into columns that wrap every keywordLen number of columns
    #
    # For example, with 
    #   msg: AGDKLTSET
    #   keywordLen: 3
    #
    # The columns would look as follows:
    #
    #   A G D
    #   K L T
    #   S E T
    #
    # These columns can then be analyzed as if they were encrypted
    # using a monoalphabetic cipher
    #
    def msgSplit(self, msg, keywordLen):    
        # return the a list of columns
        # this works by separating the message into tuples of every
        # keywordLen letters and then transposing the result
        return map(list, zip(*(zip(*[iter(list(msg))]*keywordLen))))
    
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
    def vigenereSquareDecrypt(self, c, p):    
        for key, value in self.vigenereSquare[p].items():
            if value == c:
                return key
        return None
        
    ## vigenereSquareEncrypt
    #
    # k is the keyword letter (i.e. 'j')
    # p is the plaintext letter to encrypt (shift)
    #
    def vigenereSquareEncrypt(self, k, p):    
        return self.vigenereSquare[k][p]
    
if __name__ == "__main__":  
    polyCi = PolyalphabeticCipher()
    #polyCi.msgSplit("ABCDEFGHI", 3)
    #print polyCi.vigenereSquareDecrypt('N', 'e')
    #print polyCi.vigenereSquareEncrypt('j', 'e')
    #print polyCi.getKeywordLength(460, 0.04713)
    # parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    # parser.add_argument('-d', '--decrypt', dest='decrypt', action='store_true',
                       # default=False, help='Whether to decrypt the message. \
                       # (Default action is to encrypt the message.)')
    # parser.add_argument('-i', '--invert', dest='invert', action='store_true',
                       # default=False, help='Whether to invert the key. \
                       # (Default action is to not invert the key.)')
    # parser.add_argument('--msg', dest='msg', action='store',
                       # help='The message to encrypt or decrypt.', 
                       # required=True)
    # parser.add_argument('--split', dest='splitN', action='store', type=int,
                       # default=5, help='The size of the split for encrypted plaintext.')
    # parser.add_argument('--key', dest='key', action='store', nargs='+', type=int,
                       # help='The key used to encrypt or decrypt.', 
                       # required=True)

    # args = parser.parse_args()
    # letFreq = LetterFrequency()

    #msg = "MFE RLH WSR LHW BZN BNW SRX DEC INQ RNW JHL RBW BNL DER HQN DEQ BUJ WSH UZS RNN LDE RDA HJH LQC RWS HUM DTR EHU ICH NWN CDU JRE WSH ULD UDM DCP BWN AER RBW ZHU QRM CHP RIH UPX SRE RHE ZSB LRI RNI BIB WBU HQH WSW FQ"
    # msg = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"

    
    # msgIC = polyCi.calcIC(msg)
    # isPoly = polyCi.isPolyalphabetic(msgIC)
    
    # print "Analyzing message: %s" % msg
    # print "Message IC: %.4f" % msgIC
    # print "Message is likely %s" % ("polyalphabetic" if isPoly else "monoalphabetic")
    
    # if isPoly:
        # ""
    # else:
        # ""
    # msg = msg.replace(' ' , '')

    # col0 = []
    # col1 = []
    # col2 = []
    # col3 = []

    # for i in range(0, len(msg), 4):
        # col0.append(msg[i])
        # col1.append(msg[i+1])
        # col2.append(msg[i+2])
        # col3.append(msg[i+3])

    # msg0 = ''.join(col0)
    # msg1 = ''.join(col1)
    # msg2 = ''.join(col2)
    # msg3 = ''.join(col3)

    # print "\ncol1:", letFreq.getFrequencies(msg0)
    # print "\ncol2:", letFreq.getFrequencies(msg1)
    # print "\ncol3:", letFreq.getFrequencies(msg2)
    # print "\ncol4:", letFreq.getFrequencies(msg3)