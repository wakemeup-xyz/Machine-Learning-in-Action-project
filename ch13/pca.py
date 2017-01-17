from numpy import *

def loadDataSet(fileName, delim = '\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float,line) for line in stringArr]
    # 对于每个元素： 数值  行数
    return mat(datArr)

def pca(dataMat, topNfeat = 9999999):
    meanVals = mean(dataMat, axis = 0)
    meanRemoved = dataMat - meanVals  #去平均值 得误差？
    covMat = cov(meanRemoved, rowvar= 0)  # covariance 协方差
    eigVals,eigVects = linalg.eig(mat(covMat))    #eig() 为求 eigenvalues 特征值
    eigValInd = argsort(eigVals)                #按照从小到大排序
    eigValInd = eigValInd[: -(topNfeat+1) : -1] # 从后面取从大到小的 topNfeat 个特征值最大的特征向量
    redEigVects =eigVects[:,eigValInd]
    lowDDataMat =meanRemoved * redEigVects    #将数据转换到新空间
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat,reconMat

def replaceNanWithMean():
    datMat = loadDataSet('/Users/wakemeup/Documents/MLiA/ch13/secom.data',' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i]) # 计算所有非 NaN 的平均值
        datMat[nonzero(isnan(datMat[:,i].A))[0],i] = meanVal
    return datMat



"""
dataMat = loadDataSet('/Users/wakemeup/Documents/MLiA/ch13/testSet.txt')
lowDMat, reconMat = pca(dataMat, 1)
#lowDMat, reconMat = pca(dataMat, 2)
#print(lowDMat)
import matplotlib
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dataMat[:,0].flatten().A[0], dataMat[:,1].flatten().A[0], marker = '^', s = 90)
ax.scatter(reconMat[:,0].flatten().A[0], reconMat[:,1].flatten().A[0], marker = 'o', s = 50, c = 'red' )
plt.show()
"""



