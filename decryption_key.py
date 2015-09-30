# most frequent letter in ciphertext
cipherLetter1 = 'M'
# second most frequent letter in ciphertext
cipherLetter2 = 'J'

# assume that the above are 'e' and 't' respectively
mostFreq = 'e'
secondMostFreq = 't'

multiplicativeInverses = {
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

alpha = ord(mostFreq)
beta = ord(cipherLetter1.lower())
delta = ord(secondMostFreq)
gamma = ord(cipherLetter2.lower())


