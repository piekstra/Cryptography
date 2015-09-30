import string

class DigraphFrequency:
    
    def getFrequencies(self, msg):
        msgLen = len(msg)/2
        
        frequencies = []
        for digraph in commonDigraphs:
            frequencies.append((digraph, (msg.count(digraph)/float(msgLen))*100))
        frequencies = sorted(frequencies, key=lambda x: -x[1])    

        # for digraph, frequency in frequencies:
            # return print "%s frequency: %0.2f%%" % (digraph, frequency)
            
        return frequencies
    
    ## getDigraphFrequencies
    #
    # returns the most common digraphs found in English sentences
    # as well as their corresponding frequencies
    #
    def getDigraphFrequencies(self):
        return [('TH', 1.52), ('HE', 1.28), ('IN', 0.94), ('ER', 0.94), ('AN', 0.82), ('RE', 0.68), ('ND', 0.63), ('AT', 0.59), ('ON', 0.57)]
        
# manual run
diFreq = DigraphFrequency()
testMsg = "STB RDX TZQ MFY MJQ GTB WTT RXM FPJ XUJ FWJ MFI PNS LOT MSX FDF UUF WJS YQD MJB FXS YTS YMJ BFX MNS LYT SGJ QYB FDF YYM JYN RJ"
testMsg = testMsg.replace(' ', '')
print testMsg
print diFreq.getFrequencies(testMsg)