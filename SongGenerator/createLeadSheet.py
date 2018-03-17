# -*- coding: utf-8 -*-
import mergeMelodyAndRythm as melody
import createPercussion as perc
import harmonize as hm
import numpy as np
import createArticulation as ac

class SampleComposition:
    def __init__(self):
        self.notePerBar_n = 16
        self.noteParChord_n = 16

        #create leadLine
        self.a_onePhrase_bars = 8
        self.a_loop = 2
        self.a_lastNote = 0
        self.b_onePhrase_bars = 4
        self.b_loop = 4
        self.b_lastNote = 0
        self.vamp_onePhrase_bars = 2
        self.vamp_loop = 4
        self.vamp_lastNote = 0

        self.a = melody.Create(self.a_onePhrase_bars, self.a_loop, self.notePerBar_n, self.a_lastNote)
        self.b = melody.Create(self.b_onePhrase_bars, self.b_loop, self.notePerBar_n, self.b_lastNote)
        self.vamp = melody.Create(self.vamp_onePhrase_bars, self.vamp_loop, self.notePerBar_n, self.vamp_lastNote)

        self.leadLine = np.r_[self.vamp,self.a,self.b,self.vamp]

        #create chordProgeression
        self.chordProgress = hm.Create(self.leadLine, self.noteParChord_n)

        #create rythmSection
        self.perc1 = perc.Create(self.leadLine , temperature = 0.0005)
        self.perc2 = perc.Create(self.leadLine , temperature = 0.001)
        self.perc3 = perc.Create(self.leadLine , temperature = 0.01)
        self.perc4 = perc.Create(self.leadLine , temperature = 0.0004)

        #create articuration
        self.articuration = ac.Create(self.leadLine, notePerBar_n = self.notePerBar_n, r = 0.96)
