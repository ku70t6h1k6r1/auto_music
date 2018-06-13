# coding: UTF-8
#default
import numpy as np

#option
from Composer import ChordSet as cs
from Composer import DiatonicSet as ds
from Composer import CommonFunction as func
from Composer import ChordProgression as cp

class Melody:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n

        #WITH CHORD
        self._methodsObject = Methods(self._notePerBar_n)
        self._setMelodyNameWithChord()

        #WITHOUT CHORD
        #self._subMethodsObject = SubMethods(notePerBar_n = 16)
        self._setMelodyNameWithoutChord()

    def _setMelodyNameWithChord(self):
        self.cherryA = "cherryA" # >2bars only even
        self.cherryB = "cherryB" # >1bars ただし4回繰り返すからあまり多すぎる小節もどうかと

    def _setMelodyNameWithoutChord(self):
        return None

    def create(self, melodyName, scoreObj, range, arg):
        """
        コード進行とかkey変更される場合はちゃんとscoreObjの中身変更する。
        """
        if melodyName == self.cherryA:
            melody = self._methodsObject.cherryA( scoreObj.keyProg, scoreObj.chordProg, range, arg[0])
            scoreObj.setMelodyLine(melody[2])
        elif melodyName == self.cherryB:
            melody = self._methodsObject.cherryB( scoreObj.keyProg, scoreObj.chordProg, range, arg[0])
            scoreObj.setMelodyLine(melody[2])


class Methods:
    u"""
    WITH CHORD

    MIDIノート <> Hz の変換は以下参照
    https://drumimicopy.com/audio-frequency/
    """

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

    def _cherryA(self, keyProg, chordProg, range):
        """
        chordPrg's length must be two-bars
        Erorr History
        指定のkeyとコードが異なり、エラーが発生
        """
        melody = np.full(2*self._notePerBar_n ,-1)
        if len(chordProg) != 2 :
            print("ERROR IN Melody 1")
            return None

        melody[0] = self._chordIdx.getTonesFromIdx(chordProg[0][0])[np.random.randint(3)]
        melody[0] = func.clipping(melody[0], range[0], range[1])
        melody[1*self._notePerBar_n] = self._chordIdx.getTonesFromIdx(chordProg[1][0])[np.random.randint(3)]
        melody[1*self._notePerBar_n] = func.clipping(melody[1*self._notePerBar_n], range[0], range[1])

        if melody[0] < melody[1*self._notePerBar_n] :
            #issue1
            chord = chordProg[0][1] if len(chordProg[0]) == 2 else chordProg[0][0]
            root = self._chordIdx.getTonesFromIdx(chord)[np.random.randint(3)] #名前がrootなのははじめrootだけ指定してたから
            key = keyProg[0]
            if key[1] == 0:
                noteIdx = np.where((self._majorScale+key[0])%12 == root)[0]
                tempMelody = [root, \
                                self._majorScale[(noteIdx + 1)%len(self._majorScale)]+key[0], \
                                self._majorScale[(noteIdx + 2)%len(self._majorScale)]+key[0], \
                                self._majorScale[(noteIdx + 3)%len(self._majorScale)]+key[0] \
                                ]
            elif key[1] == 1:
                noteIdx = np.where((self._minorScale+key[0])%12 == root)[0]
                tempMelody = [root, \
                                self._minorScale[(noteIdx + 1)%len(self._minorScale)]+key[0], \
                                self._minorScale[(noteIdx + 2)%len(self._minorScale)]+key[0], \
                                self._minorScale[(noteIdx + 3)%len(self._minorScale)]+key[0] \
                                ]
        else : #同じときは？
            #issue1
            chord = chordProg[0][1] if len(chordProg[0]) == 2 else chordProg[0][0]
            root = self._chordIdx.getTonesFromIdx(chord)[np.random.randint(3)] #名前がrootなのははじめrootだけ指定してたから
            key = keyProg[0]
            if key[1] == 0:
                noteIdx = np.where((self._majorScale+key[0])%12 == root)[0]
                tempMelody = [root, \
                                self._majorScale[(noteIdx - 1)%len(self._majorScale)]+key[0], \
                                self._majorScale[(noteIdx - 2)%len(self._majorScale)]+key[0], \
                                self._majorScale[(noteIdx - 3)%len(self._majorScale)]+key[0] \
                                ]
            elif key[1] == 1:
                noteIdx = np.where((self._minorScale+key[0])%12 == root)[0]
                tempMelody = [root, \
                                self._minorScale[(noteIdx - 1)%len(self._minorScale)]+key[0], \
                                self._minorScale[(noteIdx - 2)%len(self._minorScale)]+key[0], \
                                self._minorScale[(noteIdx - 3)%len(self._minorScale)]+key[0] \
                                ]

        if self._notePerBar_n == 16:
            melody[int(self._notePerBar_n/2)] = tempMelody[0]
            melody[int(self._notePerBar_n/2 + self._notePerBar_n/4/2)] = tempMelody[1]
            melody[int(self._notePerBar_n/2 + self._notePerBar_n/4/2 * 2)] = tempMelody[2]
            melody[int(self._notePerBar_n/2 + self._notePerBar_n/4/2 * 3)] = tempMelody[3]
        else:
            print("ALERT IN MELODY 2, Not Prepared")

        for beat, note in enumerate(melody):
            if note > -1:
                melody[beat] = func.clipping(note, range[0], range[1])
        return melody

    def cherryA(self, keyProg, chordProg, range = [69,101], reverseFlg = False):
        melody = np.full(len(chordProg)*self._notePerBar_n, -1)
        if len(keyProg)%2 != 0 or len(chordProg)%2 != 0 :
            print("ALERT IN MELODY 3")
            return None

        if reverseFlg:
            trueChordProg = chordProg
            chordProg = np.r_[ chordProg[1:len(chordProg)], chordProg[0:1] ]
            trueKeyProg  = keyProg
            keyProg = np.r_[ keyProg[1:len(keyProg)], keyProg[0:1] ]

        bar = 0
        while bar < len(chordProg):
            tempMelody = self._cherryA(keyProg[bar:bar+2], chordProg[bar:bar+2], range)
            melody[bar*self._notePerBar_n : (bar+2)*self._notePerBar_n] = tempMelody[0 : len(tempMelody)]

            bar += 2

        if reverseFlg:
            melody = np.r_[ melody[len(melody)-1*self._notePerBar_n:len(melody)], melody[0:len(melody)-1*self._notePerBar_n ]]
            chordProg = trueChordProg
            keyProg = trueKeyProg


        return keyProg, chordProg, melody

    def _cherryB(self, tempMelody, last_chord_beat, last_key, last_chord, last_chord_tone_degree = 0, range = [69,101]):
        if self._notePerBar_n == 16:
            if len(tempMelody) < self._notePerBar_n :
                print("ALERT IN MELODY _cherryB 1 ")
            else :
                last_melody = self._threeNotesApproach(last_key, last_chord, last_chord_tone_degree)
                tempMelody[last_chord_beat] = last_melody[3]
                approach_melody = [last_melody[0],-1,-1,last_melody[1],-1,-1,last_melody[2],-1]
                tempMelody[last_chord_beat-len(approach_melody) : last_chord_beat] =  approach_melody
        else:
            print("ALERT IN MELODY 2, Not Prepared")

        for beat, note in enumerate(tempMelody):
            if note > -1:
                tempMelody[beat] = func.clipping(note, range[0], range[1])

        return tempMelody

    def cherryB(self, keyProg, chordProg, range = [69,101], reverseFlg = False):
        tempMelody = np.full(len(chordProg)*self._notePerBar_n, -1)
        last_chord_beat  = 0
        for bar, chords in enumerate(chordProg):
            for beat, chord in enumerate(chords):
                #issue1
                tempMelody[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) ] = self._chordIdx.getTonesFromIdx(chord)[np.random.randint(4)]
                last_chord_beat = int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2)

        a = self._cherryB(tempMelody, last_chord_beat, keyProg[-1], chordProg[-1][-1], 2, range)
        b = self._cherryB(tempMelody, last_chord_beat, keyProg[-1], chordProg[-1][-1], 1, range)
        bb = self._cherryB(tempMelody, last_chord_beat, keyProg[-1], chordProg[-1][-1], 0, range)

        melody = np.zeros(0)
        melody = np.r_[a, b, a, bb]

        return np.tile(keyProg,(4,1)), np.tile(chordProg,(4,1)), melody.flatten()

    #approachノート系
    def _threeNotesApproach(self, key, chord_idx, degree = np.random.randint(3)):
        u"""
        チェリーのサビ
        前前前世のサビ
        """
        aporoachNotes_dict = [\
                        [1,0,-1,0], \
                        [-1,0,1,0], \
                        [-3,-2,-1,0], \
                        [3,2,1,0], \
                        [1,0,1,0], \
                        [-1,0,-1,0] \
                        ]

        melody = []
        note = self._chordIdx.getTonesFromIdx(chord_idx)[degree]
        if key[1] == 0:
            noteIdx = np.where((self._majorScale+key[0])%12 == note)[0]
            for deg in aporoachNotes_dict[np.random.randint(len(aporoachNotes_dict))]:
                melody.append(self._majorScale[(noteIdx + deg)%len(self._majorScale)]+key[0])

        elif key[1] == 1:
            noteIdx = np.where((self._minorScale+key[0])%12 == note)[0]
            for deg in aporoachNotes_dict[np.random.randint(len(aporoachNotes_dict))]:
                melody.append(self._minorScale[(noteIdx + deg)%len(self._minorScale)]+key[0])

        else:
            print("ERROR IN Melody _threeNotesApproach :Selected key is wrong")
            return None

        return np.array(melody).flatten()

if __name__ == '__main__':
    cp = cp.ChordProgression()
    melody = Melody()

    #A
    a_Chord = cp.create(cp.cherry,  [-1, [0,1], [0,4]])
    a = melody.create(melody.cherryA, a_Chord[0], a_Chord[1], [69,101], [True])
    print(a)

    #B
    b_Chord = cp.createChild(cp.cherryB,a_Chord[0],a_Chord[1])
    b = melody.create(melody.cherryB, b_Chord[0], b_Chord[1], [69,101], [False])
    print(b)
