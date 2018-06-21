# coding: UTF-8
#default
import numpy as np

#option
from Composer import ChordSet as cs
from Composer import DiatonicSet as ds

class ChordProgression:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n

        #PARENT
        self._methodsObject = Methods()
        self._setChangeName()

        #CHILD
        self._subMethodsObject = SubMethods()
        self._setChildChangeName()

    def _setChangeName(self):
        self.cherry = "cherry" # >0bars
        self.punk = "punk" # >0bars

    def _setChildChangeName(self):
        self.cherryIntro = "cherryIntro" # >4bars
        self.cherryB = "cherryB" # >6bars
        self.none = "none"

    def create(self, scoreObj, changeName, **arg): #arg = [-1, [0,1], [0,4]]):
        if changeName == self.cherry:
            chords = self._methodsObject.cherryChanges(arg['rotate'],arg['keyMm'],arg['chordDeg'])
            harmony = np.full(len(chords[1]) * self._notePerBar_n, -1)
            for bar, chord in enumerate(chords[1]):
                for beat, idx in enumerate(chord):
                    #issue1
                    harmony[bar*self._notePerBar_n + int(beat*self._notePerBar_n/2) ] =  idx

            scoreObj.setKeyProg(chords[0])
            scoreObj.setChordProg(chords[1])

        elif changeName == self.punk:
            chords = self._methodsObject.punkRockChanges(arg['is_Maj'], arg['chord_per_1bar'])
            scoreObj.setKeyProg(chords[0])
            scoreObj.setChordProg(chords[1])
            #def punkRockChanges(self, is_Maj = True , chord_per_1bar = 1):

    def update(self, scoreObj, changeName): #, keyProgression, chordProgression):
        if changeName  == self.cherryIntro:
            chords = self._subMethodsObject.cherryIntro(scoreObj.keyProg, scoreObj.chordProg)
            harmony = np.full(len(chords[1]) * self._notePerBar_n, -1)
            for bar, chord in enumerate(chords[1]):
                for beat, idx in enumerate(chord):
                    #issue1
                    harmony[bar*self._notePerBar_n + int(beat*self._notePerBar_n/2) ] =  idx
            scoreObj.setKeyProg(chords[0])
            scoreObj.setChordProg(chords[1])
            #return chords[0], chords[1], harmony #key, chord, chord with Rythm

        elif changeName  == self.cherryB:
            chords = self._subMethodsObject.cherryB(scoreObj.keyProg, scoreObj.chordProg)
            harmony = np.full(len(chords[1]) * self._notePerBar_n, -1)
            for bar, chord in enumerate(chords[1]):
                for beat, idx in enumerate(chord):
                    #issue1
                    harmony[bar*self._notePerBar_n + int(beat*self._notePerBar_n/2) ] =  idx
            scoreObj.setKeyProg(chords[0])
            scoreObj.setChordProg(chords[1])
            #return chords[0], chords[1], harmony #key, chord, chord with Rythm

        else:
            scoreObj


class Methods:
    """
    returnは以下のフォーマット
    [[C,G],[C],[C,F],[G,F,C,G]]
    -> / C,C,G,G / C,C,C,C / C,C,F,F / G,F,C,G
       ただし　2コード/小節　より多いのは作らない。
    最低でも8bars 作る
    """
    def __init__(self):

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
        self._majorDiatonicChords = self._majorScaleObj.diatonicIdx
        self._minorDiatonicChords = self._minorScaleObj.diatonicIdx

    def cherryChanges(self, rotate = -6, majorMinor = [0,1], chordProgress = [0,4]):
        """
        -majorMino
         [0,1] : major>minor
         [1,0] : minor>major
         [0] : major
         [1] : minor

        -ChordProgress
         length is 2.
        """
        keys = []
        for i in range(int(4 / len(majorMinor))):
            keys.append(self._o5th[0])
            self._o5th.rotate(rotate)
        self._o5th = self._o5thObj.circleOfFifth

        keysForReturn = []
        chords = []
        for key in keys:
            for mM in majorMinor:
                if mM == 0 :
                        for degree in chordProgress:
                            idx = (self._majorDiatonicChords[degree] + key[0]*len(self._chordSymbols)) % (len(self._chordSymbols)*len(self._rootSymbols))
                            chords.append([idx])
                            keysForReturn.append([key[0],0])
                elif mM == 1:
                        for degree in chordProgress:
                            idx = (self._minorDiatonicChords[degree] + key[1]*len(self._chordSymbols)) % (len(self._chordSymbols)*len(self._rootSymbols))
                            chords.append([idx])
                            keysForReturn.append([key[1],1])
                else:
                        print("ERROR IN ChordProgression 1")

        chords[-1] = [self._majorDiatonicChords[4]]
        keysForReturn[-1] = [0,0]
        chords = np.array(chords) #np.tile(np.array(chords) ,(2,1))
        keysForReturn = np.array(keysForReturn) #np.tile(np.array(keysForReturn) ,(2,1))

        return keysForReturn,chords

    def punkRockChanges(self, is_Maj = True , chord_per_1bar = 1):
        """
        chord_per_: 1bar 1 or 2
        return : 16bars or 8bars
        """
        if chord_per_1bar  == 1:
            bars = 16
        elif chord_per_1bar  == 2:
            bars =  8

        prog_dict = [\
                        [0, 3, 4, 0], \
                        [0, 0, 3, 4], \
                        [3, 4, 0, 0], \
                        [3, 4, 0, 4], \
                        [3, 4, 0, 3], \
                        [0, 4, 3, 0], \
                        [0, 4, 3, 4], \
                        [4, 0, 3, 4], \
                        [4, 0, 4, 3] \
                        ]


        if is_Maj:
            keyProg = [[0,0]] * bars
            chordProg = self._fourChordToBeats(prog_dict[np.random.randint(len(prog_dict))], chord_per_1bar)
            for i, chords in enumerate(chordProg):
                for j, chord in enumerate(chords):
                    chordProg[i][j] = self._majorDiatonicChords[chord]
        else:
            keyProg = [[0,1]] * bars
            chordProg = self._fourChordToBeats(prog_dict[np.random.randint(len(prog_dict))], chord_per_1bar)
            for i, chords in enumerate(chordProg):
                for j, chord in enumerate(chords):
                    chordProg[i][j] = self._minorDiatonicChords[chord]

        return np.array(keyProg), np.array(chordProg*int(bars/len(chordProg)))

    def _fourChordToBeats(self, prog, chord_per_1bar):
        if chord_per_1bar  == 1:
            return [[prog[0]], [prog[1]], [prog[2]], [prog[3]]]

        elif chord_per_1bar  == 2:
            return [[prog[0], prog[1]], [prog[2], prog[3]]]

class SubMethods:
    def cherryIntro(self, keyProgression, chordProgression):
        """
        INTROで使われているメソッド
        """
        if len(chordProgression) < 4 :
            print("ERROR IN ChordProgression 2")
            return None
        else:
            keysForReturn = []
            tempChords = []
            for chord in chordProgression:
                tempChords.append(chord [0])

            tempChords = np.array(tempChords)
            chords = [[tempChords[0],tempChords[1]],[tempChords[2],tempChords[3]]]
            chords = np.array(chords)#np.tile(np.array(chords), (4,1))

            keysForReturn = [keyProgression[0], keyProgression[1]]
            keysForReturn = np.array(keysForReturn) #np.tile(np.array(keysForReturn), (4,1))

            return keysForReturn, chords

    def cherryB(self, keyProgression, chordProgression):
        """
        サビで使われているメソッド
        """
        if len(chordProgression) < 6 :
            print("ERROR IN ChordProgression 3")
            return None
        else:
            keysForReturn = []
            tempChords = []
            for chord in chordProgression:
                tempChords.append(chord [0])

            tempChords = np.array(tempChords)
            chords = [[tempChords[2],tempChords[3]],[tempChords[4],tempChords[5]]]
            chords = np.array(chords) #np.tile(np.array(chords), (4,1))

            keysForReturn = [keyProgression[2], keyProgression[4]]
            keysForReturn = np.array(keysForReturn) #np.tile(np.array(keysForReturn), (4,1))

            return keysForReturn, chords

if __name__ == '__main__':
    cp = ChordProgression()
    a = cp.create(cp.cherry,  [-1, [0,1], [0,4]])
    #print(a[2])
    intro = cp.createChild(cp.cherryB,a[0],a[1])
    print(intro[2])

    #print(a[1])
    #print(a[0])
    #alg = Methods()
    #for chord in a[0]:
    #    print(alg._chordIdx.getSymbolFromIdx(chord[0]))

    """
    subAlg = SubMethods()
    intro = subAlg._cherryB(chords)
    print(intro)
    for chord in intro:
        print("###")
        print(alg._chordIdx.getSymbolFromIdx(chord[0]))
        print(alg._chordIdx.getSymbolFromIdx(chord[1]))
        print("###")
    """
