from letter_frequency import LetterFrequency
import sys

# Problem 1's Message
#ciphertext = "KFM YGV VEM VHK AWK YZK FWG RKF MSJ JZG XOJ MEM DJZ MAM SCJ GKF EJK TSF GJI STM ZSW MKF MEJ KBS XGJ SFH PMJ JIK FME JKR MSZ"
# Problem 2's Message
#ciphertext = "XTS OCZ SIV JPI FCS XQE BEA SIV YIP SOF ICO SJR QYC VJJ SNS VJE VXT FSS BIA XEF OXT SPS DEA CXQ EBX TSY CVJ XTS JCO XIV ASC XRD EYO IAF EOO XTS YIX SFX TSD SVK XTE BXC MSC XRD EYO"
# Problem 4's Message
#ciphertext = "STB RDX TZQ MFY MJQ GTB WTT RXM FPJ XUJ FWJ MFI PNS LOT MSX FDF UUF WJS YQD MJB FXS YTS YMJ BFX MNS LYT SGJ QYB FDF YYM JYN RJ"
# Problem 5's Message
ciphertext = "CWF FSK AAC KHW JAO ZHA NGA THO ZUW ENC AKK MUA KJA HR"

print "Attempting to decipher:\n", ciphertext, "\n"

# get the letter frequencies
letFreq = LetterFrequency()
frequencies = letFreq.getFrequencies(ciphertext)
print "Letter Frequencies:\n", frequencies, "\n"

# most frequent letter in ciphertext
cipherLetter1 = frequencies[0][0]
# second most frequent letter in ciphertext
cipherLetter2 = frequencies[1][0]

print "Most frequent letter in ciphertext:", frequencies[0][0]
print "\twith frequency: %.2f%%" % frequencies[0][1]
print "Second most frequent letter in ciphertext:", cipherLetter2
print "\twith frequency: %.2f%%\n" % frequencies[1][1]

# assume that the two most frequent letters are 'e' and 't' respectively
# unless manual guesses are specified via command line
if len(sys.argv) <= 1:
    mostFreq = 'e'
    secondMostFreq = 't'
else:
    mostFreq = sys.argv[1]
    secondMostFreq = sys.argv[2]

print "Assuming that", cipherLetter1, "is equivalent to", mostFreq
print "Assuming that", cipherLetter2, "is equivalent to", secondMostFreq, "\n"

# quick lookup table of multiplicative inverses for integers mod 26
multiplicativeInverse = {
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

# initialize the variables to the mod 26 equivalents of the letters
# plaintext characters
p1 = ord(mostFreq) - 96
p2 = ord(secondMostFreq) - 96
# ciphertext characters
c1 = ord(cipherLetter1.lower()) - 96
c2 = ord(cipherLetter2.lower()) - 96

lhs = (p2 - p1)
rhs = (c2 - c1) % 26

s = -1
for multKey in multiplicativeInverse.keys():
    if lhs * multKey % 26 == rhs:
        s = multKey
        break
if s == -1:
    print "ERROR: could not find multiplicative key"
    sys.exit(-1)
    
rhs = c1 - s*p1%26
if rhs < 0:
    rhs += 26

r = -1
for addKey in range (0, 26):
    if addKey * s % 26 == rhs:
        r = addKey
        break
if r == -1:
    print "ERROR: could not find additive key"
    sys.exit(-1)

# key is s, r
key = (s, r)
print "Key:", key, "\n"

plaintext = ""
for ch in ciphertext.lower():
    if ch == ' ':
        continue
    else:
        cipherInt = ((ord(ch) - 96)*multiplicativeInverse[key[0]] - key[1]) % 26
        # cover the 'z' case
        if cipherInt == 0:
            cipherInt = 26
        plaintext += chr(cipherInt + 96)

print "Plaintext:\n", plaintext



