# coding: UTF-8
import math
import random
import numpy as np
from scipy import stats

#commonsettings
notePerBar_n = 16


class Score:
    def __init__(self):
        self.keyProg = None #最小単位がnotePerBar_n = 16じゃない
        self.chordProg = None #最小単位がnotePerBar_n = 16じゃない
        self.melodyLine = None
        self.bassLine = None
        self.voiceProg = None
        self.drumObj = Drums() #Drumの中身どうしよう

    def setKeyProg(self, keyProg):
        self.keyProg = keyProg

    def setChordProg(self, chordProg):
        self.chordProg = chordProg

    def setMelodyLine(self, melodyLine):
        self.melodyLine = melodyLine

    def setBassLine(self, bassLine):
        self.bassLine = bassLine

    def setVoiceProg(self, voiceProg):
        self.voiceProg = voiceProg

    def setDrumObj(self, drumObj):
        self.drumObj = drumObj

class Drums:
    def __init__(self):
        self.kick = None
        self.snare = None
        self.hihat = None
        self._setInstrumentName()

    def _setInstrumentName(self):
        self.hihatName = "hihat"
        self.snareName = "snare"
        self.kickName = "kick"

    def setKick(self, array, is_default = False):
        if is_default :
            self.kick  = array[0:notePerBar_n]
        else:
            self.kick = array

    def setSnare(self, array, is_default = False):
        if is_default :
            self.snare  = array[0:notePerBar_n]
        else:
            self.snare = array

    def setHihat(self, array, is_default = False):
        if is_default :
            self.hihat  = array[0:notePerBar_n]
        else:
            self.hihat = array
