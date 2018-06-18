# coding:utf-8
#使っていないやつ消す。
from Composer import ChordProgression as cp
from Composer import Melody as mel
from Composer import Drums as dr
from Composer import Bass as bs
from Composer import VoiceProgression as vp
from Composer.common import CommonSettings as cs

class Section:
    def __init__(self):
        self._methodObject = Methods()
        self._setMethodName()

    def _setMethodName(self):
        self.aaba = "aaba"
        self.ab = "ab"

    def create(self, methodName):
        if methodName == self.aaba:
            return self._methodObject.aaba()
        elif methodName == self.ab:
            return self._methodObject.ab()

class Methods:
    def __init__(self):
        return None

    def aaba(self):
        a = cs.Score()
        b = cs.Score()
        return [a,a,b,a]

    def ab(self):
        a = cs.Score()
        b = cs.Score()
        return  [a,b]


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
