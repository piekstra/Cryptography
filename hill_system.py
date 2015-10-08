import string, argparse, math
from common.matrix_operations import MatrixOperations

class HillSystem:

    def __init__(self):            
        # initialize a string of chars that cannot be encrypted
        self.illegalChars = string.punctuation + ' ' 
        # initialize the character used to pad messages to fit the blocks
        self.padChar = 'x'
        # create a reference to the matrix operations
        self.matrixOps = MatrixOperations()
       
    def encrypt(self, msg, key, decrypt=False):
        keyDim = len(key)
        msg = msg.lower().translate(string.maketrans("", ""), self.illegalChars)
        # determine if we need to pad 'x's at the end of the msg to make it fill a block
        numToFill = (keyDim - (len(msg) % keyDim)) % keyDim
        msg += numToFill * self.padChar
        encryptedMsg = ""
        blocks = [msg[i:i+keyDim] for i in range(0,len(msg),keyDim)]
        for block in [msg[i:i+keyDim] for i in range(0,len(msg),keyDim)]:
            encryptedMatrix = self.matrixOps.matrixMult(key, [[ord(char)-96] for char in block])
            for encryptedRow in encryptedMatrix:
                cipherInt = encryptedRow[0] % 26
                # cover the 'z' case
                if cipherInt == 0:
                    cipherInt = 26
                encryptedMsg += chr(cipherInt+96)
        return encryptedMsg if decrypt else encryptedMsg.upper()
    
    def decrypt(self, msg, key, invertKey=False):
        # remove spaces from the message
        msg = ''.join(msg.split())
        # invert the key for decryption of the msg
        if invertKey:
            return self.encrypt(msg.lower(), self.matrixOps.invertMatrix(key), decrypt=True)
        return self.encrypt(msg.lower(), key, decrypt=True)
    
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
                       required=True)

    args = parser.parse_args()
    
    # Initialize the crypto system
    cryptoSystem = HillSystem()    
    
    #key = [[3,2], [8,5]]
    # the 'dimension' of the array is the square root of the length since it
    # is a square matrix
    arrDim = int(math.sqrt(len(args.key)))
    # Initialize the key (The argument is a 1D array it needs to be converted
    # into a square matrix)
    key = [args.key[i:i+arrDim] for i in range(0, len(args.key), arrDim)]
    
    # Initialize the message to encrypt or decrypt
    #msg = "MUBYA QIQGN AEWOS RZQJI RZQKC LIZAG SXCJA AQFRM HO"
    msg = args.msg
    
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
