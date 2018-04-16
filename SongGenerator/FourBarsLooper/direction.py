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
        self.sequence_l = len(self.sequence)
    
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
        
    def sendMsg(self, o, i, cnt): #cnt <= self.sequence_l
        
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
            if self.bass[i] != -1 :
                baOn = func.throwSomeCoins(self.bass[i],4)

                if baOn > 0 :
                    o.note_off(note_past_bs,60, self.bach)
                    o.note_on(self.chordObj.tones[int(self.cds[i] * 1.0 / 8)][self.cds[i]  % 8][0] + 36 , int(85*self.articuration[i]), self.bach)
                    note_past_bs = self.chordObj.tones[int(self.cds[i] * 1.0 / 8)][self.cds[i]  % 8][0] + 36

                if baOn > 0 :
                    o.note_off(note_past_v1,60, self.bkch)
                    o.note_on(self.chordObj.tones[int(self.cds[i] * 1.0 / 8)][self.cds[i]  % 8][1] + 48 , int(30*self.articuration[i]), self.bkch)
                    note_past_v1 = self.chordObj.tones[int(self.cds[i] * 1.0 / 8)][self.cds[i]  % 8][1] + 48

                    o.note_off(note_past_v2,60, self.bkch)
                    o.note_on(self.chordObj.tones[int(self.cds[i] * 1.0 / 8)][self.cds[i]  % 8][2] + 48 , int(30*self.articuration[i]), self.bkch)
                    note_past_v2 = self.chordObj.tones[int(self.cds[i] * 1.0 / 8)][self.cds[i]  % 8][2] + 48

            if i % 64 == 63 :
                if self.sequence[cnt] == 0:
                    self.leadFlg += 1
                    self.lead = self.seqObj.update(self.melody, self.leadFlg)
                elif self.sequence[cnt] == 2:
                    self.chordsFlg += 1
                    self.baFlg += 1
                    self.cds = self.seqObj.update(self.chords, self.chordsFlg)
                    self.bass = self.seqObj.update(self.ba, self.baFlg)
                elif self.sequence[cnt] == 4:
                    self.drFlg += 1
                    self.hh = self.seqObj.update(self.cHH, self.drFlg)
                elif self.sequence[cnt] == 5:
                    self.drFlg2 += 1
                    self.sn = self.seqObj.update(self.sDr, self.drFlg2)
                elif self.sequence[cnt] == 6:
                    self.drFlg3 += 1
                    self.bd = self.seqObj.update(self.bDr, self.drFlg3)

            if cnt == len(sequence):
                flg = Fals
