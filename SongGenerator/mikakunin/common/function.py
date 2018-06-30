        # coding: UTF-8
import math
import random
import numpy as np
from scipy import stats

def midiNoteToHz(midiNote):
    # ref:https://drumimicopy.com/audio-frequency/
    return 440 * 2**( (midiNote - 69)/12 ) if midiNote > -1 else midiNote

def a16beatToSec( bpm):
    return 60/bpm/4

def toBytes(wave):
    return (wave * float(2 ** (32 - 1) ) ).astype(np.int32).tobytes()

def add(wav_list, w_list):
    len_list = []
    for np_a in wav_list:
        len_list.append(len(np_a))

    length = np.min(np.array(len_list))

    wave = np.zeros(length)
    for idx, np_a in enumerate(wav_list):
        wave = wave + np_a[0:length] * w_list[idx]

    return wave/sum(w_list)

def softmax(a, t = 1):
    temp = np.empty(len(a))

    for i in range(len(a)):
        temp[i] = math.exp(a[i]/t)

    return temp / temp.sum()

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
