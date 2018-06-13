# coding: UTF-8
#default
import numpy as np

#option
from Composer import ChordSet as cs
from Composer import DiatonicSet as ds
from Composer import CommonFunction as func
from Composer import ChordProgression as cp
from Composer import _DrumsPatternSet as drptn
from Composer.common import CommonSettings as cs

class Bass:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._methodObject = Methods(self._notePerBar_n)
        self._setMethodName()

    def _setMethodName(self):
        self.eightBeat = "eightbeat"
        self.synchroniseKick = "kick"

    def create(self, methodName, scoreObj, range): #melodyName, keyProg, chordProg, range, arg
        if methodName == self.eightBeat:
            bassLine = self._methodObject.eightBeat( scoreObj.chordProg, range)
            scoreObj.setBassLine(bassLine)
        elif methodName == self.synchroniseKick:
            kick = scoreObj.drumObj.kick
            bassLine = self._methodObject.synchroniseKick(scoreObj.chordProg, kick, range)
            scoreObj.setBassLine(bassLine)

class Methods:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n

        #SET CIRCLE OF FIFTH
        self._o5thObj = ds.CircleOfFifth()
        self._o5th = self._o5thObj.circleOfFifth

        #SET CHORDS
        self._chordSet = self._o5thObj._chordSet
        self._chordIdx = self._chordSet.chordIdx
        self._rootSymbols = self._chordSet.rootSymbols
        self._chordSymbols = self._chordSet.chordSymbols

    def eightBeat(self, chordProg, range):
        bassLine = np.full(len(chordProg)*self._notePerBar_n ,-1)
        for bar, chords in enumerate(chordProg):
            for beat, chord in enumerate(chords):
                #issue1
                bassLine[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) : int((bar+1)*self._notePerBar_n)] \
                = np.full( int(self._notePerBar_n/(beat+1) ) , self._chordIdx.getTonesFromIdx(chord)[0])

        for beat, note in enumerate(bassLine):
            if note > -1:
                bassLine[beat] = func.clipping(note, range[0], range[1])

        return  bassLine

    def synchroniseKick(self, chordProg, kickScore, range):
        bassLine = self.eightBeat(chordProg, range)
        for beat, note in enumerate(kickScore):
            if note < 0:
                bassLine[beat] = -1

        return  bassLine

if __name__ == '__main__':
    import Drums as dr

    scoreObj = cs.Score()
    scoreObj.setChordProg([[1,2], [33,34], [54,55]])
    drumObj = dr.Drums()
    drumObj.create(drumObj.random, scoreObj )
    bassObj = Bass()
    bassObj.create(bassObj.synchroniseKick, scoreObj, [24,48])
    print(scoreObj .bassLine)
