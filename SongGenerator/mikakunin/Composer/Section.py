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
        self.paaibbi = "paaibbi"
        self.ppaabbi = "ppaabbi"
        self.piaabbi = "piaabbi"
        self.iaabbi = "iaabbi"
        self.aaba = "aaba"
        self.ab = "ab"
        self.a = "a"
#サビ（ドラムなし）→A→インタールード→アウトロ


    def create(self, methodName):
        if methodName == self.aaba:
            return self._methodObject.aaba()
        elif methodName == self.ab:
            return self._methodObject.ab()
        elif methodName == self.a:
            return self._methodObject.a()
        elif methodName == self.iaabbi:
            return self._methodObject.iaabbi()
        elif methodName == self.piaabbi:
            return self._methodObject.piaabbi()
        elif methodName == self.ppaabbi:
            return self._methodObject.ppaabbi()
        elif methodName == self.paaibbi:
            return self._methodObject.paaibbi()

class Methods:
    def __init__(self):
        return None

    def paaibbi(self):
        p = cs.Score()
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        return [p,a,a,i,b,b,i]

    def ppaabbi(self):
        p = cs.Score()
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        return [p,p,a,a,b,b,i]

    def piaabbi(self):
        p = cs.Score()
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        return [p,i,a,a,b,b,i]

    def iaabbi(self):
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        return [i,a,a,b,b,i]

    def aaba(self):
        a = cs.Score()
        b = cs.Score()
        return [a,a,b,a]

    def ab(self):
        a = cs.Score()
        b = cs.Score()
        return  [a,b]

    def a(self):
        a = cs.Score()
        return [a]

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
