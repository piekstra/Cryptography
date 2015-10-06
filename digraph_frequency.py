import string

class DigraphFrequency:
    
    def getFrequencies(self, msg):
        msgLen = len(msg)/2
        
        # create a dict of digraphs in the message and their counts
        digraphDict = {}
        for i in range(0, len(msg)-1):
            digraph = msg[i:i+2]
            # if the digraph has not been discovered yet, add it to the dict
            if digraph not in digraphDict:
                digraphDict[digraph] = 1
            # otherwise increment the count for that digraph
            else:
                digraphDict[digraph] += 1
        
        # determine the number of unique digraphs
        numDigraphs = float(len(digraphDict))
        
        # update the dict to contain frequencies instead of counts
        for digraph, count in digraphDict.iteritems():
            digraphDict[digraph] = round(count / numDigraphs, 2)
        
        # get a list of tuples containing the digraphs and their corresponding frequencies
        frequencies = digraphDict.items()
        
        # returns the list of tuples sorted from greatest frequency to least
        return sorted(frequencies, key=lambda x: -x[1])    
    
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