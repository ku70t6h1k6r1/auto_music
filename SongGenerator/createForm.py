# -*- coding: utf-8 -*-
import mergeMelodyAndRythm as melody
import harmonize as hm
import numpy as np

def Create(notePerBar_n = 16):
    a = melody.Create(8, 2, notePerBar_n, 2)
    b = melody.Create(4, 4, notePerBar_n, 0)
    output = np.r_[a,b]
    return output

melody =  Create()
chordProgress = hm.Create(melody, 8)
print melody
print chordProgress
