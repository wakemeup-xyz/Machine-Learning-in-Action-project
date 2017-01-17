import time

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
    def inc(self, numOccur):
        self.count += numOccur
    def disp(self, ind = 1):
        print '  '*ind, self.name, '  ',self.count
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet, minSup = 1):
    headerTable = {}
    for trans in dataSet: #每个集
        for item in trans: #每个元素
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]  #计算该元素总共出现的次数
    for k in headerTable.keys():  #移除不满足阈值要求的元素
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys()) #存储满足阀值要求元素的名字
    if len(freqItemSet) == 0 : return None,None #都不满足阀值要求
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]
    print "first round to calculate count of each item ~~~~~~over"
    retTree = treeNode('Null Set', 1 ,None)
    transSetCount = 0
    for tranSet, count in dataSet.items():
        if transSetCount % 10000 == 0:
            print "transSetCount = %d W" % (transSetCount/10000)
        transSetCount += 1
        localD ={}
        #print "tranSet = ", tranSet
        for item in tranSet:
            if item in freqItemSet: 
                localD[item] = headerTable[item][0]   
        #print "localD = " , localD
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(),key = lambda p: p[1],reverse = True)]   #根据全局频率对每个事务中的元素进行排序
            #print "orderedItems = ", orderedItems
            updateTree(orderedItems,retTree,headerTable, count) # 使用排序后的频率对树进行填充
            
    return retTree, headerTable

def updateTree(  items,           inTree,       headerTable, count):
#            排序后的一个事务的元素  树根节点（相对的）  头指针表    一个事物计数（一般为1））
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0],count, inTree)
        if headerTable[items[0]][1] == None : # 头指针表中该元素还没指向到该节点
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])  # 把新建立的 node 作为headerTable 内这个元素的链表集的最后一位
    if len(items) > 1:
        updateTree(items[1::],inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode): 
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

#############
#发现以给定元素项结尾的所有路径的元素
############
def ascendTree(leafNode, prefixPath): #从某节点追溯往上的路径并添加到 prefixPath
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):  #收集所有该元素的路径 （向右链 ＋ 上溯）
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),key = lambda p: p[1])] #从头指针表的底端开始
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1]) # 收集所有该元素的路径 （向右链 ＋ 上溯）
        #print 'basePat = ',basePat
        #print "condPattBases = ",condPattBases
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:
            #print 'conditional tree for: ',newFreqSet
            #print "myHead = ",myHead
            myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


#程序运行时间起点
startTime = time.clock()



"""
rootNode = treeNode('pyramid', 9, None)
rootNode.children['eye'] = treeNode('eye',13,None)
rootNode.children['phoenix'] = treeNode('phoenix',3,None)
rootNode.disp()
"""


"""
simpDat = loadSimpDat()
print(simpDat)
initSet = createInitSet(simpDat)
print(initSet)
myFPtree, myHeaderTab = createTree(initSet,3)
myFPtree.disp()
tree2,headertab = createTree({frozenset(['x', 's']): 1, frozenset(['z']): 1, frozenset(['y', 'x', 'z']): 1},3)
#print "tree2 = ",tree2
#tree2.disp()
print(findPrefixPath('x',myHeaderTab['x'][1]))
print(findPrefixPath('r',myHeaderTab['r'][1]))
print(findPrefixPath('y',myHeaderTab['y'][1]))
print "________________________________________________________________________________________________"
freqItems = []
mineTree(myFPtree,myHeaderTab, 3, set([]), freqItems)
print "freqItems = ", freqItems
"""

parsedDat = [line.split() for line in open('/Users/wakemeup/Documents/MLiA/ch12/kosarak.dat').readlines()]
print "parsedDat has been  created ~~~~~~~~~~~"
print "len(parsedDat) = ",len(parsedDat)

initSet = createInitSet(parsedDat)
print "initSet has been  created ~~~~~~~~~~~"

myFPtree, myHeaderTab = createTree(initSet,100000)
print "myFPtree has been  created ~~~~~~~~~~~"
midTime = time.clock()
myFreqList = []
mineTree(myFPtree, myHeaderTab, 100000, set([]), myFreqList)
print "myFreqList has been  created ~~~~~~~~~~~"
print(myFreqList)


#程序运行时间终点
endTime = time.clock()
print "\n--------create FPtree use : %f s--------" % (midTime-startTime)
print "\n--------program complete : %f s--------" % (endTime-startTime)