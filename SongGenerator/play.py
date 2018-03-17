# -*- coding: utf-8 -*-
import numpy as np
import createLeadSheet as ls
import common_function as func
import chord_voices as cv
import pygame.midi
from time import sleep

def smoothing(note, pastNote, lowestPitch = 60, highestPitch = 80):
    if (note - pastNote) > 5  and note > lowestPitch:
        note = note - 12
    elif (note - pastNote) < -6 and note < highestPitch:
        note = note + 12
    else:
        note = note

    return int(note)



pygame.init()
pygame.midi.init()
#input_id = pygame.midi.get_default_input_id()
output_id = pygame.midi.get_default_output_id()
#print("input MIDI:%d" % input_id)
#print("output MIDI:%d" % output_id)
#input = pygame.midi.Input(input_id)
o = pygame.midi.Output(output_id)

print ("starting")

i = 0
note_past = 60
note_past_bs = 60
note_past_v1 = 60
note_past_v2 = 60

#set inst
o.set_instrument(8,0) #Lead
o.set_instrument(4,1) #ba
o.set_instrument(4,2) #backing
o.set_instrument(53,3) #Lead2
o.set_instrument(25,9) #drum

#control change
o.write_short(0xb0, 10, 42)
o.write_short(0xb1, 10, 54)
o.write_short(0xb2, 10, 74)
o.write_short(0xb3, 10, 90)

#load part
leadSheet = ls.SampleComposition()
melody = leadSheet.leadLine
chords = leadSheet.chordProgress
chordObj = cv.Chord()
ba = leadSheet.perc4
bDr = leadSheet.perc1
sDr = leadSheet.perc2
cHH = leadSheet.perc3

articuration = leadSheet.articuration

sleepTime = np.random.normal(0.15,0.1)
for note in melody:

    #Lead
    if note != -1 :
        o.note_off(note_past, 60, 0)
        fixedNote = smoothing(note + 60, note_past)
        o.note_on(fixedNote, int(45*articuration[i]) ,0)

        o.note_off(note_past, 60, 3)
        o.note_on(fixedNote, int(21*articuration[i]) ,3)

        note_past = fixedNote
    #Dr
    if i % leadSheet.notePerBar_n == 0:
        o.note_on(36, 50, 9)
    else:
        o.note_on(func.dice([1 - bDr[i] , bDr[i] ]) * 36,50,9)
        o.note_on(func.dice([1 - sDr[i] , sDr[i] ]) * 39,50,9)

    #throwSomeCoins
    o.note_on(func.throwSomeCoins(cHH[i],20) * 42, int(21*articuration[i]) , 9)
    #o.note_on(42,20,9)

    #Ba
    #baOn = dice([1 - ba_rythm[i] , ba_rythm[i] ]) + dice([1 - ba_rythm[i] , ba_rythm[i] ]) + dice([1 - ba_rythm[i] , ba_rythm[i] ])
    baOn = func.throwSomeCoins(ba[i],4)
    if baOn > 0:
        #print melodyObj.voice[0][0]
        o.note_off(note_past_bs,60, 1)
        o.note_on(chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][0] + 36 , int(25*articuration[i]), 1)
        note_past_bs = chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][0] + 36

        o.note_off(note_past_v1,60, 2)
        o.note_on(chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][1] + 48 , int(27*articuration[i]), 2)
        note_past_v1 = chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][1] + 48

        o.note_off(note_past_v2,60, 2)
        o.note_on(chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][2] + 48 , int(27*articuration[i]), 2)
        note_past_v2 = chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][2] + 48

    i += 1
    sleep(sleepTime)
##o.note_on(60 ,60,0)
#o.note_on(48, 40, 1)
sleep(6)

#input.close()
o.close()
pygame.midi.quit()
pygame.quit()
exit()
