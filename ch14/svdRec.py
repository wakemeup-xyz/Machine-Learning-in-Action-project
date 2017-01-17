from numpy import *
from numpy import linalg as la

def loadExData():
    return[[0, 0, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1],
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 1, 0, 0]]
    
def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]
#  欧式距离
def eulidSim(inA, inB):
    return 1.0/(1.0 + la.norm(inA- inB))
# 皮尔逊相关系数
def pearsSim(inA, inB):
    if len(inA) < 3 : return 1.0
    return 0.5+0.5*corrcoef(inA, inB, rowvar = 0)[0][1]
# 余弦相似度
def cosSim(inA, inB):
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    return 0.5+0.5*(num/denom)

def standEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]
    simTotal = 0.0; ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0: continue
        overLap = nonzero(logical_and(dataMat[:,item].A > 0, dataMat[:,j].A > 0))[0]
        if len(overLap) == 0 : similarity = 0
        else: similarity = simMeas(dataMat[overLap,item], dataMat[overLap,j])
        print 'the %d and %d similarity is: %f' % (item, j , similarity)
        simTotal += similarity
        ratSimTotal += similarity * userRating 
    if simTotal == 0: return 0
    else : return ratSimTotal/simTotal

def recommend(dataMat, user, N = 3, simMeas = cosSim, estMethod = standEst):
    unratedItems = nonzero(dataMat[user,:].A == 0)[1]
    if len(unratedItems) == 0 : return 'you rated everything'
    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores,key = lambda jj: jj[1], reverse=True)[:N]

def svdEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]
    simTotal = 0.0; ratSimTotal = 0.0
    U, Sigma, VT = la.svd(dataMat)
    Sig4 = mat(eye(4) * Sigma[:4])
    xformedItems = dataMat.T * U[:,:4] * Sig4.I  #构建转换后的物品
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating ==0 or j == item: continue
        similarity = simMeas(xformedItems[item,:].T, xformedItems[j,:].T)
        print 'the %d and %d similarity is : %f' % (item, j, similarity)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else: return ratSimTotal/simTotal

def printMat(inMat, thresh = 0.8):
    for i in range(32):
        for k in range(32):
            if float(inMat[i,k]) > thresh:
                print 1,
            else : print 0,
        print " "

def imgCompress(numSV=3, thresh=0.8):
    my1 = []
    for line in open('/Users/wakemeup/Documents/MLiA/ch14/0_5.txt').readlines():
        newRow = []
        for i in range(32):
            newRow.append(int(line[i]))
        my1.append(newRow)
    myMat = mat(my1)
    print "****original matrix****"
    printMat(myMat, thresh)
    U,Sigma,VT = la.svd(myMat)
    SigRecon = mat(zeros((numSV, numSV)))
    for k in range(numSV):
        SigRecon[k,k] = Sigma[k]
    reconMat = U[:,:numSV] * SigRecon * VT[:numSV,:]
    print "****reconstructed matrix using %d singular values ****" % numSV
    printMat(reconMat, thresh)



"""
myMat = mat(loadExData())
print "欧式距离"
print(eulidSim(myMat[:,0],myMat[:,4]))
print(eulidSim(myMat[:,0],myMat[:,0]))
print "余弦相似度"
print(cosSim(myMat[:,0],myMat[:,4]))
print(cosSim(myMat[:,0],myMat[:,0]))
print "皮尔逊相关系数"
print(pearsSim(myMat[:,0],myMat[:,4]))
print(pearsSim(myMat[:,0],myMat[:,0]))
"""

"""
myMat = mat(loadExData())
myMat[0,1]=myMat[0,0]=myMat[1,0]=myMat[2,0]=4
myMat[3,3]=2
print(myMat)
print(recommend(myMat,2))
"""

"""
myMat = mat(loadExData())
myMat[0,1]=myMat[0,0]=myMat[1,0]=myMat[2,0]=4
myMat[3,3]=2
print(myMat)
U, Sigma, VT = la.svd(mat(loadExData2()))
print(Sigma)
Sig2 = Sigma**2
print "sum(Sig2)", sum(Sig2)
print "sum(Sig2 * 0.9)", sum(Sig2) * 0.9
print "sum(Sig2[:2])" , sum(Sig2[:2])
print "sum(Sig2[:3])", sum(Sig2[:3])
print(recommend(myMat, 1, estMethod = svdEst))
"""

imgCompress(2)