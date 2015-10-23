import string

class LetterCounts:
    
    def getCounts(self, msg):
        msgLen = len(msg)
        
        counts = []
        for ch in string.ascii_uppercase:
            counts.append((ch, msg.count(ch)))
        counts = sorted(counts, key=lambda x: -x[1])    
            
        return counts
        
if __name__ == "__main__":   

    letCount = LetterCounts()

    msg = "LTG ZRH JGJ WYE DRK XUC SLK SCG UGZ KWI LXF CSA QUL JRA SWD HZZ HBG NHU MAH RUY PIY LES SSG SLJ RAG DOH NWZ CXK WGZ MIT LJR ABW JSZ SEZ KKD BJO KOZ GQS GJW VOK WVG L"

    counts = letCount.getCounts(msg)
    print counts
    lenMsg = len(msg.replace(' ', ''))
    print lenMsg
    sum = 0
    for letter, count in counts:
        sum += (count*count)/float(lenMsg*lenMsg)
    print sum