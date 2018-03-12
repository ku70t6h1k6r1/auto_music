# coding: UTF-8
import numpy as np
import common_function as func
import rythm_weight as rw


def Create(bars_n, notePerBar_n = 16):
    rwObj = rw.RythmWeight()
    rwObj.setWeight()
    #print rwObj.noteLength
    #print rwObj.noteWeight
    #print rwObj.noteWeightMaster

    noteDuration = func.dice(rwObj.noteWeightMaster)
    rythmLine = np.array(rwObj.noteLength[noteDuration])

    while len(rythmLine) < notePerBar_n  * (bars_n + 1):
        loopFlg = func.dice(rwObj.noteWeight[noteDuration])
        if loopFlg > 0 :
            rythmLine = np.r_[rythmLine,rwObj.noteLength[noteDuration]]
        else:
            noteDuration = func.dice(rwObj.noteWeightMaster)
    return rythmLine[:notePerBar_n  * bars_n]

#TEST
#test = Create(4,16)
#print test
#print len(test)
