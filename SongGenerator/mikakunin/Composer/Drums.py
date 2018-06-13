# coding:utf-8
#default
import numpy as np

#option
from Composer import _DrumsPatternSet as drPtn
from Composer.common import CommonSettings as cs

class Drums:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._methodsObject = Methods(notePerBar_n = 16)
        self._setMethodName()

    def _setMethodName(self):
        self.random = "random"

    def create(self, methodName, scoreObj):
        if methodName == self.random:
            drumObj = self._methodsObject.randomChoise(scoreObj.chordProg)
            scoreObj.setDrumObj(drumObj)

class Methods:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._pattrensObj = drPtn.Patterns()
        self._patterns = self._pattrensObj.list
        self.drumObj = cs.Drums()


    def randomChoise(self, chordProg):
        idx = np.random.randint(0, len(self._patterns), 1)[0]
        hihatScore = np.tile(self._patterns[idx].hihat, len(chordProg))
        snareScore = np.tile(self._patterns[idx].snare, len(chordProg))
        kickScore = np.tile(self._patterns[idx].kick, len(chordProg))

        self.drumObj.setHihat(hihatScore)
        self.drumObj.setSnare(snareScore)
        self.drumObj.setKick(kickScore)
        return self.drumObj

if __name__ == '__main__':
    scoreObj = cs.Score()
    scoreObj.setChordProg([[1,2], [3,4], [4,5]])
    dp = Drums()
    drum = dp.create(dp.random, scoreObj )
    print(scoreObj.drumObj.snare)
