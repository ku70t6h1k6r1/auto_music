# coding: UTF-8
import numpy as np
import common_function as func
import pitch_weight as pw

#Simple Function
#def Create(bars_n, notePerBar_n = 16, mergin_n = 16):
#    melody = []
#    pwObj = pw.PitchWeight()

#    for i in range( notePerBar_n  * bars_n + mergin_n ):
#        melody.append(func.dice(pwObj.pitchWeight))
#    return np.array(melody)

def Create(bars_n, notePerBar_n = 16, mergin_n = 16, std_f = 'softmax', pwObj = pw.PitchWeight()):
    """
    pwObj = pw.PitchWeight()はカスタマイズする必要がある時だけ引数にいれる。
    """
    melody = []

    #set first situation
    #prevNote = func.dice(pwObj.pitchWeight)
    prevNote = 0

    for i in range( notePerBar_n  * bars_n + mergin_n ):
        pwObj.updateDW((notePerBar_n * bars_n) * 1.0 / (i+1))
        pwObj.updateRelPW(prevNote, std_f = std_f)
        prevNote = func.dice(pwObj.relPitchWeight)
        melody.append(prevNote)
    return np.array(melody)

#TEST
#print Create(16)
