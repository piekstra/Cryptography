import string

commonDigraphs = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ND', 'AT', 'ON']

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
        
# manual run
diFreq = DigraphFrequency()
testMsg = "STB RDX TZQ MFY MJQ GTB WTT RXM FPJ XUJ FWJ MFI PNS LOT MSX FDF UUF WJS YQD MJB FXS YTS YMJ BFX MNS LYT SGJ QYB FDF YYM JYN RJ"
testMsg = testMsg.replace(' ', '')
print testMsg
print diFreq.getFrequencies(testMsg)