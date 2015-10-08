import string, argparse, sys

class AffineSystem:

    def __init__(self):            
        # initialize a string of chars that cannot be encrypted
        self.illegalChars = string.punctuation + ' ' 
       
    def encrypt(self, msg, key, decrypt=False):
        # initialize the multiplicative and additive keys
        multKey = key[0]
        addKey = key[1]
        
        # make all capital letters lowercase then clear
        # the message of all punctuation and whitespace
        msg = msg.lower().translate(string.maketrans("", ""), self.illegalChars)
        
        # holds the encrypted message (or decrypted message)
        encryptedMsg = ""
        for ch in msg:    
            charInt = ord(ch) - 96
            # decryption is done slightly differently than encryption
            if decrypt:
                cipherInt = ((charInt * multKey) - addKey)%26
            else:
                cipherInt = ((charInt + addKey) * multKey)%26
            # cover the 'z' case
            if cipherInt == 0:
                cipherInt = 26
            encryptedMsg += chr(cipherInt+96)
        return encryptedMsg if decrypt else encryptedMsg.upper()
     
    def decrypt(self, msg, key, invertKey=False):
        return self.encrypt(msg, key, decrypt=True)
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    parser.add_argument('-d', '--decrypt', dest='decrypt', action='store_true',
                       default=False, help='Whether to decrypt the message. \
                       (Default action is to encrypt the message.)')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to encrypt or decrypt.', 
                       required=True)
    parser.add_argument('--split', dest='splitN', action='store', type=int,
                       default=5, help='The size of the split for encrypted plaintext.')
    parser.add_argument('--key', dest='key', action='store', nargs='+', type=int,
                       help='The key used to encrypt or decrypt.', 
                       required=True)

    args = parser.parse_args()
    
    # Initialize the crypto system
    cryptoSystem = AffineSystem()    
    
    # Initialize the message to encrypt or decrypt
    msg = args.msg
    
    # Initialize the key used to encrypt or decrypt the message
    key = args.key
        
    if not args.decrypt:
        print "Encrypting message:\n%s\n" % msg
        print "Using key:\n%s\n" % key
        ciphertext = cryptoSystem.encrypt(msg, key)
        print "Ciphertext:\n%s\n" % ciphertext
    else:
        print "Decrypting message:\n%s\n" % msg
        print "Using key:\n%s\n" % key
        plaintext = cryptoSystem.decrypt(msg, key)
        print "Plaintext:\n%s\n" % plaintext
