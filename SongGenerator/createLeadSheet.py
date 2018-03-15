# -*- coding: utf-8 -*-
import mergeMelodyAndRythm as melody
import createPercussion as perc
import harmonize as hm
import numpy as np

class SampleComposition:
    def __init__(self):
        self.notePerBar_n = 16
        self.noteParChord_n = 8

        #create leadLine
        self.a_onePhrase_bars = 8
        self.a_loop = 2
        self.a_lastNote = 2
        self.b_onePhrase_bars = 4
        self.b_loop = 4
        self.b_lastNote = 0

        self.a = melody.Create(self.a_onePhrase_bars, self.a_loop, self.notePerBar_n, self.a_lastNote)
        self.b = melody.Create(self.b_onePhrase_bars, self.b_loop, self.notePerBar_n, self.b_lastNote)

        self.leadLine = np.r_[self.a,self.b]

        #create chordProgeression
        self.chordProgress = hm.Create(self.leadLine, self.noteParChord_n)

        #create rythmSection
        self.perc1 = perc.Create(self.leadLine , temperature = 0.0005)
        self.perc2 = perc.Create(self.leadLine , temperature = 0.001)
        self.perc3 = perc.Create(self.leadLine , temperature = 0.01)
        self.perc4 = perc.Create(self.leadLine , temperature = 0.0004)
