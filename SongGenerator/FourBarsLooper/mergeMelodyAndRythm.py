# -*- coding: utf-8 -*-
import createRythm as rythm
import createMelody as pitch
import numpy as np

#rehC
def Create(bars_n, loop_n, notePerBar_n = 16, lastNote = 0):
    reh_rythm = rythm.Create(bars_n, notePerBar_n = notePerBar_n )
    reh_pitch = pitch.Create(bars_n, notePerBar_n = notePerBar_n )
    rev_reh_rythm = reh_rythm[::-1]
    rev_reh_pitch  = reh_pitch[::-1]

    onsetIndex = np.where(rev_reh_rythm == 1)
    firstDoIndex = np.min(np.where(rev_reh_pitch == lastNote))

    reh_melody = np.full(bars_n*notePerBar_n, -1)

    j = 0
    onsetIndex = list(onsetIndex[0])
    for i in onsetIndex:
        reh_melody[i] = rev_reh_pitch[firstDoIndex + j]
        j += 1

    melody = reh_melody[::-1]
    for i in range(loop_n - 1 ):
        melody = np.r_[melody,reh_melody[::-1]]

    return melody

def Merge(reh_rythm, reh_pitch, bars_n, loop_n, notePerBar_n = 16, lastNote = 0):
    rev_reh_rythm = reh_rythm[::-1]
    rev_reh_pitch  = reh_pitch[::-1]

    onsetIndex = np.where(rev_reh_rythm == 1)
    firstDoIndex = np.min(np.where(rev_reh_pitch == lastNote))

    reh_melody = np.full(bars_n*notePerBar_n, -1)

    j = 0
    onsetIndex = list(onsetIndex[0])
    for i in onsetIndex:
        reh_melody[i] = rev_reh_pitch[firstDoIndex + j]
        j += 1

    melody = reh_melody[::-1]
    for i in range(loop_n - 1 ):
        melody = np.r_[melody,reh_melody[::-1]]

    return melody


#TEST
#test = Create(16,3)
#print test
#print len(test)
