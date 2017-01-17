from numpy import *
import time

class treeNode():
    def __init__(self,feat,val,right,left):
        featureToSplitOn = feat
        valueOfSplit = val
        rightBranch = right
        leftBranch = left  

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)  #
        dataMat.append(fltLine)       #  将每行映射成浮点数
    return dataMat

def binSplitDataSet(dataSet, feature, value):  
    #               数据     依据哪一列   依据的值
    mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:][0]
    """
    print "dataSet[:,feature] :  type : " , type(dataSet[:,feature])
    print "dataSet[:,feature] :  content : " , dataSet[:,feature]
    print "dataSet[:,feature] > value :", (dataSet[:,feature] > value)
    print "nonzero(dataSet[:,feature] > value) Type : ",type(nonzero(dataSet[:,feature] > value))
    print "nonzero(dataSet[:,feature] > value) : ",nonzero(dataSet[:,feature] > value)
    print
    print "dataSet[nonzero(dataSet[:,feature] > value)[0],:] : ",dataSet[nonzero(dataSet[:,feature] > value)[0],:] 
    #此处的 dataSet[nonzero(dataSet[:,feature] > value)[0],:] 实质为 dataSet[nonzero(dataSet[:,feature] > value)[0][0][0],:]
    print "-------------------"
    """
    mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:][0]
    return mat0,mat1    

def regLeaf(dataSet):
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1]) * shape(dataSet)[0]

def chooseBestSplit(dataSet,leafType = regLeaf, errType = regErr, ops = (1,4)):  #这里的 leafType 和 errType 传入的是两个函数！！
    tolS = ops[0]; tolN = ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:  #tolist() : return the matrix as a (possibly nested) list.
        return None,leafType(dataSet)              #如果所有值相等则退出（叶子节点？）
    m,n = shape(dataSet)
    S = errType(dataSet)
    bestS = inf; bestIndex = 0; bestValue = 0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex]):
            mat0,mat1 = binSplitDataSet(dataSet, featIndex, splitVal)  #splitVal 依次取第 featIndex 列的每一个值，即把 featIndex 列每一行都试着划分一次
            if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if (S - bestS) < tolS:   #如果误差减少不大则退出。。。
        return None,leafType(dataSet)
    mat0,mat1 = binSplitDataSet(dataSet,bestIndex, bestValue)
    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN) : #如果切分出的数据集很小则退出 （叶子节点？）
        return None,leafType(dataSet)
    return bestIndex,bestValue

""" 原版
def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
    tolS = ops[0]; tolN = ops[1]
    #if all the target variables are the same value: quit and return value
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1: #exit cond 1
        return None, leafType(dataSet)
    m,n = shape(dataSet)
    #the choice of the best feature is driven by Reduction in RSS error from mean
    S = errType(dataSet)
    bestS = inf; bestIndex = 0; bestValue = 0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS: 
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    #if the decrease (S-bestS) is less than a threshold don't do the split
    if (S - bestS) < tolS: 
        return None, leafType(dataSet) #exit cond 2
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):  #exit cond 3
        return None, leafType(dataSet)
    return bestIndex,bestValue#returns the best feature to split on
                              #and the value used for that split
"""
def createTree(dataSet, leafType = regLeaf, errType = regErr,ops = (1,4)): #ops 参数用于预剪枝
    feat,val = chooseBestSplit(dataSet,leafType,errType,ops)
    if feat == None: return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet,rSet = binSplitDataSet(dataSet,feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet,leafType,errType,ops)
    return retTree

def isTree(obj):
    return (type(obj).__name__ == 'dict')

def getMean(tree):
    if isTree(tree['right']): tree['right'] = getMean(tree['right'])
    if isTree(tree['left']): tree['left'] = getMean(tree['left'])
    return (tree['left'] + tree['right']) / 2.0

def prune(tree, testData):
    if shape(testData)[0] == 0: return getMean(tree)
    if (isTree(tree['right']) or isTree(tree['left'])):
        lSet,rSet = binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if isTree(tree['left']): tree['left'] = prune(tree['left'],lSet)
    if isTree(tree['right']) : tree['right'] = prune(tree['right'],rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNoMerge = sum(power(lSet[:,-1] - tree['left'],2)) + sum(power(rSet[:,-1] - tree['right'],2))
        treeMean = (tree['left'] + tree['right'])/2.0
        errorMerge = sum(power(testData[:,-1] - treeMean,2))
        if errorMerge < errorNoMerge:
            print "merging"
            return treeMean
        else:
            return tree
    else:
        return tree

def linearSolve(dataSet):
    m,n = shape(dataSet)
    X = mat(ones((m,n)));  Y = mat(ones((m,1)))
    X[:,1:n] = dataSet[:,0:n-1]; Y = dataSet[:,-1]
    xTx = X.T*X
    #print(xTx)
    #print "linalg.det(xTx) = " ,linalg.det(xTx)
    if linalg.det(xTx) == 0.0:
        raise NameError('This matrix is singular, can not do inverse .try increasing the second value of ops')
    ws = xTx.I * (X.T * Y)
    return ws,X,Y

def modelLeaf(dataSet):
    ws,X,Y = linearSolve(dataSet)
    return ws

def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y - yHat,2))

def regTreeEval(model,inDat):
    return float(model)

def modelTreeEval(model, inDat):
    n = shape(inDat)[1]
    X = mat(ones((1,n+1)))
    X[:,1:n+1] = inDat
    return float(X*model)

def treeForeCast(tree, inData, modelEval = regTreeEval):
    if not isTree(tree): return modelEval(tree, inData)
    if inData[tree['spInd']] > tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData, modelEval)
        else:
            return modelEval(tree['left'], inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'], inData,modelEval)
        else:
            return modelEval(tree['right'], inData)

def createForeCast(tree, testData, modelEval = regTreeEval):
    m = len(testData)
    yHat = mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0] = treeForeCast(tree, mat(testData[i]), modelEval)
    return yHat








#程序运行时间起点
startTime = time.clock()

"""
#test for binSplitDataSet

testMat = mat(eye(4))
testMat[0] = [1,1,0,0] 
print(testMat)
mat0,mat1 = binSplitDataSet(testMat,1,0.5)
print(mat0,mat1)
"""

"""
myDat = loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/ex00.txt')
myMat = mat(myDat)
retTree = createTree(myMat)
print(retTree)

myDat2 = loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/ex0.txt')
myMat2 = mat(myDat2)
retTree2 = createTree(myMat2)
print(retTree2)
"""

"""
myDat2 = loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/ex2.txt')
myMat2 = mat(myDat2)
retTree2 = createTree(myMat2)
print(retTree2)
"""

"""
myDat2 = loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/ex2.txt')
myMat2 = mat(myDat2)
myTree = createTree(myMat2,ops=(0,1))
print(myTree)
myDatTest = loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/ex2test.txt')
myMatTest = mat(myDatTest)
myNewTree = prune(myTree,myMatTest)
print(myNewTree)
"""

"""
myDat2 = loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/exp2.txt')
myMat2 = mat(myDat2)
myTree2 = createTree(myMat2,modelLeaf,modelErr,(1,10))
print(myTree2)
"""

trainMat = mat(loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/bikeSpeedVsIq_train.txt'))
testMat = mat(loadDataSet('/Users/wakemeup/Documents/MLiA/ch09/bikeSpeedVsIq_test.txt'))
myTree = createTree(trainMat,ops = (1,20))
yHat = createForeCast(myTree,testMat[:,0])
print(corrcoef(yHat,testMat[:,1],rowvar = 0)[0,1]) # corrcoef() :Return Pearson product-moment correlation coefficients.

myTree = createTree(trainMat,modelLeaf,modelErr,(1,20))
yHat = createForeCast(myTree,testMat[:,0],modelTreeEval)
print(corrcoef(yHat,testMat[:,1],rowvar = 0)[0,1])

ws,X,Y = linearSolve(trainMat)
for i in range(shape(testMat)[0]):
    yHat[i] = testMat[i,0] * ws[1,0] + ws[0,0]
print(corrcoef(yHat,testMat[:,1],rowvar = 0)[0,1])



#程序运行时间终点
endTime = time.clock()
print "\n--------program complete : %f s--------" % (endTime-startTime)
