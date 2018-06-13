# coding: UTF-8
#default
import numpy as np

#option
from Composer import ChordSet as cs
from collections import deque

class CircleOfFifth :
    """
    circle of fifth といいつつ完全4度なので注意。
    ただし、deque()のrotateでは+で（通常の）右まわり、-で左まわり
    """
    def __init__(self):
        """
        [major,minor]
        """
        self.circleOfFifth = deque()
        self.circleOfFifth.extend([[0,9],[5,2],[10,7],[3,0],[8,5],[1,10],[6,3],[11,8],[4,1],[9,6],[2,11],[7,4]])

        """
        chordSetはtetrad
        """
        self._chordSet = cs.Tetrad()

class MajorScale:
    """
    もう少し、コードの部分をCicleOfFifthに依存させる。
    """
    def __init__(self):
        self.scale = np.array([0,2,4,5,7,9,11])
        self.diatonicSymbol = [ ["C","M7"], ["D","m7"], ["E","m7"], ["F","M7"], ["G","7"], ["A","m7"], ["B","m7-5"]]
        self.diatonicIdx = []
        for symbol in self.diatonicSymbol:
            idx = cs.Tetrad().chordIdx.getIdxFromSymbol(symbol[0], symbol[1])
            self.diatonicIdx.append(idx)

class NaturalMinorScale:
    def __init__(self):
        self.scale = np.array([0,2,3,5,7,8,10])
        self.diatonicSymbol = [ ["C","m7"], ["D","m7-5"], ["Eb","M7"], ["F","m7"], ["G","m7"], ["Ab","M7"], ["Bb","7"]]
        self.diatonicIdx = []
        for symbol in self.diatonicSymbol:
            idx = cs.Tetrad().chordIdx.getIdxFromSymbol(symbol[0], symbol[1])
            self.diatonicIdx.append(idx)

if __name__ == '__main__':
    o5thObj = CircleOfFifth()
    o5th = o5thObj.circleOfFifth
    print(o5th[-1])
    o5th.rotate(-2)
    print(o5th)
