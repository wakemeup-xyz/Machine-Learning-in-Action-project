0from numpy import *
def loadDataSet():
    return [[1,3,4],[2,3,5,],[1,2,3,5],[2,5]]

def createC1(dataSet):
    C1 =[]
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)  #对 C1 中的每个项构建一个不变集合？？？

def scanD(   D,      Ck,   minSupport): # 选出在数据集中所包含的并且符合条件（大于最小支持度）的候选项集元素
    #     数据集   候选项集    最小支持度
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can) : ssCnt[can] = 1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return    retList,     supportData
    #      大于最小支持度的项  各项的支持度（dict）

def aprioriGen(Lk,k): #create Ck    {0} {1} {2} --->  {01} {12} {02}
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport = 0.5):  #Apriori 算法主函数
    C1 = createC1(dataSet)
    D = map(set,dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(  L,       supportData,      minConf = 0.7):
    # 主函数    频繁项集列表  各项集的支持度（dict） 最小可信度阈值
    bigRuleList = []
    for i in range(1,len(L)): #只获取有两个或更多元素的集合
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            print "freqSet = ",freqSet, " H1 = ", H1
            if (i > 1):
                rulesFromConseq(freqSet,H1,supportData, bigRuleList,minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H , supportData, br1, minConf = 0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            print freqSet-conseq, '--->',conseq,'conf',conf
            br1.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, br1, minConf = 0.7):
    m = len(H[0])
    if (len(freqSet)) > (m + 1):
        Hmp1 = aprioriGen(H, m+1)
        print "Hmp1 = ",Hmp1
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1,minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet,Hmp1,supportData, br1, minConf)



"""
dataSet = loadDataSet()
print "dataSet = ", dataSet

#L1,suppData0 = scanD(D,C1,0.5)
#print "L1 = ", L1

L,suppData = apriori(dataSet)
print "L = ", L

print(aprioriGen(L[0],2))
"""
dataSet = loadDataSet()
print "dataSet = ", dataSet
L, suppData = apriori(dataSet, minSupport = 0.5)
print "L = ", L
rules = generateRules(L, suppData, minConf = 0.5)
print(rules)