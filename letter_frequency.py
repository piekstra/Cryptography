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
    
    ## getLetterFrequencies
    #
    # returns the most common letters found in English sentences
    # as well as their corresponding frequencies
    #
    def getLetterFrequencies(self):
        return [('e', 12.702),('t', 9.056), ('a', 8.167), ('o', 7.507), ('i', 6.966), ('n', 6.749), ('s', 6.327), ('h', 6.094), ('r', 5.987)]