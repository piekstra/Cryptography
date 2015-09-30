import string
class LetterFrequency:
    
    def getFrequencies(self, msg):
        msgLen = len(msg)
        
        frequencies = []
        for ch in string.ascii_uppercase:
            frequencies.append((ch, (msg.count(ch)/float(msgLen))*100))
        frequencies = sorted(frequencies, key=lambda x: -x[1])    

        # for letter, frequency in frequencies:
            # return print "%c frequency: %0.2f%%" % (letter, frequency)
            
        return frequencies