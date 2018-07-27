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
        self.eightbeat = "eightbeat"
        self.snareroll = "snareroll"
        self.fourBeat = "fourbeat"

    def create(self, scoreObj, methodName):
        if methodName == self.random:
            drumObj = self._methodsObject.randomChoise(scoreObj.chordProg)
            scoreObj.setDrumObj(drumObj)
        elif methodName == self.eightbeat:
            drumObj = self._methodsObject.eightBeat(scoreObj.chordProg)
            scoreObj.setDrumObj(drumObj)
        elif methodName == self.snareroll:
            drumObj = self._methodsObject.snareRoll(scoreObj.chordProg)
            scoreObj.setDrumObj(drumObj)
        elif methodName == self.fourBeat:
            drumObj = self._methodsObject.fourBeat(scoreObj.chordProg)
            scoreObj.setDrumObj(drumObj)


class Methods:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._pattrensObj = drPtn.Patterns()
        self._patterns = self._pattrensObj.list
        self._FillsObj = drPtn.Fills()
        self._fills = self._FillsObj.list

    def randomChoise(self, chordProg):
        drumObj = cs.Drums()

        idx = np.random.randint(0, len(self._patterns), 1)[0]
        hihatScore = np.tile(self._patterns[idx].hihat, len(chordProg))
        snareScore = np.tile(self._patterns[idx].snare, len(chordProg))
        kickScore = np.tile(self._patterns[idx].kick, len(chordProg))

        drumObj.setHihat(hihatScore)
        drumObj.setSnare(snareScore)
        drumObj.setKick(kickScore)
        return drumObj

    def eightBeat(self, chordProg):
        drumObj = cs.Drums()

        idx = np.random.randint(0, 3, 1)[0]
        hihatScore = np.tile(self._patterns[idx].hihat, len(chordProg))
        snareScore = np.tile(self._patterns[idx].snare, len(chordProg))
        kickScore = np.tile(self._patterns[idx].kick, len(chordProg))

        drumObj.setHihat(hihatScore)
        drumObj.setSnare(snareScore)
        drumObj.setKick(kickScore)
        return drumObj

    def snareRoll(self, chordProg):
        """
        実質的には self._notePerBar_n = 16　が前提になっている。
        """

        drumObj = cs.Drums()

        silent_length = len(chordProg) * self._notePerBar_n
        silent = np.full(silent_length, -2)
        snare = np.tile(self._fills[0].snare, len(chordProg))

        snare[-4*self._notePerBar_n:-2*self._notePerBar_n] = np.tile(self._fills[1].snare, 2)
        snare[-2*self._notePerBar_n: len(snare)] = np.tile(self._fills[2].snare, 2)

        drumObj.setHihat(silent)
        drumObj.setSnare(snare)
        drumObj.setKick(silent)
        return drumObj

    def fourBeat(self,chordProg):
        drumObj = cs.Drums()

        idx = -1#8
        hihatScore = np.tile(self._patterns[idx].hihat, len(chordProg))
        snareScore = np.tile(self._patterns[idx].snare, len(chordProg))
        kickScore = np.tile(self._patterns[idx].kick, len(chordProg))

        drumObj.setHihat(hihatScore)
        drumObj.setSnare(snareScore)
        drumObj.setKick(kickScore)
        return drumObj

if __name__ == '__main__':
    scoreObj = cs.Score()
    scoreObj.setChordProg([[1,2], [3,4], [4,5]])
    dp = Drums()
    drum = dp.create(dp.random, scoreObj )
    print(scoreObj.drumObj.snare)
