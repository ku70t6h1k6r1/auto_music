# coding: UTF-8
#default
import numpy as np

#option
from Composer import ChordSet as cs
from Composer import DiatonicSet as ds
from Composer import CommonFunction as func
from Composer import _MelodicRhythmPatterns as _rp
import random

class CounterMelody:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n

        #WITH CHORD
        self._methodsObject = Methods(self._notePerBar_n)
        self._setCounterMelody()

        #WITHOUT CHORD
        #self._setMelodyNameWithoutChord()

    def _setCounterMelody(self):
        self.arp = "arp"
        self.breaka = "break"
        self.unison = "unison"

    def create(self, scoreObj, melodyName,  range, **arg):
        if melodyName == self.arp :
            melody = self._methodsObject.counter( scoreObj.keyProg, scoreObj.chordProg, range)
            scoreObj.setMelodyLine2(melody)

        elif melodyName == self.breaka :
            melody = self._methodsObject.breaka( scoreObj.keyProg, scoreObj.chordProg)
            scoreObj.setMelodyLine2(melody)

        elif melodyName == self.unison :
            melody = self._methodsObject.unison(scoreObj.melodyLine)
            scoreObj.setMelodyLine2(melody)

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
        self._majorDiatonicChords = self._majorScaleObj.diatonicIdx
        self._minorDiatonicChords = self._minorScaleObj.diatonicIdx

        #SET Rhythm Patterns
        self._rhythmPattersObj = _rp.Patterns()
        self._rhythmPatters = self._rhythmPattersObj.list

    def breaka(self,keyProg=None, chordProg = None):
        #print("break",len(chordProg), chordProg )
        melody = np.full(len(keyProg) * self._notePerBar_n, -1)
        melody[0] = -2

        #print(len(melody))
        return  melody

    def unison(self, melody):
        return melody

    def counter(self, keyProg=None, chordProg=None, _range = [69,101]):
        #print("counter",len(chordProg), chordProg )
        melody = []
        for chord in chordProg:
            grp_name, patterns = random.choice(list(self._rhythmPatters.items()))
            grp_name2, patterns2 = random.choice(list(self._rhythmPatters.items()))

            a = patterns[np.random.randint(len(patterns))]
            a1 = patterns2[np.random.randint(len(patterns2))]

            tempMelody = np.r_[np.array(a), np.array(a1)]


            tempMelody = np.array(tempMelody[0::2] )

            tempMelody_on = np.where(tempMelody > -1)[0]

            for idx in tempMelody_on:
                tempMelody[idx] = self._chordIdx.getTonesFromIdx(chord[0])[np.random.randint(0, 4, 1)[0]]

            melody.extend(tempMelody)

        melody = func.processing(melody, _range)
        melody = np.array(melody)

        return  melody
