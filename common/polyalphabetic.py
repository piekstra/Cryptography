from letter_frequency import LetterFrequency
if __name__ == "__main__":    
    # parser = argparse.ArgumentParser(description='Encrypt or decrypt a message!')
    # parser.add_argument('-d', '--decrypt', dest='decrypt', action='store_true',
                       # default=False, help='Whether to decrypt the message. \
                       # (Default action is to encrypt the message.)')
    # parser.add_argument('-i', '--invert', dest='invert', action='store_true',
                       # default=False, help='Whether to invert the key. \
                       # (Default action is to not invert the key.)')
    # parser.add_argument('--msg', dest='msg', action='store',
                       # help='The message to encrypt or decrypt.', 
                       # required=True)
    # parser.add_argument('--split', dest='splitN', action='store', type=int,
                       # default=5, help='The size of the split for encrypted plaintext.')
    # parser.add_argument('--key', dest='key', action='store', nargs='+', type=int,
                       # help='The key used to encrypt or decrypt.', 
                       # required=True)

    # args = parser.parse_args()
    letFreq = LetterFrequency()

    msg = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"

    msg = msg.replace(' ' , '')

    col0 = []
    col1 = []
    col2 = []
    col3 = []

    for i in range(0, len(msg), 4):
        col0.append(msg[i])
        col1.append(msg[i+1])
        col2.append(msg[i+2])
        col3.append(msg[i+3])

    msg0 = ''.join(col0)
    msg1 = ''.join(col1)
    msg2 = ''.join(col2)
    msg3 = ''.join(col3)

    print "\ncol1:", letFreq.getFrequencies(msg0)
    print "\ncol2:", letFreq.getFrequencies(msg1)
    print "\ncol3:", letFreq.getFrequencies(msg2)
    print "\ncol4:", letFreq.getFrequencies(msg3)