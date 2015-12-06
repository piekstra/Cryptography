import argparse

class CombinatorialSystem:

    ## __init__
    #
    # The constructor
    #
    def __init__(self): 
        ""
    
    def letToInt(self, let):
        let = let.lower()
        if 'a' <= let <= 'z':
            return ord(let) - 97
        elif let == ' ':
            return 26
        elif let == '?':
            return 27
        elif let == '!':
            return 28
        elif let == '.':
            return 29
        elif int == "'":
            return 30
        elif int == "\\":
            return 31
    
    def intToLet(self, int):
        if int <= 25:
            return chr(int+97)
        elif int == 26:
            return ' '
        elif int == 27:
            return '?'
        elif int == 28:
            return '!'
        elif int == 29:
            return '.'
        elif int == 30:
            return "'"
        elif int == 31:
            return "\\"
    
    def bcmodm(self, b, c, m):
        return (b*c) % m
    
    def knapsack(self, sequence, v):
        binary = ""
        # make sure the sequence is in descending order
        if sequence[-1] > sequence[0]:
            sequence = reversed(sequence)
        for num in sequence:
            if v >= num:
                v -= num
                binary += '1'
            else:
                binary += '0'
        return binary
    
    ## sums elements in sequence based on binary string
    def knapsackSum(self, sequence, bin):
        return sum([sequence[i] for i in range(len(sequence)) if int(bin[i])])
        
        
    ## decrypt
    def decrypt(self, msg, public_key, b, m, split=0, verbose=False):
        private_sequence = [self.bcmodm(b,c,m) for c in public_key]
        private_msg = [self.bcmodm(b,c,m) for c in msg]
        
        if verbose:
            print "Calculated key sequence:\n\t%s" % private_sequence
            print "Calculated msg segments:\n\t%s" % private_msg
            print   "\nBinary segments found using calculated key and msg\n"\
                    "segments as the 'V' in the knapsack problem:"
            print "\t%s\tDec\tLet" % "Bin".ljust(split)
            
        decrypted_msg = ""
        for v in private_msg:
            binSequence = self.knapsack(private_sequence, v)       
            # whether to split the binary sequence into chunks 
            # for individual binary to letter conversions
            if split != 0:       
                binSequences = [binSequence[i:i+split] for i in range(0, len(binSequence), split)]
                for bin in binSequences:                
                    dec = int(bin, 2)
                    if split == 5:
                        let = self.intToLet(dec)
                    elif split == 8:
                        let = chr(dec)
                    decrypted_msg += let
                    if verbose:
                        print "\t%s\t%d\t%c" % (bin, dec, let)
                    
        return decrypted_msg    
    
    def encrypt(self, msg, public_key, b, m, fill=0, verbose=False):
        dec = map(self.letToInt, msg)
        bins = [str(bin(x))[2:].zfill(fill) for x in dec]
        fullBin = ''.join(bins)
        seqLen = len(public_key)
        largeBins = [fullBin[i:i+seqLen] for i in range(0, len(fullBin), seqLen)]
        
        
        encryptedMsg = []
        for largeBin in largeBins:
            encryptedMsg.append(self.knapsackSum(public_key, largeBin))
        
        if verbose:
            print "Let\tDec\tBin"
            for i in range(len(msg)):
                print "%c\t%d\t%s" % (msg[i], dec[i], bins[i])
            print "\n%s\tKnapsack Sum" % 'Sequence Bin'.ljust(len(public_key))
            for i in range(len(largeBins)):
                print "%s\t%d" % (largeBins[i], encryptedMsg[i])
            
        return encryptedMsg
        
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Combinatorial System encryption and decryption.')
                       
    args = parser.parse_args()
    
    public_key = [181,182,362,649,939,438,813,542]
    # secret key
    b = 996
    m = 1459
    
    comb = CombinatorialSystem()
    
    decrypt = True    
    if decrypt:
        msg = [1631,3276,1086,2548,1631]
        split = 8
        print "Decrypting:\n\t%s" % msg
        print "Using public key:\n\t%s" % public_key
        print "\tb = %d\n\tm = %d\n" % (b, m)
        decryptedMsg = comb.decrypt(msg, public_key, b, m, split=split, verbose=True)
        print "\nDecrypted Message: %s" % decryptedMsg
    else:
        msg = "hello world!"
        fill = 5
        print "Encrypting:\n\t%s" % msg
        print "Using public key:\n\t%s" % public_key
        print "\tb = %d\n\tm = %d\n" % (b, m)
        encryptedMsg = comb.encrypt(msg, public_key, b, m, fill=fill, verbose=True)
        print "\nEncrypted Message: %s" % encryptedMsg

