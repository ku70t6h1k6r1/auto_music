# coding:utf-8
from Composer import ChordProgression as cp
from Composer import Melody as mel
from Composer import Drums as dr
from Composer import Bass as bs
from Composer import VoiceProgression as vp
from Composer.common import CommonSettings as cs

"""
1.ChordProgression
2.Melody
3.Drums
4.Bass
5.VoiceProgression

"""

class Section:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._methodObject = Methods(self._notePerBar_n)
        self._setMethodName()

    def _setMethodName(self):
        self.defaultChoise = "defaultchoice"

    def create(self, methodName):
        if methodName == self.defaultChoise:
            return self._methodObject.defaultChoise()

class Methods:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n

        self._chordProgressionObj = cp.ChordProgression()
        self._melodyObj = mel.Melody()
        self._drumObj = dr.Drums()
        self._bassObj = bs.Bass()
        self._VoiceProgressionObj = vp.VoiceProgression()

    def defaultChoise(self):
        """
        ref cherryChanges
        """
        scoreObj = cs.Score()
        self._chordProgressionObj.create(self._chordProgressionObj.cherry,  scoreObj, [-1, [0,1], [0,4]])
        self._melodyObj.create(self._melodyObj.cherryA, scoreObj, [69,101],  [True])
        self._drumObj.create(self._drumObj.random, scoreObj)
        self._bassObj.create(self._bassObj.synchroniseKick, scoreObj, [45,60])
        self._VoiceProgressionObj.create(self._VoiceProgressionObj.triad, self._VoiceProgressionObj.synchroniseBass, scoreObj, [45,80])

        return scoreObj

if __name__ == '__main__':
    song = Methods()
    song.defaultChoise()
    print(song.scoreObj.chordProg)
    print(song.scoreObj.melodyLine)
    print(song.scoreObj.voiceProg)
    print(song.scoreObj.bassLine)

    #DRUM
    print("DRUM")
    print(song.scoreObj.drumObj.hihat)
    print(song.scoreObj.drumObj.snare)
    print(song.scoreObj.drumObj.kick)
