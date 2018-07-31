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
        self.paasibbis = "paasibbis"
        self.paaibbi = "paaibbi"
        self.ppaabbi = "ppaabbi"
        self.piaabbi = "piaabbi"
        self.pasbbis = "pasbbis"
        self.pasbis = "pasbis"
        self.iaabbi = "iaabbi"
        self.iaabi = "iaabi"
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
        elif methodName == self.iaabi:
            return self._methodObject.iaabi()
        elif methodName == self.ppaabbi:
            return self._methodObject.ppaabbi()
        elif methodName == self.paaibbi:
            return self._methodObject.paaibbi()
        elif methodName == self.paasibbis:
            return self._methodObject.paasibbis()
        elif methodName == self.pasbbis:
            return self._methodObject.pasbbis()
        elif methodName == self.pasbis:
            return self._methodObject.pasbis()

class Methods:
    def __init__(self):
        return None

    def paasibbis(self):
        p = cs.Score()
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        s = cs.Score()
        return [p,a,a,s,i,b,b,i,s]

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

    def pasbbis(self):
        p = cs.Score()
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        s = cs.Score()
        return [p,a,s,b,b,i,s]

    def pasbis(self):
        p = cs.Score()
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        s = cs.Score()
        return [p,a,s,b,i,s]

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

    def iaabi(self):
        i = cs.Score()
        a = cs.Score()
        b = cs.Score()
        return [i,a,a,b,i]

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
