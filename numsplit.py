
The following message was encrypted using an RSA with p=899809363, q=982451653 and public key e=334214467
 

643877753679548435, 866292537275322330, 254748148578229380, 71138974994887714, 222645256501525868, 679882255230499927, 819816742241006630, 577742589253578360, 833787219953584998, 138795253479420573, 530705632385445762, 804290049605549707, 15688874561665654, 764453583216645513, 648472557086646285, 317057428507657618, 534154217500032982, 489963676396102764, 764564117374117737, 544497681776975040
Decrypt the message to determine how to access the next message. Once you have decrypted the message, make sure to answer all the questions below. You have one attempt at each!

084104101032112097115115119111114100032102111114032116104101032110101120116032113117105122032105115032104101108108111046032084104101032112097115115119111114100032102111114032116104101032116104105114100032113117105122032105115032116104101032100101103114101101032111102032116104101032076070083082032105110032116104101032110101120116032113117105122046013010

'084 104 101 032 112 097 115 115 119 111 114 100 321 021 111 140 321 161 041 010 321 101 011 201 160 321 131 171 051 220 321 051 150 321 041 011 081 081 110 460 320 841 041 010 321 120 971 151 151 191 111 141 000 321 021 111 140 321 161 041 010 321 161 041 051 141 000 321 131 171 051 220 321 051 150 321 161 041 010 321 001 011 031 141 011 010 321 111 020 321 161 041 010 320 760 700 830 820 321 051 100 321 161 041 010 321 101 011 201 160 321 131 171 051 220 460 130 10 '
>>>
mstr = "084104101032112097115115119111114100032102111114032116104101032110101120116032113117105122032105115032104101108108111046032084104101032112097115115119111114100032102111114032116104101032116104105114100032113117105122032105115032116104101032100101103114101101032111102032116104101032076070083082032105110032116104101032110101120116032113117105122046013010"

newStr = ""
for i in range(0, len(mstr), 3):
    newStr += chr(int(mstr[i:i+3]))
    
print newStr

quiz1
Trying decryption key: [[25, 1], [6, 15]], encryption key [[-15, 1], [6, -25]]
thisisthetakehomeportionoftheexamyouwillhavetobreaksixcryptosystemseachonewillgiveinformationonhowtodecodethenextforthenextsystemlogintothemoodlepageandtakethefirstquizthepasswordisfeetmakesuretoanswerallquestionsalongthewayasitwillbepartofyourgradex

quiz2
The password for the next quiz is hello. The password for the third quiz is the degree of the LFSR in the next quiz.

quiz3
def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])
    
def xor(b1, b2):
    return str(ord(b1) ^ ord(b2))
    
mstr = "star"

binStr = ""
for c in mstr:
    bin = baseN(ord(c), 2)
    binStr += str(bin).zfill(8)
    
c = "10000101001100111000110111111101"
print "msg", binStr
print "c  ", c

key = ""
cIdx = 0
for idx, b in enumerate(c):
    key += xor(b, binStr[idx])

print "key", key
print "keylen:", len("110110010001111")

"key"
"110110010001111"
"degree 4"

quiz4
Decrypting:
        [1631, 3276, 1086, 2548, 1631]
Using public key:
        [181, 182, 362, 649, 939, 438, 813, 542]
        b = 996
        m = 1459

Calculated key sequence:
        [819, 356, 179, 67, 25, 7, 3, 2]
Calculated msg segments:
        [609, 572, 537, 607, 609]

Binary segments found using calculated key and msg
segments as the 'V' in the knapsack problem:
        Bin             Dec     Let
        01110100        116     t
        01101111        111     o
        01100001        97      a
        01110011        115     s
        01110100        116     t

Decrypted Message: toast

quiz 5:
python monoalphabetic_cipher.py --msg "DHY NIL AJG LAF HYR THJ LIV HYV PHI VPV RRL NVL BLT EIH PUV FYN EFY FRW VMA WVY VKA PVR RLN VFR DHY ALF YVM FYL YVY SVG HQV FYA WVA HQU HKH JAR FMV HEP THE EFD VAW VGV AAV IBF GGU VLM MIV RRV MAH THJ IAV PQH ILI TLG FLR BWF DWF RHY VHE AWV PIP VYL DHG GVD AFH YHE DWL ILD AVI REI HPD WFG MIV YRU HHX RTH JIL GFL RFR PIY HYR VYR V" --mfc V A
Attempting to decipher:
DHYNILAJGLAFHYRTHJLIVHYVPHIVPVRRLNVLBLTEIHPUVFYNEFYFRWVMAWVYVKAPVRRLNVFRDHYALFYVMFYLYVYSVGHQVFYAWVAHQUHKHJARFMVHEPTHEEFDVAWVGVAAVIBFGGUVLMMIVRRVMAHTHJIAVPQHILITLGFLRBWFDWFRHYVHEAWVPIPVYLDHGGVDAFHYHEDWLILDAVIREIHPDWFGMIVYRUHHXRTHJILGFLRFRPIYHYRVYRV

Ciphertext Letter Frequencies:
[('V', 13.360323886639677), ('H', 10.526315789473683), ('R', 7.6923076923076925), ('Y', 7.6923076923076925), ('F', 7.28744939271255), ('L', 7.28744939271255), ('A', 6.477732793522267), ('I', 6.477732793522267), ('G', 4.048582995951417), ('P', 4.048582995951417), ('D', 3.643724696356275), ('W', 3.643724696356275), ('E', 3.2388663967611335), ('M', 2.834008097165992), ('T', 2.42914979757085), ('J', 2.0242914979757085), ('N', 1.6194331983805668), ('U', 1.6194331983805668), ('B', 1.214574898785425), ('Q', 1.214574898785425), ('K', 0.8097165991902834), ('S', 0.4048582995951417), ('X', 0.4048582995951417), ('C', 0.0), ('O', 0.0), ('Z', 0.0)]

English Language Letter Frequencies:
[('e', 12.702), ('t', 9.056), ('a', 8.167), ('o', 7.507), ('i', 6.966), ('n', 6.749), ('s', 6.327), ('h', 6.094), ('r', 5.987), ('d', 4.253), ('l', 4.025), ('c', 2.782), ('u', 2.758), ('m', 2.406), ('w', 2.36), ('f', 2.228), ('g', 2.015), ('y', 1.974), ('p', 1.929), ('b', 1.492), ('v', 0.978), ('k', 0.772), ('j', 0.153), ('x', 0.15), ('q', 0.095), ('z', 0.074)]

Using letter in ciphertext: V
        with frequency: 13.36%
Using letter in ciphertext: A
        with frequency: 6.48%

Assuming that V is equivalent to e
Assuming that A is equivalent to t

Key: (9, 9)

Plaintext:
congratulationsyouareonemoremessageawayfrombeingfinishedthenextmessageiscontainedinanenvelopeinthetopboxoutsideofmyofficetheletterwillbeaddressedtoyourtemporaryaliaswhichisoneofthemrmenacollectionofcharactersfromchildrensbooksyouraliasismrnonsense

efrgdckylmvzsneafyhmxvgrmebidfjvjizccqeeurkeupfvdqtksfupzwhfivxawgysmqrfvtuqesffjvjizccixmopsuzgvhtaifxofjvgogtjimaqupeigstasgrrdpqnrlacuxhqvroetqdifuprpfunvmtuugeseyfvdbtfxeovvhttggeseyfwdngzrgnkjguuvjgoziietgnrxiapjegmke

EFRGDCKYLMVZSNEAFYHMXVGRMEBIDFJVJIZCCQEEURKEUPFVDQTKSFUPZWHFIVXAWGYSMQRFVTUQESFFJVJIZCCIXMOPSUZGVHTAIFXOFJVGOGTJIMAQUPEIGSTASGRRDPQNRLACUXHQVROETQDIFUPRPFUNVMTUUGESEYFVDBTFXEOVVHTTGGESEYFWDNGZRGNKJGUUVJGOZIIETGNRXIAPJEGMKE

CREAM	CONGRATULATIONSYOUHAVECRACKEDTHEFINALMESSAGEINORDERTOFINISHTGETAKEHOMEPORTIONOFTHEFINALEXAMYOUNEEDTOGOTOTHECOURSEMOODLEWEBPAGEANDDOWNLOADTHETAKEHOMEFINALFILEITISPASSWORDPROTECTEDTHEPASSWOSDBEINGBISCUITSCONGRATULATIONSAGAIN

CONGRATULATIONS YOU HAVE CRACKED THE FINAL MESSAGE IN ORDER TO FINISH TGE TAKE HOME PORTION OF THE FINAL EXAM YOU NEED TO GO TO THE COURSE MOODLE WEB PAGE AND DOWNLOAD THE TAKE HOME FINAL FILE IT IS PASSWORD PROTECTED THE PASSWOSD BEING BISCUITS CONGRATULATIONS AGAIN

    
    