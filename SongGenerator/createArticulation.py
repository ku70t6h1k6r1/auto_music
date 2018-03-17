# -*- coding: utf-8 -*-
import numpy as np
import common_function as func

def Create(melody, notePerBar_n = 16, r = 0.95):
    weight = np.zeros(notePerBar_n)
    output = np.zeros(len(melody))
    for i in range(notePerBar_n):
        weight[i] =  r ** i

    for i in range(len(melody)):
        output[i] = weight[i % notePerBar_n]


    return output
