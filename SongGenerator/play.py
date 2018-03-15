# -*- coding: utf-8 -*-
import numpy as np
import createLeadSheet as ls
import common_function as func
import chord_voices as cv
import pygame.midi
from time import sleep

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

#load part
leadSheet = ls.SampleComposition()
melody = leadSheet.leadLine
chords = leadSheet.chordProgress
chordObj = cv.Chord()
ba = leadSheet.perc4
bDr = leadSheet.perc1
sDr = leadSheet.perc2
cHH = leadSheet.perc3


sleepTime = np.random.normal(0.2,0.1)
for note in melody:

    #Lead
    if note != -1 :
        o.note_off(note_past, 60, 0)
        o.note_on(note + 60,int(np.random.normal(45,5)),0)

        o.note_off(note_past, 60, 3)
        o.note_on(note + 60,int(np.random.normal(21,5)),3)

        note_past = note + 60
    #Dr
    if i % leadSheet.notePerBar_n == 0:
        o.note_on(36, 50, 9)
    else:
        o.note_on(func.dice([1 - bDr[i] , bDr[i] ]) * 36,50,9)
        o.note_on(func.dice([1 - sDr[i] , sDr[i] ]) * 39,50,9)

    #throwSomeCoins
    o.note_on(func.throwSomeCoins(cHH[i],20) * 42,20,9)
    #o.note_on(42,20,9)

    #Ba
    #baOn = dice([1 - ba_rythm[i] , ba_rythm[i] ]) + dice([1 - ba_rythm[i] , ba_rythm[i] ]) + dice([1 - ba_rythm[i] , ba_rythm[i] ])
    baOn = func.throwSomeCoins(ba[i],4)
    if baOn > 0:
        #print melodyObj.voice[0][0]
        o.note_off(note_past_bs,60, 1)
        o.note_on(chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][0] + 36 , int(np.random.normal(25,8)), 1)
        note_past_bs = chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][0] + 36

        o.note_off(note_past_v1,60, 2)
        o.note_on(chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][1] + 48 , int(np.random.normal(27,8)), 2)
        note_past_v1 = chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][1] + 48

        o.note_off(note_past_v2,60, 2)
        o.note_on(chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][2] + 48 , int(np.random.normal(27,8)), 2)
        note_past_v2 = chordObj.tones[int(chords[i] * 1.0 / 8)][chords[i]  % 8][2] + 48

    i += 1
    sleep(sleepTime)
o.note_on(60 ,60,0)
o.note_on(48, 40, 1)
sleep(4)

#input.close()
o.close()
pygame.midi.quit()
pygame.quit()
exit()
