# coding: UTF-8
import numpy as np
import common_function as func
import pitch_weight as pw

def Create(bars_n, notePerBar_n = 16, mergin_n = 16):
    melody = []
    pwObj = pw.PitchWeight()

    for i in range( notePerBar_n  * bars_n + mergin_n ):
        melody.append(func.dice(pwObj.pitchWeight))
    return np.array(melody)

#TEST
#print Create(16)
