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

#o = pygame.midi.Output(3)
print ("starting")


class Direction:
    def __init__(self, o, leadSheet):
        self.ldch = 0
        self.ld2ch = 3
        self.bach = 1
        self.bkch = 2
        self.drch = 9
        
        self.note_past = 60
        self.note_past_bs = 60
        self.note_past_v1 = 60
        self.note_past_v2 = 60

        #set inst
        #o.set_instrument(8,0) #Lead
        #o.set_instrument(4,1) #ba
        #o.set_instrument(4,2) #backing
        #o.set_instrument(53,3) #Lead2
        #o.set_instrument(25,9) #drum

        #control change
        o.write_short(0xb0 + self.ldch, 10, 42)
        o.write_short(0xb0 + self.bach, 10, 54)
        o.write_short(0xb0 + self.bkch, 10, 74)
        o.write_short(0xb0 + self.ld2ch, 10, 90)

        #load lead sheet
        #leadSheet = ls.SampleComposition()

        # parse section
        self.melody = leadSheet.leadLine
        self.chords = leadSheet.chordProgress
        self.chordObj = cv.Chord()
        self.ba = leadSheet.perc4
        self.bDr = leadSheet.perc1
        self.sDr = leadSheet.perc2
        self.cHH = leadSheet.perc3
        self.articuration = leadSheet.articuration
    
        #set sequencer
        self.seqObj = seq.Sequencer()
        self.seqObj.crateStepSequence()
        self.sequence = self.seqObj.sequence
    
        self.flg = False
        self.leadFlg = 3
        self.leadFlg2 = -1
        self.chordsFlg = -1
        self.drFlg = -1
        self.drFlg2 = -1
        self.drFlg3 = -1
        self.baFlg = -1

        self.lead = self.seqObj.update(self.melody, self.leadFlg)
        self.cds = np.full(len(self.melody), -1)
        self.bass = np.full(len(self.melody), -1)
        self.hh = np.full(len(self.melody), -1)
        self.sn = np.full(len(self.melody), -1)
        self.bd = np.full(len(self.melody), -1)
        
    def sendMsg(self, o, i, cnt):
        
        if self.flg:
            #Lead
            if self.lead[i] != -1 :
                fixedNote = smoothing(self.lead[i]  + 60, self.note_past)
                
                #part1
                o.note_off(self.note_past, 60, self.ldch)
                o.note_on(fixedNote, int(95*self.articuration[i]) ,self.ldch)
                #part1
                o.note_off(self.note_past + 12, 60, self.ld2ch)
                o.note_on(fixedNote + 12, int(51*self.articuration[i]) ,self.ld2ch)

                self.note_past = fixedNote
            #Dr
            if self.bd[i] != -1 :
                o.note_on(func.dice([1 - self.bd[i] , self.bd[i] ]) * 36, 80, self.drch)

            if self.sn[i] != -1 :
                o.note_on(func.dice([1 - self.sn[i] , self.sn[i] ]) * 39, 80, self.drch)

            if self.hh[i] != -1 :
                o.note_on(func.throwSomeCoins(self.hh[i],20) * 42, int(70*self.articuration[i]), self.drch)

        #Ba
        if bd[i] != -1 :
            baOn = func.throwSomeCoins(bass[i],4)

            if baOn > 0 :
                o.note_off(note_past_bs,60, self.bach)
                o.note_on(chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][0] + 36 , int(85*articuration[i]), self.bach)
                note_past_bs = chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][0] + 36

            if baOn > 0 :
                o.note_off(note_past_v1,60, self.bkch)
                o.note_on(chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][1] + 48 , int(30*articuration[i]), self.bkch)
                note_past_v1 = chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][1] + 48

                o.note_off(note_past_v2,60, self.bkch)
                o.note_on(chordObj.tones[int(cds[i] * 1.0 / 8)][cds[i]  % 8][2] + 48 , int(30*articuration[i]), self.bkch)
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


            #i = 0
            #cnt += 1
            #if cnt == len(sequence):
            #    flg = False
        else  :
            #i += 1

       
##o.note_on(60 ,60,0)
#o.note_on(48, 40, 1)
sleep(6)

#input.close()
o.close()
pygame.midi.quit()
pygame.quit()
exit()
