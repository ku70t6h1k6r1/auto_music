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
        self._setMelodyNameWithChord()

        #WITHOUT CHORD
        self._setMelodyNameWithoutChord()

    def _setCounterMelody(self):
        self.pattern1 = "pattern1"

    def create(self, scoreObj, melodyName,  range, **arg):
        if melodyName == self.pattern1 :

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
