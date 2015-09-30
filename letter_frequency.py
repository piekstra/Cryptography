import string

ciphertext = "KFM YGV VEM VHK AWK YZK FWG RFK MSJ JZG XOJ MEM DJZ MAM SCJ GKF EJK TSF GJI STM ZSW MKF MEJ KMS XGJ SFH PMJ JIK FME JKR MSZ"

msgLen = len(ciphertext)
frequencies = []
for ch in string.ascii_uppercase:
    frequencies.append((ch, (ciphertext.count(ch)/float(msgLen))*100))
frequencies = sorted(frequencies, key=lambda x: -x[1])    

for letter, frequency in frequencies:
    print "%c frequency: %0.2f%%" % (letter, frequency)