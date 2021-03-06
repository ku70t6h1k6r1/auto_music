# coding: UTF-8
import math
import random
import numpy as np
from scipy import stats

def sigmoid(a):
    return 1.0 / (1.0 + math.exp(-a))

def softmax(a, t = 1):
    temp = np.empty(len(a))

    for i in range(len(a)):
        temp[i] = math.exp(a[i]/t)

    return temp / temp.sum()

def simpleStd(a):  
    return a / a.sum()

def dice(pkIn):
    xk = np.arange(len(pkIn))
    pk = (pkIn)
    custm = stats.rv_discrete(name='custm', values=(xk, pk))
    return (custm.rvs(size=1))[0]

def throwSomeCoins(pOn, n):
    pOn = pOn * n

    if pOn > 1 :
        return 1
    elif dice([1 - pOn, pOn ]) > 1 :
        return 1
    else :
        return 0
