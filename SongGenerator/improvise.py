# -*- coding: utf-8 -*-
import numpy as np
import math
import common_function as func
import harmonize_tf as hm
import pitch_weight as pw
import createMelody as mel
import createRythm as rythm
import mergeMelodyAndRythm

def Create(chord_idx, melody, bars_n, notePerBar_n = 16, ct_w = 1.5):
    """
    chordは一つだけ
    ct_w は大きい方がインサイド

    """
    #create melody
    chordObj = hm.Dataset()
    pitchObj = pw.PitchWeight()

    melody_hist = chordObj.translateMelody(melody)
    chord_tone = chordObj.tones[chord_idx]

    pitch_weight_a = np.zeros(12)
    pitch_weight_a[chord_tone] = ct_w #コードトーンの重さ

    for note, n in enumerate(melody_hist) :
        pitch_weight_a[note] += n

    pitchObj.updatePW(pitch_weight_a, std_f = 'simpleStd')

    improvise_melody  = mel.Create(bars_n, notePerBar_n = notePerBar_n, std_f = 'simpleStd', pwObj = pitchObj)

    #create rythm
    improvise_rythm = rythm.Create(bars_n, notePerBar_n = notePerBar_n )

    return mergeMelodyAndRythm.Merge(improvise_rythm, improvise_melody, bars_n, 1, notePerBar_n, lastNote = 0)



if __name__ == '__main__':
    print(Create(0, [0,2,4,5,7,9,11,0,2,4,5,7,9,11,0,2,4,5,7,9,11,0,2,4,5,7,9,11],2))
