import binascii, math
from hill_system import HillSystem

# message to encrypt
msg = "Hi!"
# key used to encrypt the message
key = [ [1, 0, 1, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0]]

# dimension 'n' of the (n x n) key matrix
keyDim = len(key)

print "Encrypting:\n%s\n" % msg
print "Using key:\n%s\n" % key
 
# get the binary representation of the message
binMsg = ''.join(format(ord(ch), 'b').zfill(8) for ch in msg)
# set up a reference to the crypto system
cryptoSystem = HillSystem()

# holds the encrypted message
encryptedMsg = ""

# holds a chunk of the encrypted message
binChunk = ""

# loop through the binary
for i in range(0, len(binMsg), keyDim):
    # extract a block from the message
    binBlock = map(int, binMsg[i:i+keyDim])
    # encrypt the block using the key
    encryptedBlockMatrix = cryptoSystem.matrixMult(key, map(list, zip(binBlock)))
    # because the encrypted block is an n x 1 matrix, the rows
    # need to be joined into a 1D list and then to a string
    encryptedBlockString = ''.join([str(row[0]%2) for row in encryptedBlockMatrix])
    # append the encoded binary to the chunk
    binChunk += encryptedBlockString
    
    # if the chunk is large enough to represent a charcter, convert it
    # to ascii and append it to the encrypted message
    if len(binChunk) % 8 == 0:
        encryptedMsg += chr(int(binChunk, 2)%128)
        # reset the chunk
        binChunk = ""
        
# print the encrypted message
print "Encrypted message in ASCII:\n%s\n" % encryptedMsg
# print the binary of the encrypted message
print "Encrypted message in binary:\n%s\n" % ' '.join(format(ord(ch), 'b').zfill(8) for ch in encryptedMsg)


