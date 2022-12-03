import random 

class MakeBlock :
    def __init__(self):
        self.valid = 0
        self.tag = None
        self.offset = None

#set 생성
def makeSet() :
    for i in range(256) :
        globals()['set'+str(i)] = []
        for j in range(4) :
            block = MakeBlock()
            globals()['set'+str(i)].append(block)


#caching

def caching(mem) :
    global total_loads 
    global total_stores 
    global load_hits 
    global load_misses 
    global store_hits 
    global store_misses 
    
    temp = mem.split()
    
    sorl = temp[0]
    address = temp[1]
    tag = address[2:7]
    setIndex = int(address[7:9],16)
    offset = int(address[9:10],16)

    if(sorl=='l'):
        total_loads += 1
    else :
        total_stores +=1

    #cache에 있는지 확인
    #set index로 먼저 set 접근
    currentSet= globals()['set'+str(setIndex)]
    isHit=False
    
    # set 내 valid랑 tag 매치 확인
    for item in currentSet :
        #있다면
        if(item.valid == 1 and item.tag == tag):
            #hit
            isHit = True
            #for lru
            currentIndex = currentSet.index(item)
            used = currentSet.pop(currentIndex)
            currentSet.append(used)
            
            if(sorl == 'l'):
                load_hits +=1
            else :
                store_hits +=1
            break


    #없다면
    if(not isHit):
        if(sorl == 'l'):
            load_misses +=1
        else :
            store_misses+=1

        #빈 block이 있는가
        filledSpace = 0
        for item in currentSet :
            if(item.valid ==1) :
                filledSpace +=1
                
        #빈 block 없으므로 교체 정책에 따라
        if(filledSpace >=4):
            #random 정책
            ranNum = random.randrange(0,4)
            currentSet[ranNum].valid = 1
            currentSet[ranNum].tag = tag
            currentSet[ranNum].offset = offset

            #FIFO 정책
            '''currentSet.pop(0)
            newBlock = MakeBlock()
            newBlock.valid =1
            newBlock.tag = tag
            newBlock.offset = offset
            currentSet.append(newBlock)'''

            #lru 정책
            currentSet.pop(0)
            newBlock = MakeBlock()
            newBlock.valid =1
            newBlock.tag = tag
            newBlock.offset = offset
            currentSet.append(newBlock)
        #빈 block 존재
        else :
            for item in currentSet :
                #비어있는 경우
                if(item.valid == 0) :
                    item.valid = 1
                    item.tag = tag
                    item.offset = offset
                    break
            
total_loads = 0
total_stores = 0
load_hits = 0
load_misses = 0
store_hits = 0
store_misses = 0
total_cycles = 0

makeSet()
    
f = open("gcc.trace","r")
while True :
    c = f.readline()
    if c=='':
        break
    caching(c)
f.close()

print("lru 정책")
print("total_loads:",total_loads)
print("total_stores:",total_stores)
print ("load_hits:",load_hits)
print ("load_misses:",load_misses)
print("store_hits:",store_hits)
print("store_misses:",store_misses)


    
