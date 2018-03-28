# -*- coding: utf-8 -*-
import numpy as np
import common_function as func
import chord_voices as cv
import pitch_weight as pw

def Create(chords, melody, rythm):
    chordObj = cv.Chord()
    pwObj = pw.PitchWeight()

    i = 0
    for note in melody:
        chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][1]
        i = i + 1
