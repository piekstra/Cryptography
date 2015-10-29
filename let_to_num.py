import argparse, random

letToNumDict = {
    'a' : [15, 33, 37, 55, 57, 72, 91, 96],
    'b' : [24],
    'c' : [3, 39, 67],
    'd' : [4, 43, 61, 88],
    'e' : [8, 12, 20, 46, 47, 59, 64, 79, 81, 85, 90, 94, 97],
    'f' : [40, 48],
    'g' : [29, 53],
    'h' : [5, 16, 30, 42, 69, 99],
    'i' : [14, 45, 50, 60, 73, 82, 93],
    'j' : [11],
    'k' : [77],
    'l' : [1, 26, 71, 98],
    'm' : [34, 87],
    'n' : [6, 17, 22, 31, 49, 58],
    'o' : [2, 10, 41, 51, 66, 75, 83],
    'p' : [13, 18],
    'q' : [36],
    'r' : [21, 25, 65, 68, 92, 95],
    's' : [0, 28, 52, 63, 74, 78],
    't' : [7, 19, 23, 35, 38, 54, 70, 84, 89],
    'u' : [9, 32],
    'v' : [44],
    'w' : [56, 80],
    'x' : [86],
    'y' : [62, 76],
    'z' : [27]
}

def encipher(msg):
    encryptedMsg = ""
    for let in msg:
        possibleValues = letToNumDict[let]
        ranVal = possibleValues[random.randint(0, len(possibleValues)-1)]
        encryptedMsg += str(ranVal).zfill(2)
    return encryptedMsg    

def decipher(msg):
    decryptedMsg = ""
    for i in range(0, len(msg), 2):
        diNum = int(msg[i:i+2])
        for let, nums in letToNumDict.items():
            if diNum in nums:
                decryptedMsg += let
                break
    return decryptedMsg 
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Replace letters with numbers!')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to encrypt or decrypt.', 
                       required=True)
    parser.add_argument('-e', dest='encipher', action='store_true',
                       help='Whether to encipher. (Default is to decipher)', 
                       required=False)

    args = parser.parse_args()
    
    if args.encipher:
        print encipher(args.msg.lower().replace(' ', ''))
    else:
        print decipher(args.msg.lower().replace(' ', ''))
    
   