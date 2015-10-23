from common.letter_counts import LetterCounts

class VignereCipher:

    def __init__(self):
        self.letCounter = LetterCounts()
        self.ic = { "english" : 0.065, "equiprobable" : 0.038}

    ## clearMsg
    #
    # cleans up the ciphertext so that it only contains
    # A-Z characterws
    #
    def clearMsg(self, msg):
        return msg.replace(' ', '')
    
    ## Index of Coincidence (IC)
    # The IC of the English Language is 0.065
    # The IC of a text written where all letters are
    # equiprobable is 0.038
    #
    # IC is equivalent to the sum from i=1 to 26
    # of c**2/n**2 where n is the length of the
    # string and c is the count of the letter 
    # (corresponding letter of the alphabet) in
    # the message
    #
    def calcIC(self, msg):
        # Determine the letter counts in the message
        counts = self.letCounter.getCounts(msg)
        
        # Determine the squared length of the message
        n = len(msg)**2
        
        # The IC (results from a summation)
        ic = 0
        for letter,num in counts:
            # Since some of the counts could be 0, skip those
            if num == 0:
                continue
            ic += num**2/float(n)
        
        return ic
     
    ## isMonoalphabetic
    # 
    # determines if the IC is closer to the English Language
    # IC or to the IC of text with equiprobable letter occurrence
    #
    # return: whether the IC is closer to english IC or not
    def isMonoalphabetic(self, ic):
        deltaEng = abs(self.ic["english"] - ic)
        deltaEqui = abs(self.ic["equiprobable"] - ic)
        
        return deltaEng > deltaEqui
        
if __name__ == "__main__":
    # initialize the vignere cipher
    vici = VignereCipher()
    
    
    originalMsg = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"
    
    msg = vici.clearMsg(originalMsg)
    
    ic = vici.calcIC(msg)
    
    isMono = vici.isMonoalphabetic(ic)
    
    if isMono:
        ""
    else:
        ""
        
    print "Ciphertext:\n%s\n" % originalMsg
    print "Index of Coincidence (IC): %0.4f\n" % ic
    if isMono:
        print "Message was likely encrypted using a monoalphabetic cipher"
    else:
        print "Message was likely encrypted using a polyalphabetic cipher"
    