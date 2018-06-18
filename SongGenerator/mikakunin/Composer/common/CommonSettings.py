# coding: UTF-8
import math
import random
import numpy as np
from scipy import stats

#commonsettings
notePerBar_n = 16
class GeneratorArg:
    def __init__(self):
        self.methodName = None
        self.scoreObj = None
        self.range = None
        self.generalArg = None

    def setMethodName(self, methodName):
        self.methodName = methodName

    def setScoreObj(self, scoreObj):
        self.scoreObj = scoreObj

    def setRange(self, range):
        self.range = range

    def setGeneralArg(self, generalArg):
        self.generalArg = generalArg

    def reseet(self):
        self.methodName = None
        self.scoreObj = None
        self.range = None
        self.generalArg = None

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

    def addScoreObj(self, scoreObj):
        self.keyProg  = self._appendPoly(self.keyProg, scoreObj.keyProg)
        self.chordProg  = self._appendPoly(self.chordProg, scoreObj.chordProg)
        self.melodyLine  = self._append(self.melodyLine, scoreObj.melodyLine)
        self.bassLine  = self._append(self.bassLine, scoreObj.bassLine)
        self.voiceProg  = self._appendPoly(self.voiceProg, scoreObj.voiceProg)
        self.drumObj._append(scoreObj.drumObj)

    def _append(self, scoreProp, score):
        if scoreProp is None:
            return score
        else:
            return np.append(scoreProp, score)

    def _appendPoly(self, scoreProp, score):
        if scoreProp is None:
            return score
        else:
            dif = len(scoreProp[0,:]) - len(score[0,:])
            if dif > 0 :
                default = np.full( (len(score[:,0]), dif), tuple([-1]*dif ))
                score = np.append(score, default, axis = 1)

            elif dif < 0 :
                default = np.full( (len(scoreProp[:,0]), -dif), tuple([-1]*-dif) )
                scoreProp = np.append(scoreProp, default, axis = 1)

            return np.append(scoreProp, score, axis = 0)

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

    def _append(self, drumObj):
        if self.kick is None and self.snare is None and self.hihat is None :
            self.kick = drumObj.kick
            self.snare= drumObj.snare
            self.hihat = drumObj.hihat
        else:
            self.kick = np.append(self.kick, drumObj.kick)
            self.snare = np.append(self.snare, drumObj.snare)
            self.hihat = np.append(self.hihat, drumObj.hihat)
