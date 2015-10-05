
class HillSystem:

    def __init__(self, key):
        if len(key) < 1:
            print("ERROR: invalid key")            
            return
            
        # initialize the n x n matrix
        self.key = key
        # initialize the key's dimension (n)
        self.keyDim = len(key[0])
        
    def matrixMult(self, matrix1, matrix2):
        return
    
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
    
    def invertMatrix(self, matrix):
        return
    
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
    
    def encrypt(self, msg, decrypt=False):
        encryptedMsg = ""
        for block in [msg[i:i+self.keyDim] for i in range(0,len(msg), self.keyDim)]:
            print block
            for row in self.key:
                print row
                ciphertext = 0
                for idx, char in enumerate(block):
                    plaintextInt = ord(char)-96
                    cipherInt = row[idx]*plaintextInt
                    ciphertext += cipherInt
                encryptedMsg += (chr(ciphertext%26+96))                   
        return encryptedMsg if decrypt else encryptedMsg.upper()
    
    def decrypt(self, msg):
        # remove spaces from the message
        msg = ''.join(msg.split())
        return self.encrypt(msg.lower(), decrypt=True)
    
if __name__ == "__main__":
    #key = [[6, 3], [7,8]]
    #key = [[3, 2], [8,5]]
    key = ([[1,2,3],
            [0,1,4],
            [5,6,0]])
    cryptoSystem = HillSystem(key)
    #print cryptoSystem.encrypt("testing")
    #print cryptoSystem.decrypt("MUBYA QIQGN AEWOS")
    print cryptoSystem.det(key)
    print cryptoSystem.getAdjugateMatrix(key)

