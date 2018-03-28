# -*- coding: utf-8 -*-
import numpy as np
import createLeadSheet_temp as ls
import common_function as func
import chord_voices as cv
import part_weight as seq
import pygame.midi
from time import sleep
import time

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
print("output MIDI:%d" % output_id)
#input = pygame.midi.Input(input_id)
o = pygame.midi.Output(3)
#o = pygame.midi.Output(3)
print ("starting")


note_past = 60
note_past_bs = 60
note_past_v1 = 60
note_past_v2 = 60

#set inst
#o.set_instrument(8,0) #Lead
#o.set_instrument(4,1) #ba
#o.set_instrument(4,2) #backing
#o.set_instrument(53,3) #Lead2
#o.set_instrument(25,9) #drum

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

sleepTime = np.random.normal(0.10,0.04)

i = 0
flg = True
leadFlg = 3
leadFlg2 = -1
chordsFlg = -1
drFlg = -1
drFlg2 = -1
drFlg3 = -1
baFlg = -1

seqObj = seq.Sequencer()
seqObj.crateStepSequence()
sequence = seqObj.sequence
lead = seqObj.update(melody, leadFlg)


cds = np.full(len(melody), -1)
bass = np.full(len(melody), -1)
hh = np.full(len(melody), -1)
sn = np.full(len(melody), -1)
bd = np.full(len(melody), -1)


cnt = 0
while flg:
    start = time.time()

    #Lead
    if lead[i] != -1 :
        o.note_off(note_past, 60, 0)
        fixedNote = smoothing(lead[i]  + 60, note_past)
        o.note_on(fixedNote, int(95*articuration[i]) ,0)

        o.note_off(note_past + 12, 60, 3)
        o.note_on(fixedNote + 12, int(51*articuration[i]) ,3)

        note_past = fixedNote
    #Dr
    if bd[i] != -1 :
        o.note_on(func.dice([1 - bd[i] , bd[i] ]) * 36,80,9)

    if sn[i] != -1 :
        o.note_on(func.dice([1 - sn[i] , sn[i] ]) * 39,80,9)

    if hh[i] != -1 :
        o.note_on(func.throwSomeCoins(hh[i],20) * 42, int(70*articuration[i]) , 9)

    #Ba
    if bd[i] != -1 :
        baOn = func.throwSomeCoins(bass[i],4)

        if baOn > 0 :
            o.note_off(note_past_bs,60, 1)
            o.note_on(chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][0] + 36 , int(85*articuration[i]), 1)
            note_past_bs = chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][0] + 36

        if baOn > 0 :
            o.note_off(note_past_v1,60, 2)
            o.note_on(chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][1] + 48 , int(30*articuration[i]), 2)
            note_past_v1 = chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][1] + 48

            o.note_off(note_past_v2,60, 2)
            o.note_on(chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][2] + 48 , int(30*articuration[i]), 2)
            note_past_v2 = chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][2] + 48

    if i % 64 == 63 :
        if sequence[cnt] == 0:
            leadFlg += 1
            lead = seqObj.update(melody, leadFlg)
        elif sequence[cnt] == 2:
            chordsFlg += 1
            baFlg += 1
            cds = seqObj.update(chords, chordsFlg)
            bass = seqObj.update(ba, baFlg)
        elif sequence[cnt] == 4:
            drFlg += 1
            hh = seqObj.update(cHH, drFlg)
        elif sequence[cnt] == 5:
            drFlg2 += 1
            sn = seqObj.update(sDr, drFlg2)
        elif sequence[cnt] == 6:
            drFlg3 += 1
            bd = seqObj.update(bDr, drFlg3)


        i = 0
        cnt += 1
        if cnt == len(sequence):
            flg = False
    else  :
        i += 1

    end = time.time()

    sleep(sleepTime - (end - start))
##o.note_on(60 ,60,0)
#o.note_on(48, 40, 1)
sleep(6)

#input.close()
o.close()
pygame.midi.quit()
pygame.quit()
exit()
