from numpy import *


def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]
    return postingList,classVec

def createVoacList(dataSet):
    vocabSet = set([])
    for document in dataSet:            #创建一个空集
        vocabSet = vocabSet | set(document)#创建两个集合的并集
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):   
    returnVec = [0] * len(vocabList)   #创建一个其中所含元素都是0的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word: %s is not in my vocabulary!" % word
    return returnVec
 


def trainNBO(trainMatrix,trainCategory):
    
    numTrainDocs = len(trainMatrix)   #段数
    numWords = len(trainMatrix[0])  #总词数l
    #初始化概率
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i]  == 1:
            p1Num += trainMatrix[i]
            #print(p1Num)
            #print(trainMatrix[i])
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    print "p1NUM = "
    #print (p1Num)
    p1Vect = log(p1Num/p1Denom) 
    p0Vect = log(p0Num/p0Denom)
 
    return p0Vect, p1Vect, pAbusive 
#          p(w|c0) p(w|c1) p(c1)

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVoacList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNBO(array(trainMat),array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            print(vocabList.index(word))
            returnVec[vocabList.index(word)] += 1
    return returnVec



#testingNB()
#mySent = 'This book is aaa ddd ml.l. aaa  eee aa'
#print(mySent.split())
#import re 
#regEx = re.compile('\\W*')
#listOfTokens = regEx.split(mySent)
#print(listOfTokens)
#newListOfToken = [tok.lower() for tok in listOfTokens if len(tok) >0]
#print(newListOfToken)


def textPrase(bigString):
    import re
    listOfTokens = re.split(r'\W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    docList=[]; classList=[]; fullText = []
    for i in range(1,26):
        wordList = textPrase(open('/Users/wakemeup/Documents/MLiA/ch04/email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textPrase(open('/Users/wakemeup/Documents/MLiA/ch04/email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVoacList(docList)
    trainingSet =range(50); testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = [];  trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNBO(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        print(wordVector)
        if classifyNB(array(wordVector),p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1 
    print 'the error rate is: ',float (errorCount)/len(testSet)


def calcMotstFreq(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(),key = operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

def localWords(feed1, feed0):
    import feedparser
    docList = []; classList=[];  fullText = []
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textPrase(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textPrase(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVoacList(docList)
    top30Words = calcMotstFreq(vocabList,fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet))) #return a random number from 0 to len(trainingSet)
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))    
        trainClasses.append(classList[docIndex])
    p0V,p1V, pSpam = trainNBO(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is : ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V



def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V = localWords(ny,sf)
    topNY = []; topSF = [];
    for i in range(len(p0V)):
        if p0V[i] > -5.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -5.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair:pair[1], reverse=True)
    print "SFSFSFSFSFSFSFSF"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair:pair[1], reverse=True)
    print "NYNYNYNYNNYNYNYN"
    for item in sortedNY:
        print item[0]



import feedparser
ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
vocabList,pSF,pNY = localWords(ny,sf)
getTopWords(ny,sf)
#print(ny)



