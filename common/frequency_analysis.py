import string
import operator

class LetterFrequency:
    def __init__(self):
        # initialize the standard english frequency dict
         self.stdDict = {'e': 12.702, 't': 9.056, 'a': 8.167, 'o': 7.507, 'i': 6.966, 'n': 6.749, 's': 6.327, 'h': 6.094, 'r': 5.987}
         self.stdTuples = sorted(self.stdDict.items(), key=operator.itemgetter(1), reverse=True)
            
    
    ## Determines frequencies of letters in the msg
    def getFrequencies(self, msg):
        msgLen = len(msg)
        
        frequencies = {}
        for ch in string.ascii_uppercase:
            frequencies[ch] = (msg.count(ch)/float(msgLen))*100
        
        # return a tuple of the frequencies dict and a list of tuples
        # of (let, letFreq) sorted from greatest frequency to least
        return (frequencies, sorted(frequencies.items(), key=operator.itemgetter(1), reverse=True))
    
    
    ## getStandardFrequencies
    #
    # returns a tuple of a dictionary and a list of tuples
    # 
    # The dictionary and list of tuples contain most common letters found in 
    # English sentences with their corresponding frequencies
    # 
    # The list of tuples is sorted from greatest to least    
    #
    def getStandardFrequencies(self):
        return (self.stdDict, self.stdTuples)

class DigraphFrequency:

    def __init__(self):
        # initialize the standard english frequency dict
        self.stdDict = {
            'TH': 1.52, 
            'HE': 1.28, 
            'IN': 0.94, 
            'ER': 0.94,
            'AN': 0.82, 
            'RE': 0.68, 
            'ND': 0.63, 
            'AT': 0.59,
            'ON': 0.57 
        }
        self.stdTuples = sorted(self.stdDict.items(), key=operator.itemgetter(1), reverse=True)
    
    def getFrequencies(self, msg):
        msgLen = len(msg)/2

        # create a dict of digraphs in the message and their counts
        digraphDict = {}
        for i in range(0, len(msg), 2):
            digraph = msg[i:i+2]
            # if the digraph has not been discovered yet, add it to the dict
            if digraph not in digraphDict:
                digraphDict[digraph] = 1                
            # otherwise increment the count for that digraph
            else:
                digraphDict[digraph] += 1
                    
        # determine the number of unique digraphs
        numDigraphs = len(msg)/2.0

        # update the dict to contain frequencies instead of counts
        for digraph, count in digraphDict.iteritems():
            digraphDict[digraph] = round((count / numDigraphs) * 100, 2)

        # return a tuple of the frequencies dict and a list of tuples
        # of (digraph, digraphFreq) sorted from greatest frequency to least
        return (digraphDict, sorted(digraphDict.items(), key=operator.itemgetter(1), reverse=True))
        
    
    ## getStandardFrequencies
    #
    # returns a tuple of a dictionary and a list of tuples
    # 
    # The dictionary and list of tuples contain most common digraphs found in 
    # English sentences with their corresponding frequencies
    # 
    # The list of tuples is sorted from greatest to least
    #
    def getStandardFrequencies(self):
        return (self.stdDict, self.stdTuples)
        
 
if __name__ == "__main__":    
    # manual run
    diFreq = DigraphFrequency()
    testMsg = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"
    testMsg = testMsg.replace(' ', '')
    print testMsg
    print "Ciphertext digraph frequencies:\n%s\n" % diFreq.getFrequencies(testMsg)
    print "Common digraph frequencies:\n%s\n" % diFreq.getDigraphFrequencies()