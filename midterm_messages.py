from polyalphabetic_cipher import PolyalphabeticCipher
from monoalphabetic_cipher import MonoalphabeticCipher
from common.kasiski_test import KasiskiTest

messages = ["MFE RLH WSR LHW BZN BNW SRX DEC INQ RNW JHL RBW BNL DER HQN DEQ BUJ WSH UZS RNN LDE RDA HJH LQC RWS HUM DTR EHU ICH NWN CDU JRE WSH ULD UDM DCP BWN AER RBW ZHU QRM CHP RIH UPX SRE RHE ZSB LRI RNI BIB WBU HQH WSW FQ", "YBR GPT OOY CBC GUG SNR TCW MVF RMU GJC MUI RCC UZV LJX BAJ DNU RTJ LLF KFF YBL JMZ NWG YNY JYB RRV HCG VLL MGH DKB NCN JHF NRW YNY JDV VTL ZGO RPX IAR QBY PNL YYI RLG YTV LYI GUG SEN OMZ NVA YSS IRP DXR SGS CGR UFS BHP GLN VLX BNI CJP BYT JXG BEJ NHF MZN BSR MYE NGS ZVA BBB REC YBR OCW LVR QFL RNL IER RNZ MSE MRA RGR NHT XGQ FRQ MZL OEY NHF QGI HBG CAI YIC YIU RJU OFT PFM CEC FFY LJF LTR LZG ORP XIE GMQ IBX YYN UVL LMV AYM OAQ PJX GUM ZMN ABI CZR LXC BAQ", "OTG WRV RHU GXO XUQ UEK VYO TSE NYU NSI YSH MHB BUR ZTR CCD DAK MHC ALI OJZ UOT JYC KFN KIO THO GWK Z", "ESP PYR TYP PCE STY VDZ QST DPB FLE TZY DLD LYL AAC ZIT XLE TZY EZC PLW TEJ ESP ASJ DTN TDE EST YVD CPL WTE JTD LYL AAC ZIT XLE TZY EZS TDP BFL ETZ YDE SPX LES PXL ETN TLY OZP DYE NLC P"]

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
        if not repeatedSubstrs:
            continue
        print "Repeated substrs of length >= 3:\n%s\n" % repeatedSubstrs
        
        print "Potential keys determined by running Kasiski test on each substring:"
        # print out potential key lengths for every substring
        for keyLens in kt.getAllPotentialKeyLens(msg, repeatedSubstrs):
            print keyLens
            
        mostLikelyKey = kt.getMostLikelyKeyLen(msg, repeatedSubstrs)
        print "\nMost likely key length: %d" % (mostLikelyKey)
        
    # 2. For the ones which you guess to be monoalphabetic, do the following:
    else:
        # (a) Run frequency analysis to determine which letters most likely correspond to "e" and "t".
        # (b) Use these correspondences to find the key. 
        # (c) Decrypt the message.        
        plaintext = monCi.decrypt(msg, verbose=True)
        print "Decoded monoalphabetic message: %s" % plaintext
    
    print "\n--------------------------------------------------------------------------------------------\n"
    
    # col0 = []
    # col1 = []
    # col2 = []
    # col3 = []

    # for i in range(0, len(msg), 4):
        # col0.append(msg[i])
        # col1.append(msg[i+1])
        # col2.append(msg[i+2])
        # col3.append(msg[i+3])

    # msg0 = ''.join(col0)
    # msg1 = ''.join(col1)
    # msg2 = ''.join(col2)
    # msg3 = ''.join(col3)

    # print "\ncol1:", letFreq.getFrequencies(msg0)
    # print "\ncol2:", letFreq.getFrequencies(msg1)
    # print "\ncol3:", letFreq.getFrequencies(msg2)
    # print "\ncol4:", letFreq.getFrequencies(msg3)