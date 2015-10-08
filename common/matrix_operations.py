import string, argparse, math

class MatrixOperations:

    def __init__(self):
        return
        
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