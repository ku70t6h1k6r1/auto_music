# coding: UTF-8
#default
import numpy as np

#option
import math

class Func:
    def setTones(self, chords_dic):
        tones = {}
        for i in range(12 * len(chords_dic)):
            tones[i] = np.array(chords_dic[i % len(chords_dic)]) + int(i / len(chords_dic))
            for j in range(len(tones[i])):
                tones[i][j] = self.clip1oct(tones[i][j])
        return tones

    def clip1oct(self, note):
        if note > 11:
            return note - 12
        else:
            return note

    def convertIndexToSymbol(self, idx, rootSymbol, chordSymbol):
        root = rootSymbol[math.floor(idx / len(chordSymbol))]
        symbol = chordSymbol[idx % len(chordSymbol)]
        return root+symbol

class Set:
    def __init__(self, chords_dict, rootSymbols, chordSymbols):
        self.func = Func()
        self._chords_dict = chords_dict
        self._rootSymbols = rootSymbols
        self._chordSymbols = chordSymbols
        self._tones = self.func.setTones(self._chords_dict)

    def getSymbolFromIdx(self, idx):
        return self.func.convertIndexToSymbol(idx, self._rootSymbols, self._chordSymbols)

    def getTonesFromIdx(self, idx):
        return self._tones[idx]

    def getIdxFromSymbol(self, rootSymbol, chordSymbol):
        rootIndex = np.where(self._rootSymbols == rootSymbol)[0]
        chordIndex = np.where(self._chordSymbols == chordSymbol)[0]
        return int(rootIndex * len(self._chordSymbols) +  chordIndex)

    def getIdxFromTones(self, tones):
        return none

    def getSymbolFromTones(self, tones):
        idx = self.getIdxFromTones(self, tones)
        return getSymbolFromIdx(idx)

"""
コードセットを下に追記していく。
"""

class Triad:
    def __init__(self):
        """
        0:I
        1:Im
        2:I2
        3:I4
        4:Iaug
        5:Idim
        """

        self.chords_dic = {\
            0:[0, 4, 7], \
            1:[0, 3, 7], \
            2:[0, 2, 7], \
            3:[0, 5, 7], \
            4:[0, 4, 8], \
            5:[0, 3, 6] \
            }

        self.rootSymbols = np.array(["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"])
        self.chordSymbols = np.array([" ","m","sus2","sus4","aug","dim"])
        self.chordIdx = Set(self.chords_dic, self.rootSymbols, self.chordSymbols)

class Tetrad:
    def __init__(self) :

        """
        #DEFAULTとしてもっていたい。
        0:IM7
        1:I7
        2:Im7
        3:ImM7
        4:IM7+5
        5:I7+5
        6:Im7-5
        7:Idim7
        """
        self.chords_dic = {\
            0:[0, 4, 7, 11], \
            1:[0, 4, 7, 10], \
            2:[0, 3, 7, 10], \
            3:[0, 3, 7, 11], \
            4:[0, 4, 8, 11], \
            5:[0, 4, 8, 10], \
            6:[0, 3, 6, 10], \
            7:[0, 3, 6, 9] \
            }

        self.rootSymbols = np.array(["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"])
        self.chordSymbols = np.array(["M7","7","m7","mM7","M7+5","7+5","m7-5","dim7"])
        self.chordIdx = Set(self.chords_dic, self.rootSymbols, self.chordSymbols)

if __name__ == '__main__':
    tetrad = Tetrad().chordIdx
    print(tetrad.getSymbolFromIdx(49))
    print(tetrad.getTonesFromIdx(49))
    print(tetrad.getIdxFromSymbol("Gb","7"))
