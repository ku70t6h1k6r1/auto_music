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
        self.melodyLine2 = None
        self.bassLine = None
        self.voiceProg = None
        self.drumObj = Drums() #Drumの中身どうしよう
        self.effectsObj = Effects()

        self.form = None

    def setKeyProg(self, keyProg):
        self.keyProg = keyProg

    def setChordProg(self, chordProg):
        self.chordProg = chordProg

    def setMelodyLine(self, melodyLine):
        self.melodyLine = melodyLine

    def setMelodyLine2(self, melodyLine):
        self.melodyLine2 = melodyLine

    def setBassLine(self, bassLine):
        self.bassLine = bassLine

    def setVoiceProg(self, voiceProg):
        self.voiceProg = voiceProg

    def setDrumObj(self, drumObj):
        self.drumObj = drumObj

    def setEffectsObj(self, effectsObj):
        self.effectsObj = effectsObj

    def _addScoreObj(self, scoreObj):#old
        self.keyProg  = self._appendPoly(self.keyProg, scoreObj.keyProg)
        self.chordProg  = self._appendPoly(self.chordProg, scoreObj.chordProg)
        self.melodyLine  = self._append(self.melodyLine, scoreObj.melodyLine)
        self.bassLine  = self._append(self.bassLine, scoreObj.bassLine)
        self.voiceProg  = self._appendPoly(self.voiceProg, scoreObj.voiceProg)
        self.drumObj._append(scoreObj.drumObj)
        self.effectsObj._append(scoreObj.effectsObj)


    def addScoreObj(self, scoreObj, useable_Part_list={'melodyLine':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':False}):
        self.keyProg  = self._appendPoly(self.keyProg, scoreObj.keyProg)
        self.chordProg  = self._appendPoly(self.chordProg, scoreObj.chordProg)

        if not useable_Part_list['melodyLine']:
            off_sounds = np.full(len(scoreObj.melodyLine), -1)
            off_sounds[0] = -2
            self.melodyLine  = self._append(self.melodyLine, off_sounds)
        else:
            self.melodyLine  = self._append(self.melodyLine, scoreObj.melodyLine)
        self.form = self._append(self.form, len(self.melodyLine))

        if 'melodyLine2' in useable_Part_list.keys():
            if not useable_Part_list['melodyLine2']:
                off_sounds = np.full(len(scoreObj.melodyLine), -1)
                off_sounds[0] = -2
                self.melodyLine2  = self._append(self.melodyLine2, off_sounds)
            else:
                self.melodyLine2  = self._append(self.melodyLine2, scoreObj.melodyLine)

        if not useable_Part_list['bassLine']:
            off_sounds = np.full(len(scoreObj.bassLine), -1)
            off_sounds[0] = -2
            self.bassLine  = self._append(self.bassLine, off_sounds)
        else:
            self.bassLine  = self._append(self.bassLine, scoreObj.bassLine)

        if not useable_Part_list['voiceProg']:
            off_sounds = np.full( (len(scoreObj.voiceProg[:,0]), 1), tuple([-1]*1) )
            off_sounds[0,0] = -2
            self.voiceProg  = self._appendPoly(self.voiceProg, off_sounds)
        else:
            self.voiceProg  = self._appendPoly(self.voiceProg, scoreObj.voiceProg)

        self.drumObj._append(scoreObj.drumObj, useable_Part_list['drums'])
        self.effectsObj._append(scoreObj.effectsObj, useable_Part_list['effects'])

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
                default[0,:] = [-2]*dif
                score = np.append(score, default, axis = 1)

            elif dif < 0 :
                default = np.full( (len(scoreProp[:,0]), -dif), tuple([-1]*-dif) )
                default[0,:] = [-2]*-dif
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

    def _append(self, drumObj, is_useable):
        if self.kick is None and self.snare is None and self.hihat is None :
            off_sounds = np.full(len(drumObj.kick), -1)
            off_sounds[0] = -2
            self.kick = drumObj.kick if is_useable else off_sounds
            self.snare= drumObj.snare if is_useable else off_sounds
            self.hihat = drumObj.hihat if is_useable else off_sounds
        else:
            off_sounds = np.full(len(drumObj.kick), -1)
            off_sounds[0] = -2
            self.kick = np.append(self.kick, drumObj.kick) if is_useable else np.append(self.kick, off_sounds)
            self.snare = np.append(self.snare, drumObj.snare) if is_useable else np.append(self.snare, off_sounds)
            self.hihat = np.append(self.hihat, drumObj.hihat) if is_useable else np.append(self.hihat, off_sounds)

class Effects:
    def __init__(self):
        self.pt1 = None
        self.pt2 = None
        self.pt3 = None
        self.pt4 = None
        #self._setInstrumentName()

#    def _setInstrumentName(self):
#        self.hihatName = "hihat"
#        self.snareName = "snare"
#        self.kickName = "kick"

    def setPt1(self, array, is_default = False):
        if is_default :
            self.pt1  = array[0:notePerBar_n]
        else:
            self.pt1 = array

    def setPt2(self, array, is_default = False):
        if is_default :
            self.pt2  = array[0:notePerBar_n]
        else:
            self.pt2 = array

    def setPt3(self, array, is_default = False):
        if is_default :
            self.pt3  = array[0:notePerBar_n]
        else:
            self.pt3 = array

    def setPt4(self, array, is_default = False):
        if is_default :
            self.pt4  = array[0:notePerBar_n]
        else:
            self.pt4 = array

    def _append(self, effectsObj, is_useable):
        if self.pt1 is None and self.pt2 is None and self.pt3 is None and self.pt4 is None :
            off_sounds = np.full(len(effectsObj.pt1), -1)
            off_sounds[0] = -2
            self.pt1 = effectsObj.pt1 if is_useable else off_sounds
            self.pt2 = effectsObj.pt2 if is_useable else off_sounds
            self.pt3 = effectsObj.pt3 if is_useable else off_sounds
            self.pt4 = effectsObj.pt4 if is_useable else off_sounds

        else:
            off_sounds = np.full(len(effectsObj.pt1), -1)
            off_sounds[0] = -2
            self.pt1 = np.append(self.pt1, effectsObj.pt1) if is_useable else np.append(self.pt1, off_sounds)
            self.pt2 = np.append(self.pt2, effectsObj.pt2) if is_useable else np.append(self.pt2, off_sounds)
            self.pt3 = np.append(self.pt3, effectsObj.pt3) if is_useable else np.append(self.pt3, off_sounds)
            self.pt4 = np.append(self.pt4, effectsObj.pt4) if is_useable else np.append(self.pt4, off_sounds)
