import argparse

class CombinatorialSystem:

    ## __init__
    #
    # The constructor
    #
    def __init__(self, alphabet): 
        self.alphabet = alphabet
    
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
        binary = []
        if sequence[-1] > sequence[0]:
            sequence = reversed(sequence)
        for num in sequence:
            if v > num:
                v -= num
                binary.append(1)
            else:
                binary.append(0)
        return binary
    
    def binToInt(self, binary):
        return sum([2**idx for idx, b in enumerate(reversed(binary)) if b])
        
    ## decrypt
    def decrypt(self, msg, public_key, b, m, split=0):
        private_sequence = [self.bcmodm(b,c,m) for c in public_key]
        private_msg = [self.bcmodm(b,c,m) for c in msg]
        print private_sequence
        print private_msg
        for v in private_msg:
            binSequence = self.knapsack(private_sequence, v)       
            print binSequence            
            if split != 0:
                binSequences = [binSequence[i:i+split] for i in range(0, len(binSequence), split)]
                for bin in binSequences:
                    print self.intToLet(self.binToInt(bin))
            
        
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Combinatorial System encryption and decryption.')
    # parser.add_argument('--msg', dest='msg', action='store',
                       # help='The message to decrypt.', 
                       # required=True)
    # parser.add_argument('--mfc', dest='mfc', action='store', nargs=2, type=str,
                       # help='The two most frequent ciphertext letters.', required=False, default=None)
    # parser.add_argument('--mfp', dest='mfp', action='store', nargs=2, type=str,
                       # help='The two (most frequent) plaintext letters that the ciphertext letters are expected to be decrypted to based on frequency analysis.', 
                       # required=False, default=['e', 't'])
    # parser.add_argument('--sdf', dest='sdf', action='store_true', 
                       # help="Whether to show the digraph frequencies of the ciphertext and the English Language.", 
                       # required=False, default=False)
                       
    args = parser.parse_args()
    
    alphabetSize = 32    
    split = 5
    public_key = [24038,29756,34172,34286,38334,1824,18255,19723,143,17146,35366,11204,32395,12958,6479]
    msg = [152472,116116,68546,165420,168261]
    # secret key
    b = 30966
    m = 47107
    
    comb = CombinatorialSystem(alphabetSize)
    comb.decrypt(msg, public_key, b, m, split=split)


