import string, argparse, math

class HillSystem:

    def __init__(self):            
        # initialize a string of chars that cannot be encrypted
        self.illegalChars = string.punctuation + ' ' 
        # initialize the character used to pad messages to fit the blocks
        self.padChar = 'x'
        
    def matrixMult(self, matrix1, matrix2):
        multMatrix = []
        for row in matrix1:
            multRow = []
            for col in self.transpose(matrix2):
                # multiply each element in matrix1's row with the corresponding element in
                # matrix2's col and sum the results
                multRow.append(sum([rowEl*colEl for rowEl,colEl in zip(row,col)]))
            multMatrix.append(multRow)
        return multMatrix
    
    ## det
    # recursively determines the determinant of an n x n matrix
    def det(self, matrix):    
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        determinant = 0
        neg=1
        for colIdx in range(0, len(matrix[0])):        
            subMatrix = [row[:colIdx]+row[colIdx+1:] for row in matrix[1:]]
            subDet = self.det(subMatrix)
            col = matrix[0][colIdx]
            determinant += neg*col*subDet
            neg*=-1
        return determinant
    
    ## returns the transpose of the matrix
    def transpose(self, matrix):
        return [list(row) for row in zip(*matrix)]
    
    ## finds the inverse of a matrix
    def invertMatrix(self, matrix):
        if len(matrix) == 2:      
            return [[-matrix[1][1], matrix[0][1]],
                    [matrix[1][0], -matrix[0][0]]]
        matrixDet = self.det(matrix)
        adjugateMatrix = self.getAdjugateMatrix(matrix)
        inverseMatrix = [[colEl/matrixDet for colEl in row] for row in adjugateMatrix]
        return inverseMatrix
            
    def getAdjugateMatrix(self, matrix, transpose=True):
        # make sure the matrix is transposed
        if transpose:
            matrix = self.transpose(matrix)
        adjugateMatrix = []
        for rowIdx in range(0, len(matrix)):
            detRow = []
            for colIdx in range(0, len(matrix[rowIdx])):
                subRows = matrix[:rowIdx]+matrix[rowIdx+1:]
                subM = [row[:colIdx]+row[colIdx+1:] for row in subRows]
                detRow.append(self.det(subM))
            adjugateMatrix.append(detRow)
        return adjugateMatrix        
    
    def encrypt(self, msg, key, decrypt=False):
        keyDim = len(key)
        msg = msg.lower().translate(string.maketrans("", ""), self.illegalChars)
        # determine if we need to pad 'x's at the end of the msg to make it fill a block
        numToFill = (keyDim - (len(msg) % keyDim)) % keyDim
        msg += numToFill * self.padChar
        encryptedMsg = ""
        blocks = [msg[i:i+keyDim] for i in range(0,len(msg),keyDim)]
        for block in [msg[i:i+keyDim] for i in range(0,len(msg),keyDim)]:
            encryptedMatrix = self.matrixMult(key, [[ord(char)-96] for char in block])
            for encryptedRow in encryptedMatrix:
                cipherInt = encryptedRow[0] % 26
                # cover the 'z' case
                if cipherInt == 0:
                    cipherInt = 26
                encryptedMsg += chr(cipherInt+96)
        return encryptedMsg if decrypt else encryptedMsg.upper()
    
    def decrypt(self, msg, key):
        # remove spaces from the message
        msg = ''.join(msg.split())
        # invert the key for decryption of the msg
        return self.encrypt(msg.lower(), self.invertMatrix(key), decrypt=True)
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    parser.add_argument('-d', '--decrypt', dest='decrypt', action='store_true',
                       default=False, help='Whether to decrypt the message. \
                       (Default action is to encrypt the message.)')
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
        plaintext = cryptoSystem.decrypt(msg, key)
        print "Plaintext:\n%s\n" % plaintext
