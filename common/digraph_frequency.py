import string

class DigraphFrequency:
    
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
 
if __name__ == "__main__":    
    # manual run
    diFreq = DigraphFrequency()
    #testMsg = "STB RDX TZQ MFY MJQ GTB WTT RXM FPJ XUJ FWJ MFI PNS LOT MSX FDF UUF WJS YQD MJB FXS YTS YMJ BFX MNS LYT SGJ QYB FDF YYM JYN RJ"
    #testMsg = "KFHYY GIGMC EJSST EBOEU GRWJT SDVYK ZOZLI ZKFHX KUUIC WXFWJ GAXQP BQAGV GXDVD GUEVG MIGYK QQPIP SCLLF YPMUL KFHXP MHGME VDKAV YQCEG UEALY YYZSZ MPXZO CTXTR IMDID VDGSX OZFFT SMEDV MEIMD VMPKO UJKOD UBOAX BOORS LPZCW IMDVY GJWMI FQ"
    testMsg = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"
    #testMsg = "HZD UGQ OBK GHZ TGY KOB HZP QNS XV"
    testMsg = testMsg.replace(' ', '')
    print testMsg
    print "Ciphertext digraph frequencies:\n%s\n" % diFreq.getFrequencies(testMsg)
    print "Common digraph frequencies:\n%s\n" % diFreq.getDigraphFrequencies()