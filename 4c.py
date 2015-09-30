
## Problem 4c

plaintext = "The essence of the free press is the reliable, reasonable, and moral nature of freedom. The character of the censored press is the nondescript confusion of tyranny."
plaintext = plaintext.lower()
ciphertext = ""
plainInts = []
cipherInts = []
multKey = 23
addKey = 2
for ch in plaintext:
    if ch == ' ':
        ciphertext += ch
    elif ch == "," or ch == ".":
        continue
    else:         
        plainInt = ord(ch) - 96
        cipherInt = ((plainInt + addKey) * multKey)%26
        # cover the 'z' case
        if cipherInt == 0:
            cipherInt = 26
        plainInts.append(plainInt)
        cipherInts.append(cipherInt)
    	ciphertext += chr(cipherInt+96)

print "Integer representations for lowercase chars in plaintext:\n", plainInts        
print "Integer representations for lowercase chars in ciphertext:\n", cipherInts
print "ciphertext:\n", ciphertext.upper()