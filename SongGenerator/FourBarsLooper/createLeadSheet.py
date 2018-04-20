# -*- coding: utf-8 -*-
import mergeMelodyAndRythm as melody
import createPercussion as perc
#import harmonize as hm
import harmonize_tf as hm
import numpy as np
import createArticulation as ac
import improvise as counterMelody
import common_function as func


class SampleComposition:
    def __init__(self):
        self.notePerBar_n = 16
        self.noteParChord_n = 16

        #create leadLine
        self.a_onePhrase_bars = 8
        self.a_loop = 4
        self.a_lastNote = 0
        self.b_onePhrase_bars = 8
        self.b_loop = 4
        self.b_lastNote = 0
        self.vamp_onePhrase_bars = 4
        self.vamp_loop = 4
        self.vamp_lastNote = 0

        self.a = melody.Create(self.a_onePhrase_bars, self.a_loop, self.notePerBar_n, self.a_lastNote)
        self.b = melody.Create(self.b_onePhrase_bars, self.b_loop, self.notePerBar_n, self.b_lastNote)
        self.vamp = melody.Create(self.vamp_onePhrase_bars, self.vamp_loop, self.notePerBar_n, self.vamp_lastNote)

        self.leadLine = np.r_[self.a,self.b,self.vamp]

        pastNote = 60 #適切な値は？
        for i, note in enumerate(self.leadLine):
            if note > -1 :
                note = note + 60
                pastNote =  func.smoothing(note, pastNote)
                self.leadLine[i] = pastNote

        #create chordProgeression
        chordObj = hm.Dataset()
        self.chordProgress = hm.Create(self.leadLine, self.noteParChord_n)
        self.bk = perc.Create(self.leadLine , temperature = 0.005)
        self.bk = perc.tranBinary(self.bk , 15)

        #create Bucking
        self.ba = np.full(len(self.leadLine) ,-1)
        self.v1 = np.full(len(self.leadLine) ,-1)
        self.v2 = np.full(len(self.leadLine) ,-1)

        note_ba = 60 #適切な値は
        note_v1 = 60 #適切な値は
        note_v2 = 60 #適切な値は
        for i, chord in enumerate(self.chordProgress):
            if self.bk[i] > 0 :
                note_ba = func.smoothing(chordObj.tones[chord][0] + 36, note_ba, 28, 55)
                note_v1 = func.smoothing(chordObj.tones[chord][1] + 60, note_v1, 50, 70)
                note_v2 = func.smoothing(chordObj.tones[chord][2] + 60, note_v2, 50, 70)

                self.ba[i] = note_ba
                self.v1[i] = note_v1
                self.v2[i] = note_v2

        #create rythmSection *INST_NO +1 -1はOFFSET
        self.hiHat = perc.Create(self.leadLine , temperature = 0.01)
        self.hiHat = perc.tranBinary(self.hiHat, 18) * 43 -1
        self.snare = perc.Create(self.leadLine , temperature = 0.016)
        self.snare = perc.tranBinary(self.snare, 8) * 40 - 1
        self.baDrum = perc.Create(self.leadLine , temperature = 0.007)
        self.baDrum = perc.tranBinary(self.baDrum , 8) * 37- 1

        #create counter melody FUNCTIONとして切り出す？
        self.counterMelody = np.zeros(0)
        for i in range(int(len(self.chordProgress) / self.noteParChord_n)):
            chord_index = self.chordProgress[i * self.noteParChord_n]
            tempCounterMelody = counterMelody.Create(chord_index, self.leadLine[int(i*16) : int(i*16 + 16)], int(1*self.noteParChord_n/self.notePerBar_n) )
            self.counterMelody = np.r_[self.counterMelody, tempCounterMelody ]

        #create articuration
        self.articuration = ac.Create(self.leadLine, notePerBar_n = self.notePerBar_n, r = 0.96)

if __name__ == '__main__':
    obj = SampleComposition()
    print(obj.counterMelody)
