import operator, fractions, re, itertools

class KasiskiTest:

    def findAllRepeatedSubstrs(self, msg, substrLen):        
        # create a dict mapping each unique substring of length substrLen
        # to the number of times it occurrs in msg
        substrs = {}        
        for i in range(0, len(msg)-substrLen-1):
            substr = msg[i:i+substrLen]
            if substr in substrs:
                substrs[substr] += 1
            else:
                substrs[substr] = 1

        # convert the dict to a list of tuples, sorted from greatest to least
        substrTuples = sorted(substrs.items(), key=operator.itemgetter(1), reverse=True)
        
        # Return a list of all substrings that are repeated
        return [substrTuple[0] for substrTuple in filter(lambda substrTuple: substrTuple[1] > 1, substrTuples)]

    def mostCommonSubstr(self, msg, substrLen):
        # Return the most frequently occurring substr
        return self.findAllRepeatedSubstrs(msg, substrLen)[0]
    
    def getRepeatedSubstrs(self, msg, minLen):    
        # This is horribly NOT optimal, but it gets the job done 
        # (can have fun with it later - suffix tree!)'
        
        repeatedSubstrs = []
        
        # Go through the list backwards from the longest possible substr and
        # add them to repeatedSubstrs if it is not already there in a longer
        # form (i.e. do not add THYQ if THYQZ is already there)
        for i in range(len(msg)-1, minLen-1, -1):
            substrs = self.findAllRepeatedSubstrs(msg, i)
            for substr in substrs:
                #if any(substr in item for item in repeatedSubstrs):
                # if any(item.startswith(substr) for item in repeatedSubstrs):
                    # continue
                repeatedSubstrs.append(substr)   
        return repeatedSubstrs
    
    def getDistancesBetweenOccurrences(self, msg, substr):
        # get the indexes of each occurrence of substr in msg
        indexes = [m.start() for m in re.finditer(substr, msg)]
        gaps = []
        for i, index in enumerate(indexes):
            for nextIndex in indexes[i+1:]:
                gaps.append(nextIndex-index)
        # determine the distances between each occurrence of substr in msg
        return gaps
        
    def getPotentialKeyLens(self, msg, substr): 
        distances = self.getDistancesBetweenOccurrences(msg, substr)
        return sorted(self.getDivisors(tuple(distances)), reverse=True)[:-1]
    
    def getAllPotentialKeyLens(self, msg, substrs):
        return [self.getPotentialKeyLens(msg, substr) for substr in substrs]
    
    def getMostLikelyKeyLens(self, msg, substrs):
        # get potential key lengths for all substrings
        allKeyLens = self.getAllPotentialKeyLens(msg, substrs)
        
        # holds every potential key and the number of times it shows up
        # in the list of potential key lists (more frequently it shows up, 
        # the more likely it is to be the actual length of the key)
        keys = {}
        for keyLens in allKeyLens:
            for key in keyLens:
                if key in keys:
                    keys[key] += 1
                else:
                    keys[key] = 1
        # return the most likely key lengths in order of most likely to least likely      
        return [keyTuple[0] for keyTuple in sorted(keys.items(), key=operator.itemgetter(1), reverse=True)]
    
    def getDivisors(self, ints):
        # return the common divisors of every int in the tuple of ints
        return [i for i in range(1, reduce(lambda a,b: fractions.gcd(a,b), ints)+1) if reduce(lambda a,b: a and b, [x % i == 0 for x in ints])]
    
if __name__ == "__main__":  
    # debugging code
    kt = KasiskiTest()
    #msg = "YBR GPT OOY CBC GUG SNR TCW MVF RMU GJC MUI RCC UZV LJX BAJ DNU RTJ LLF KFF YBL JMZ NWG YNY JYB RRV HCG VLL MGH DKB NCN JHF NRW YNY JDV VTL ZGO RPX IAR QBY PNL YYI RLG YTV LYI GUG SEN OMZ NVA YSS IRP DXR SGS CGR UFS BHP GLN VLX BNI CJP BYT JXG BEJ NHF MZN BSR MYE NGS ZVA BBB REC YBR OCW LVR QFL RNL IER RNZ MSE MRA RGR NHT XGQ FRQ MZL OEY NHF QGI HBG CAI YIC YIU RJU OFT PFM CEC FFY LJF LTR LZG ORP XIE GMQ IBX YYN UVL LMV AYM OAQ PJX GUM ZMN ABI CZR LXC BAQ"
    msg = "ABCXYZABCKLMNOPQRSABC"
    msg = msg.replace(' ' , '')
    print kt.getMostLikelyKeyLens(msg, 'ABC')
        