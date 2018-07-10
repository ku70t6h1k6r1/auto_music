# coding: UTF-8
import math
import random
import numpy as np
from scipy import stats

def add(wav_list, w_list):
    len_list = []
    for np_a in wav_list:
        len_list.append(len(np_a))

    length = np.min(np.array(len_list))

    wave = np.zeros(length)
    for idx, np_a in enumerate(wav_list):
        wave = wave + np_a[0:length] * w_list[idx]

    return wave/sum(w_list)
