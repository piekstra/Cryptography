
## Problem 

import sys
if len(sys.argv) > 1:
    plaintext = sys.argv[1].lower()
    multKey = int(sys.argv[2])
    addKey = int(sys.argv[3])
else:    
    plaintext = "LQNNBN"
    plaintext = plaintext.lower()
    multKey = 1
    addKey = 9
ciphertext = ""
plainInts = []
cipherInts = []

for ch in plaintext:
    if ch == ' ':
        ciphertext += ch
    elif ch == "," or ch == ".":
        continue
    else:         
        plainInt = ord(ch) - 96
        cipherInt = ((plainInt * multKey) - addKey)%26
        # cover the 'z' case
        if cipherInt == 0:
            cipherInt = 26
        plainInts.append(plainInt)
        cipherInts.append(cipherInt)
    	ciphertext += chr(cipherInt+96)

print "Integer representations for lowercase chars in plaintext:\n", plainInts        
print "Integer representations for lowercase chars in ciphertext:\n", cipherInts
print "ciphertext:\n", ciphertext
