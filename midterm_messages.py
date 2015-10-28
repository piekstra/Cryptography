from polyalphabetic_cipher import PolyalphabeticCipher
from monoalphabetic_cipher import MonoalphabeticCipher
from common.frequency_analysis import LetterFrequency
from common.kasiski_test import KasiskiTest

#messages = ["MFE RLH WSR LHW BZN BNW SRX DEC INQ RNW JHL RBW BNL DER HQN DEQ BUJ WSH UZS RNN LDE RDA HJH LQC RWS HUM DTR EHU ICH NWN CDU JRE WSH ULD UDM DCP BWN AER RBW ZHU QRM CHP RIH UPX SRE RHE ZSB LRI RNI BIB WBU HQH WSW FQ", "YBR GPT OOY CBC GUG SNR TCW MVF RMU GJC MUI RCC UZV LJX BAJ DNU RTJ LLF KFF YBL JMZ NWG YNY JYB RRV HCG VLL MGH DKB NCN JHF NRW YNY JDV VTL ZGO RPX IAR QBY PNL YYI RLG YTV LYI GUG SEN OMZ NVA YSS IRP DXR SGS CGR UFS BHP GLN VLX BNI CJP BYT JXG BEJ NHF MZN BSR MYE NGS ZVA BBB REC YBR OCW LVR QFL RNL IER RNZ MSE MRA RGR NHT XGQ FRQ MZL OEY NHF QGI HBG CAI YIC YIU RJU OFT PFM CEC FFY LJF LTR LZG ORP XIE GMQ IBX YYN UVL LMV AYM OAQ PJX GUM ZMN ABI CZR LXC BAQ", "OTG WRV RHU GXO XUQ UEK VYO TSE NYU NSI YSH MHB BUR ZTR CCD DAK MHC ALI OJZ UOT JYC KFN KIO THO GWK Z", "ESP PYR TYP PCE STY VDZ QST DPB FLE TZY DLD LYL AAC ZIT XLE TZY EZC PLW TEJ ESP ASJ DTN TDE EST YVD CPL WTE JTD LYL AAC ZIT XLE TZY EZS TDP BFL ETZ YDE SPX LES PXL ETN TLY OZP DYE NLC P"]#, "JAKXQ SWECW MMJBK TQMCM LWCXJ BNEWS XKRBO IAOBI NOMLJ GUIMH YTACF ICVOE BGOVC WYRCV KXJZV SMRXY VPOVB UBIJK OVCVK RXBOE ASZVR AOXQS WECVO QJHSG ROXWJ MCXQF OIRGZ VRAOJ RJOMB DBMVS CIESX MBDBM VSKRM GYFHA KXQSW ECWME UWXHD QDMXB KPUCN HWIWF NFCKA SKXNF DLJBY RNOBI YFSQN HRIYV IWRQS WCGKC BHRVN SSWYF SQNTS ZNWCT AWWIB SFIWW CTAWW IWWXI RGKRN LZIAW WIWHK PNFBS ASVIE SXMBD BMVSK RMGYC NGKPU CNHWI WFNFC KASKX NFDLJ BYRNO BIYFS QNHRI NBQMW SOVBO IWCVB INWCT AWWIO WFIRG ZVRAO WNJOR RGZVR AORRB OMBDB MVSOP NJORR GZVRA OXQWB XNSXM BDBMV SPMOH OIWWC TAWWI"] # book example problem to test vigenere code!
messages = ["OTG WRV RHU GXO XUQ UEK VYO TSE NYU NSI YSH MHB BUR ZTR CCD DAK MHC ALI OJZ UOT JYC KFN KIO THO GWK Z"]

polyCi = PolyalphabeticCipher()
monCi = MonoalphabeticCipher()
# do it all for me!
for msgNum, msg in enumerate(messages):   
    # 1. Find the Index of Coincidence and use it to decide which are most likely monoalphabetic (Note: I have specifically chosen messages so the IC is a good indicator of whether the message is monoalphabetic).
    msg = msg.replace(' ' , '')
    msgIC = polyCi.calcIC(msg)
    isPoly = polyCi.isPolyalphabetic(msgIC)
    
    print "\nAnalyzing message number %d: %s\n" % (msgNum+1, msg)
    print "Message IC: %.4f" % msgIC
    print "Message is likely %s\n" % ("polyalphabetic" if isPoly else "monoalphabetic")
    
    # 3. For the ones which you suspect aren't monoalphabetic, they have been encrypted either using a Vignere cipher or Hills system. In order to differentiate, we shall apply the standard Vignere tests for keyword - the messages have specifically been chosen so that a Hills system message will be recognizable by how these tests perform. 
    if isPoly:
        # (a) Find all repeated strings of lengths 3 or more and apply the Kasiski test.
        kt = KasiskiTest()        
        repeatedSubstrs = kt.getRepeatedSubstrs(msg, 3)     
        if repeatedSubstrs:
            print "Repeated substrs of length >= 3:\n%s\n" % repeatedSubstrs
            
            print "Potential keys determined by running Kasiski test on each substring:"
            # print out potential key lengths for every substring
            for keyLens in kt.getAllPotentialKeyLens(msg, repeatedSubstrs):
                print keyLens
                
            mostLikelyKeysKasiski = kt.getMostLikelyKeyLens(msg, repeatedSubstrs)
            print "\nMost likely key lengths using Kasiski test:\n%s\n" % (mostLikelyKeysKasiski)
            
            # initialize the letter frequency class
            letFreq = LetterFrequency()
            
            # loop through the top 4 most likely key lengths according to the kasiski test
            for keyLen in mostLikelyKeysKasiski[:2]:
                # Split the message into keyLen columns        
                msgColumns = polyCi.msgSplit(msg, keyLen)
                # holds the potential keyword
                keyword = ""
                # perform frequency analysis on each column
                print "Using the Vigenere Square on the top 4 most frequent letters in each column assuming that each corresponds to 'e' results in the following options:"                
                for idx, column in enumerate(msgColumns):
                    # get the most frequent letter in the column
                    columnFrequencies = letFreq.getFrequencies(''.join(column))[1]
                    mostFrequentLetTuple = columnFrequencies[0]
                    mostFreqLet = mostFrequentLetTuple[0]
                    # for tuple in columnFrequencies[:4]:
                        # print polyCi.vigenereSquareDecrypt(tuple[0], 'e')
                    # print "options above"
                    print "Column", idx+1, [polyCi.vigenereSquareDecrypt(tuple[0], 'e') for tuple in columnFrequencies[:6]]
                    # assuming this letter corresponds to 'e', use the vigenere square
                    # to discover the original keyword letter
                    keywordLet = polyCi.vigenereSquareDecrypt(mostFreqLet, 'e')
                    keyword += keywordLet
                keyword = 'funny'
                print "\nPotential keyword: %s" % keyword
                print "Message deciphered using keyword '%s':\n%s\n" % (keyword, polyCi.vigenereDecrypt(msg,keyword))
        else:
            print "\nKasiski test failed (no repeated substrings with length >= 3)"
        mostLikelyKeyIC = polyCi.getKeywordLength(len(msg), msgIC)
        print "\nMost likely key length using IC test: %0.4f" % (mostLikelyKeyIC)
        
    # 2. For the ones which you guess to be monoalphabetic, do the following:
    else:
        # (a) Run frequency analysis to determine which letters most likely correspond to "e" and "t".
        # (b) Use these correspondences to find the key. 
        # (c) Decrypt the message.        
        plaintext = monCi.decrypt(msg, verbose=True)
        print "Decoded monoalphabetic message: %s" % plaintext
    
    print "\n--------------------------------------------------------------------------------------------\n"    