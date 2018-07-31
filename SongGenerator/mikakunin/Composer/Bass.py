# coding: UTF-8
#default
import numpy as np
import random

#option
from Composer import ChordSet as cs
from Composer import DiatonicSet as ds
from Composer import CommonFunction as func
from Composer import ChordProgression as cp
from Composer import _DrumsPatternSet as drptn
from Composer.common import CommonSettings as cs
from Composer import _DrumsPatternSet as drPtn
from Composer import _MelodicRhythmPatterns as _rp


class Bass:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._methodObject = Methods(self._notePerBar_n)
        self._setMethodName()

    def _setMethodName(self):
        self.eightBeat = "eightbeat"
        self.synchroniseKick = "kick"
        self.riff = "riff"
        self.riff16 = "riff16"
        self.riff8 = "riff8"
        self.pedal = "pedal"
        self.breaka = "break"

    def create(self, scoreObj, methodName, range): #melodyName, keyProg, chordProg, range, arg
        if methodName == self.eightBeat:
            bassLine = self._methodObject.eightBeat( scoreObj.chordProg, range)
            scoreObj.setBassLine(bassLine)
        elif methodName == self.synchroniseKick:
            kick = scoreObj.drumObj.kick
            bassLine = self._methodObject.synchroniseKick(scoreObj.chordProg, kick, range)
            scoreObj.setBassLine(bassLine)
        elif methodName == self.riff:
            bassLine = self._methodObject.riff(scoreObj.chordProg, range)
            scoreObj.setBassLine(bassLine)
        elif methodName == self.riff16:
            bassLine = self._methodObject.riff16(scoreObj.chordProg, range)
            scoreObj.setBassLine(bassLine)
        elif methodName == self.riff8:
            bassLine = self._methodObject.riff8(scoreObj.chordProg, range)
            scoreObj.setBassLine(bassLine)
        elif methodName == self.pedal:
            bassLine = self._methodObject.pedal(scoreObj.keyProg, range)
            scoreObj.setBassLine(bassLine)
        elif methodName == self.breaka:
            bassLine = self._methodObject.breaka(scoreObj.chordProg)
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

        #SET SCALE
        self._majorScaleObj = ds.MajorScale()
        self._minorScaleObj = ds.NaturalMinorScale()
        self._majorScale = self._majorScaleObj.scale
        self._minorScale = self._minorScaleObj.scale

        #SET Rhythm Patterns
        self._rhythmPattersObj = _rp.Patterns()
        self._rhythmPatters = self._rhythmPattersObj.list

    def eightBeat(self, chordProg, range, chordTone = 0):
        bassLine = np.full(len(chordProg)*self._notePerBar_n ,-1)
        for bar, chords in enumerate(chordProg):
            for beat, chord in enumerate(chords):
                #issue1
                #bassLine[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) : int((bar+1)*self._notePerBar_n)] \
                #= np.full( int(self._notePerBar_n/(beat+1) ) , self._chordIdx.getTonesFromIdx(chord)[0])
                bassLine[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) : int((bar+1)*self._notePerBar_n)] = [self._chordIdx.getTonesFromIdx(chord)[chordTone],-1] * int(8 / (beat + 1))

        for beat, note in enumerate(bassLine):
            if note > -1:
                bassLine[beat] = func.clipping(note, range[0], range[1])

        return  bassLine

    def synchroniseKick(self, chordProg, kickScore, range, chordTone = 0):
        bassLine = self.eightBeat(chordProg, range, chordTone)
        for beat, note in enumerate(kickScore):
            if note < 0:
                bassLine[beat] = -1

        return  bassLine

    def riff(self, chordProg, range):
        """
        一旦minorで考える
        """
        pattrensObj = drPtn.Patterns()
        patterns = pattrensObj.list
        idx = np.random.randint(0, len(patterns), 1)[0]
        kickScore = np.tile(patterns[idx].kick, len(chordProg))
        snareScore = np.tile(patterns[idx].snare, len(chordProg))
        bass_kick = self.synchroniseKick(chordProg, kickScore, range)
        bass_snare = self.synchroniseKick(chordProg, snareScore, range, np.random.randint(0, 4, 1)[0])

        for idx, note in enumerate(bass_kick):
            if note == -1:
                bass_kick[idx] = bass_snare[idx]

        bassLine = bass_kick

        return bassLine

    def riff16(self, chordProg, range):
        """
        一旦minorで考える
        """

        grp_name, patterns = random.choice(list(self._rhythmPatters.items()))
        grp_name, patterns2 = random.choice(list(self._rhythmPatters.items()))

        a = patterns[np.random.randint(len(patterns))]
        a1 = patterns2[np.random.randint(len(patterns2))]
        a.extend(a1)

        a = np.array(a[0::2] )

        for idx, note in enumerate(a):
            if note > -1:
                break
            else:
                a[idx] = -2

        bassLine = []
        a_on = np.where(a > -1)[0]
        for chord in chordProg:
            for idx in a_on:
                a[idx] = self._chordIdx.getTonesFromIdx(chord[0])[np.random.randint(0, 4, 1)[0]]

            bassLine.extend(a)

        for beat, note in enumerate(bassLine):
            if note > -1:
                bassLine[beat] = func.clipping(note, range[0], range[1])

        return bassLine

    def riff8(self, chordProg, range):
        """
        一旦minorで考える
        """

        grp_name, patterns = random.choice(list(self._rhythmPatters.items()))
        a =np.array( patterns[np.random.randint(len(patterns))] )

        for idx, note in enumerate(a):
            if note > -1:
                break
            else:
                a[idx] = -2

        bassLine = []
        a_on = np.where(a > -1)[0]
        for chord in chordProg:
            for idx in a_on:
                a[idx] = self._chordIdx.getTonesFromIdx(chord[0])[np.random.randint(0, 4, 1)[0]]

            bassLine.extend(a)

        for beat, note in enumerate(bassLine):
            if note > -1:
                bassLine[beat] = func.clipping(note, range[0], range[1])

        return bassLine


    def pedal(self, keyProg, range):
        patterns = [
            [0,0,0,-1, 0,0,-1,0, 0,0,0,-1, 0,0,-1,0,]
        ]

        pattern = np.array(patterns[np.random.randint(0, len(patterns), 1)[0]])

        key = keyProg[0]
        if key[1] == 0:
            scale = self._majorScale+key[0]
        elif key[1] == 1:
            scale = self._minorScale +key[0]

        bassLine = np.full(len(pattern) ,-1)
        onSets = np.where(pattern > -1)[0]

        for idx in onSets:
            bassLine[idx] = func.clipping(scale[4], range[0], range[1])

        bassLine = np.tile(bassLine, len(keyProg))

        return  bassLine

    def breaka(self, chordProg = None):
        bassLine = np.full(len(chordProg) * self._notePerBar_n, -1)
        bassLine[0] = -2

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
