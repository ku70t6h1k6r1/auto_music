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
    elif dice([1 - pOn, pOn ]) > 0 :
        return 1
    else :
        return 0

def smoothing(note, pastNote):
    dif  = note - pastNote
    octs =  int(dif / 12) + 1
    if dif > 6:
        note -= 12
    elif dif < -6 :
        note += 12
    else:
        note = note

    return int(note)

def clipping(note, lowestPitch = 60, highestPitch = 84):
    if  highestPitch - lowestPitch + 1 < 12:
        print("ERROR IN CommonFunction 1")
        return None

    if note < lowestPitch:
        while note < lowestPitch :
            note += 12
    elif note >  highestPitch:
        while note > highestPitch :
            note -= 12

    return note

def processing(melody, range):
    for beat, note in enumerate(melody):
        if note > -1:
            if beat > 0:
                melody[beat] = clipping(note, range[0], range[1])
                melody[beat] = smoothing(melody[beat], pastNote)
                pastNote = melody[beat]
            else:
                melody[beat] = clipping(note, range[0], range[1])
                pastNote = melody[beat]

    return melody

#if __name__ == '__main__':
