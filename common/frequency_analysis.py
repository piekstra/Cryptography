import string, argparse
import operator

class LetterFrequency:
    def __init__(self):
        # initialize the standard english frequency dict
         self.stdDict = {'e': 12.702, 't': 9.056, 'a': 8.167, 'o': 7.507, 'i': 6.966, 'n': 6.749, 's': 6.327, 'h': 6.094, 'r': 5.987, 'd': 4.253, 'l': 4.025, 'c': 2.782, 'u': 2.758, 'm': 2.406, 'w': 2.360, 'f': 2.228, 'g': 2.015, 'y': 1.974, 'p': 1.929, 'b': 1.492, 'v': 0.978, 'k': 0.772, 'j': 0.153, 'x': 0.150, 'q': 0.095, 'z': 0.074}
         self.stdTuples = sorted(self.stdDict.items(), key=operator.itemgetter(1), reverse=True)
            
    
    ## Determines frequencies of letters in the msg
    def getFrequencies(self, msg):
        msg = msg.replace(' ' , '')
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
    
    def getFollowingDigraphs(self, msg, digraph):
        # create a list of digraphs that follow the specified digraph
        followingDigraphs = []
        for i in range(0, len(msg), 2):
            tempDi = msg[i:i+2]            
            if tempDi == digraph:
                followingDigraphs.append(msg[i+2:i+4])

        # return a list of digraphs that follow the specified digraph
        return followingDigraphs
    
    def getDigraphs(self, msg):
        # return a list of digraphs
        return [msg[i:i+2] for i in range(0, len(msg), 2)]
    
    def letToInt(self, let, zeroSystem=False):
        return (ord(let.lower()) - 96) - (1 if zeroSystem else 0)
    
    def digraphToIntTuple(self, digraph, zeroSystem=False):
        return (self.letToInt(digraph[0], zeroSystem), self.letToInt(digraph[1], zeroSystem))
    
    def getDigraphInts(self, msg):
        # create a list of digraphs that follow the specified digraph
        digraphIntTuples = []
        for i in range(0, len(msg), 2):
            tempDi = msg[i:i+2]
            converted = tuple(map(self.letToInt, tempDi))
            if converted not in digraphIntTuples:
                digraphIntTuples.append(converted)

        # return a list of digraphs that follow the specified digraph
        return digraphIntTuples
    
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
    parser = argparse.ArgumentParser(description='Perform frequency analysis on a message.')
    parser.add_argument('--msg', dest='msg', action='store',
                       help='The message to analyze.', 
                       required=True)
    parser.add_argument('--slf', dest='slf', action='store_true', 
                       help="Whether to show the letter frequencies of the ciphertext and the English Language.", 
                       required=False, default=False)
    parser.add_argument('--sdf', dest='sdf', action='store_true', 
                       help="Whether to show the digraph frequencies of the ciphertext and the English Language.", 
                       required=False, default=False)
    parser.add_argument('--sfd', dest='sfd', action='store', type=str,
                       help="Whether to show the digraphs following a digraph.", 
                       required=False, default=None)
    parser.add_argument('--sdi', dest='sdi', action='store_true', 
                       help="Whether to show the digraphs in the ciphertext as their integer (mod 26) equivalents.", 
                       required=False, default=False)
                       
    args = parser.parse_args()
    
    letFreq = LetterFrequency()
    diFreq = DigraphFrequency()
    args.msg = args.msg.replace(' ', '')
    print "\nPerforming frequency analysis for message:\n%s\n" % args.msg
    
    if args.slf:
        print "Letter frequencies in the message:\n%s\n" % letFreq.getFrequencies(args.msg)[1]
        print "Letter frequencies in the English Language:\n%s\n" % letFreq.getStandardFrequencies()[1]    
    if args.sdf:
        print "Digraph frequencies in the message:\n%s\n" % diFreq.getFrequencies(args.msg)[1]  
        print "Digraph frequencies in the English Language:\n%s\n" % diFreq.getStandardFrequencies()[1] 
    if args.sfd:
        print "Digraphs following digraph: %s\n%s\n" % (args.sfd, diFreq.getFollowingDigraphs(args.msg, args.sfd))
    if args.sdi:
        print "Digraphs in ciphertext as their integer (mod 26) equivalents:\n%s\n" % diFreq.getDigraphInts(args.msg)