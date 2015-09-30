import itertools, string

## Problem 4d

keyword = ''.join(ch for ch, _ in itertools.groupby("communist"))
print "keyword:", keyword

keyletter = 'z'
print "keyletter:", keyletter

alphabet = string.ascii_lowercase
lookupTable = list(alphabet)
remainingLetters = alphabet.translate(None, keyword)

print "\noriginal table:\n", lookupTable
startIdx = ord(keyletter) - 97
for i in range (0, len(keyword)):
    tableIdx = (startIdx + i) % 26
    lookupTable[tableIdx] = keyword[i]
    
print "table with keyword inserted:\n", lookupTable
startIdx = (ord(keyletter) - 97 + len(keyword)) % 26
for i in range (0, len(remainingLetters)):
    tableIdx = (startIdx + i) % 26
    lookupTable[tableIdx] = remainingLetters[i]
    
print "table with remaining letters inserted:\n", lookupTable

# Now that we have the lookup table, we can go through the sequence and
# use the table to find the ciphertext
plaintext = "The essence of the free press is the reliable, reasonable, and moral nature of freedom. The character of the censored press is the nondescript confusion of tyranny."
plaintext = plaintext.lower()
ciphertext = ""
plainInts = []
cipherInts = []
for ch in plaintext:
    if ch == ' ':
        ciphertext += ch
    elif ch == "," or ch == ".":
        continue
    else:         
        plainInt = ord(ch) - 97
        cipherChar = lookupTable[plainInt]
    	ciphertext += cipherChar
        
print "Ciphertext:\n", ciphertext.upper()