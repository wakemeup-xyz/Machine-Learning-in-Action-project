from numpy import *
import time
def loadSimpData():
    datMat = matrix([[1., 2.1],
                     [2., 1.1],
                     [1.3,1. ],
                     [1., 1. ],
                     [2., 1. ]
    ])
    classLabels = [1.0,1.0,-1.0,-1.0,1.0]
    return datMat,classLabels

def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray = ones((shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray

def buildStump(dataArr,classLabels,D):
    dataMatrix = mat(dataArr);  labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
    minError = inf  #为最小错误率， 由weightedError 更新
    for i in range(n):
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();
        stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt', 'gt']:
                threshVal = (rangeMin + float(j) * stepSize)
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr = mat(ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                weightedError = D.T*errArr
                print "split: dim %d, thresh %.2f, thresh inequal: %s,the weighted error is %.3f " % (i,threshVal,inequal,weightedError)
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClasEst


def adaBoostTrainDS(dataArr,classLabels,numIt = 40):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m) #D 记录每个数据点的权重，其权重和为1
    aggClassEst = mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)
        print "D:",D.T  
        alpha = float(0.5*log((1.0-error)/error))
        #原句为 ： ？？5
        #alpha = float(0.5*log((1.0-error)/max(error,le-16)))

        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print "classEst:",classEst.T
        expon = multiply(-1*alpha*mat(classLabels).T,classEst)
        D = multiply(D,exp(expon))
        D = D/D.sum()
        aggClassEst += alpha*classEst #aggClassEst 记录每个数据点的类别估计累积值 
        print "aggClassEst: ",aggClassEst.T
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1)))
        errorRate = aggErrors.sum()/m
        print "total error: ",errorRate,"\n"
        if errorRate == 0.0 : break
    return weakClassArr,aggClassEst

def adaClassify(datToClass,classifierArr):
    dataMatrix = mat(datToClass)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],classifierArr[i]['ineq'])
        aggClassEst += classifierArr[i]['alpha'] * classEst
        #print aggClassEst
    return sign(aggClassEst)

def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t'))
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat -1 ):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat


def plotROC(predStrengths, classLabels):
    import matplotlib.pyplot as plt
    cur = (1.0,1.0)
    ySum = 0.0 #记录面积
    numPosClas = sum(array(classLabels) == 1.0)  # 实际为正例（TP+FN）
    yStep = 1/float(numPosClas)  # 1/正例
    xStep = 1/float(len(classLabels) - numPosClas) # 1/反例
    sortedIndicies = predStrengths.argsort()
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index] == 1.0:
            delX = 0; delY = yStep
        else:
            delX = xStep; delY = 0
            ySum += cur[1]
        ax.plot([cur[0],cur[0]-delX], [cur[1],cur[1]-delY],c = 'b')
        cur = (cur[0] - delX,cur[1]-delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate')
    plt.title('ROC curve for AdaBoost Horse Colic Detection System')
    ax.axis([0,1,0,1])
    plt.show()
    print "the Area Under the Curve is :",ySum*xStep




#程序运行时间起点
startTime = time.clock()



"""
datMat,classLabels = loadSimpData()
#D = mat(ones((5,1))/5)
#bestStump,minError,bestClasEst = buildStump(datMat,classLabels,D)
#print(bestStump,minError,bestClasEst)
classifierArr = adaBoostTrainDS(datMat,classLabels,30)
adaClassify([0,0],classifierArr)
"""

datArr,labelArr = loadDataSet('/Users/wakemeup/Documents/MLiA/ch07/horseColicTraining2.txt')
classifierArray,aggClassEst = adaBoostTrainDS(datArr,labelArr,1000)

#testArr,testLabelArr = loadDataSet('/Users/wakemeup/Documents/MLiA/ch07/horseColicTest2.txt')
#prediction10 = adaClassify(testArr,classifierArray)
#errArr = mat(ones((67,1)))
#print "the test error rate is " , errArr[prediction10!= mat(testLabelArr).T].sum()/67.0
plotROC(aggClassEst.T,labelArr)






#程序运行时间终点
endTime = time.clock()
print "\n--------program complete : %f s--------" % (endTime-startTime)



"""
运行结果 :
分类器数目   ｜  训练错误率  ｜ 测试错误率 ｜  用时
1               0.284       0.268       0.6s
30                0.21       0.208      18s
100              0.190      0.223       57s
500              0.157      0.253       283s
1000             0.140       0.31       600s
"""