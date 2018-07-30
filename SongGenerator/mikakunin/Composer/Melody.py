# coding: UTF-8
#default
import numpy as np

#option
from Composer import ChordSet as cs
from Composer import DiatonicSet as ds
from Composer import CommonFunction as func
from Composer import _MelodicRhythmPatterns as _rp
import random


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
        self.cherryA = "cherryA" # >2bars even
        self.cherryB = "cherryB" # >1bars ただし4回繰り返すからあまり多すぎる小節もどうかと
        self.oxgame = "oxgame" # >0bars　ただし転調しまくるコード進行に対しては多分ひどいことになる
        self.zenzenzense = "zenzenzense" # >0bars　ただし転調しまくるコード進行に対しては多分ひどいことになる
        self.romeria = "romeria"
        self.approach = "approach"
        self.breaka = "break"

    def _setMelodyNameWithoutChord(self):
        return None

    def create(self, scoreObj, melodyName,  range, **arg):
        """
        コード進行とかkey変更される場合はちゃんとscoreObjの中身変更する。
        """
        if melodyName == self.cherryA:
            melody = self._methodsObject.cherryA( scoreObj.keyProg, scoreObj.chordProg, range, arg['reverce'])
            scoreObj.setMelodyLine(melody[2])
        elif melodyName == self.cherryB:
            melody = self._methodsObject.cherryB( scoreObj.keyProg, scoreObj.chordProg, range, arg['reverce'])
            scoreObj.setKeyProg(melody[0])
            scoreObj.setChordProg(melody[1])
            scoreObj.setMelodyLine(melody[2])
        elif melodyName == self.oxgame:
            melody = self._methodsObject.oxgame( scoreObj.keyProg, scoreObj.chordProg, range)
            scoreObj.setKeyProg(melody[0])
            scoreObj.setChordProg(melody[1])
            scoreObj.setMelodyLine(melody[2])
        elif melodyName == self.zenzenzense:
            melody = self._methodsObject.zenzenzense( scoreObj.keyProg, scoreObj.chordProg, range)
            scoreObj.setKeyProg(melody[0])
            scoreObj.setChordProg(melody[1])
            scoreObj.setMelodyLine(melody[2])
        elif melodyName == self.romeria:
            melody = self._methodsObject.zenzenzense( scoreObj.keyProg, scoreObj.chordProg, range)
            scoreObj.setKeyProg(melody[0])
            scoreObj.setChordProg(melody[1])
            scoreObj.setMelodyLine(melody[2])
        elif melodyName == self.approach:
            melody = self._methodsObject.approach( scoreObj.keyProg, scoreObj.chordProg, range, arg['defaultNote'])
            scoreObj.setKeyProg(melody[0])
            scoreObj.setChordProg(melody[1])
            scoreObj.setMelodyLine(melody[2])
        elif melodyName == self.breaka :
            melody = self._methodsObject.breaka( scoreObj.keyProg, scoreObj.chordProg)
            scoreObj.setKeyProg(melody[0])
            scoreObj.setChordProg(melody[1])
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

        #SET Rhythm Patterns
        self._rhythmPattersObj = _rp.Patterns()
        self._rhythmPatters = self._rhythmPattersObj.list

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

        melody = func.processing(melody, range)
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

    def _cherryB(self, tempMelody, last_chord_beat, last_key, last_chord, last_chord_tone_degree = 0, range = [69,101], lastFractal = False):
        rythm_dict = [\
                        [0,-1,-1,1, -1,-1,2,-1], \
                        [0,-1,1,-1, -1,-1,2,-1], \
                        [0,-1,-1,-1, 1,-1,2,-1], \
                        [0,-1,1,-1, 2,-1,-1,-1], \
                        [0,-1,1,-1, 2,-1,-1,-1], \
                        [0,-1,-1,-1, 1,2,-1,-1]\
                        ]

        if self._notePerBar_n == 16:
            if len(tempMelody) < self._notePerBar_n :
                print("ALERT IN MELODY _cherryB 1 ")
            else :
                rythm = rythm_dict[np.random.randint(len(rythm_dict))]
                if lastFractal :
                    #本当は全体の調性とかちゃんと決めるべき
                    last_melody = self._threeNotesApproach([0,0], 0, 0)
                    #last_melody = self._threeNotesApproach(last_key, last_chord, last_chord_tone_degree)
                    tempMelody[last_chord_beat] = last_melody[3]

                    approach_melody = np.full(8, -1)
                    for idx, val in enumerate(rythm):
                        if val > -1 :
                            approach_melody[idx] = last_melody[val]

                    tempMelody[last_chord_beat-len(approach_melody) : last_chord_beat] =  approach_melody
                else :
                    last_melody = self._threeNotesApproach(last_key, last_chord, last_chord_tone_degree)
                    tempMelody[last_chord_beat] = last_melody[3]

                    approach_melody = np.full(8, -1)
                    for idx, val in enumerate(rythm):
                        if val > -1 :
                            approach_melody[idx] = last_melody[val]
                    tempMelody[last_chord_beat-len(approach_melody) : last_chord_beat] =  approach_melody
        else:
            print("ALERT IN MELODY 2, Not Prepared")

        melody = func.processing(tempMelody, range)

        melody = np.array(tempMelody)
        return melody

    def cherryB(self, keyProg, chordProg, range = [69,101], reverseFlg = False):
        tempMelody = np.full(len(chordProg)*self._notePerBar_n, -1)
        last_chord_beat  = 0
        for bar, chords in enumerate(chordProg):
            for beat, chord in enumerate(chords):
                #issue1
                tempMelody[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) ] = self._chordIdx.getTonesFromIdx(chord)[np.random.randint(3)]
                last_chord_beat = int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2)

        a = Methods()._cherryB(tempMelody, last_chord_beat, keyProg[-1], chordProg[-1][-1], 1, range)
        b = Methods()._cherryB(tempMelody, last_chord_beat, keyProg[-1], chordProg[-1][-1], 2, range)
        bb = Methods()._cherryB(tempMelody, last_chord_beat, keyProg[-1], chordProg[-1][-1], 0, range, True)

        melody = np.r_[a,b,a,bb]
        keyProg = np.tile(keyProg,(4,1))
        keyProg[-1] = [0,0]
        chordProg = np.tile(chordProg,(4,1))
        chordProg[-1][-1] = 0
        return  keyProg, chordProg , melody.flatten()

    def _romeria(self, key, oneBar, range, otherNoteDegree, lastNoteDegree):
        if key[1] == 0:
            scale = self._majorScale+key[0]
            scale = func.clipping(scale[0]) -scale[0] + scale
            scale = [scale[0], scale[1] , scale[2], scale[3], scale[4]-12, scale[5]-12, scale[6]-12]
            penta = [scale[0], scale[1] , scale[2], scale[4], scale[5]]

        elif key[1] == 1:
            scale = self._minorScale +key[0]
            scale = func.clipping(scale[0]) -scale[0] + scale
            scale = [scale[0], scale[1] , scale[2], scale[3], scale[4]-12, scale[5]-12, scale[6]-12]
            penta =  [scale[0], scale[2] , scale[3], scale[4], scale[6]]

        noteOnIndicies = []
        for idx, note in enumerate(oneBar):
            if note > -1:
                #全て置換
                if idx % 4 == 3 :
                    oneBar[idx] = scale[0]
                else :
                    oneBar[idx] = scale[otherNoteDegree]
                noteOnIndicies.append(idx)

        #最後の音置換
        oneBar[noteOnIndicies[-1]] = scale[lastNoteDegree]

        for i in range(2):
            if len(noteOnIndicies) > 2:
                midIndicies = np.arange(1,len(noteOnIndicies)-1)
                idx = noteOnIndicies[midIndicies[np.random.randint(len(midIndicies))]]
                oneBar[idx] =  penta[np.random.randint(len(penta))]

        return oneBar

    def _oxgame(self, key, oneBar, range, otherNoteDegree, lastNoteDegree):
        if key[1] == 0:
            scale = self._majorScale+key[0]
            scale = func.clipping(scale[0]) -scale[0] + scale
            scale = [scale[0], scale[1] , scale[2], scale[3], scale[4]-12, scale[5]-12, scale[6]-12]
            penta = [scale[0], scale[1] , scale[2], scale[4], scale[5]]

        elif key[1] == 1:
            scale = self._minorScale +key[0]
            scale = func.clipping(scale[0]) -scale[0] + scale
            scale = [scale[0], scale[1] , scale[2], scale[3], scale[4]-12, scale[5]-12, scale[6]-12]
            penta =  [scale[0], scale[2] , scale[3], scale[4], scale[6]]

        noteOnIndicies = []
        for idx, note in enumerate(oneBar):
            if note > -1:
                #全て置換
                oneBar[idx] = scale[otherNoteDegree]
                noteOnIndicies.append(idx)

        #最後の音置換
        oneBar[noteOnIndicies[-1]] = scale[lastNoteDegree]

        if len(noteOnIndicies) > 2:
            midIndicies = np.arange(1,len(noteOnIndicies)-1)
            idx = noteOnIndicies[midIndicies[np.random.randint(len(midIndicies))]]
            oneBar[idx] =  penta[np.random.randint(len(penta))]

        return oneBar

    def _zenzenzense(self, key, oneBar, range, otherNoteDegree, lastNoteDegree):
        if key[1] == 0:
            scale = self._majorScale+key[0]
            scale = func.clipping(scale[0]) -scale[0] + scale
            scale = [scale[0], scale[1] , scale[2], scale[3], scale[4], scale[5]-12, scale[6]]
            penta = [scale[0], scale[1] , scale[2], scale[4], scale[5]]

        elif key[1] == 1:
            scale = self._minorScale +key[0]
            scale = func.clipping(scale[0]) -scale[0] + scale
            scale = [scale[0], scale[1] , scale[2], scale[3], scale[4], scale[5]-12, scale[6]]
            penta =  [scale[0], scale[2] , scale[3], scale[4], scale[6]]

        noteOnIndicies = []
        for idx, note in enumerate(oneBar):
            if note > -1:
                #全て置換
                oneBar[idx] = scale[otherNoteDegree]
                noteOnIndicies.append(idx)

        #最後の音置換
        oneBar[noteOnIndicies[-1]] = scale[lastNoteDegree]

        if len(noteOnIndicies) > 2:
            midIndicies = np.arange(1,len(noteOnIndicies)-1)
            idx = noteOnIndicies[midIndicies[np.random.randint(len(midIndicies))]]
            oneBar[idx] =  penta[np.random.randint(len(penta))]

        return oneBar

    def romeria(self, keyProg=None, chordProg=None, range = [69,101]):
        grp_name, patterns = random.choice(list(self._rhythmPatters.items()))
        grp_name, patterns2 = random.choice(list(self._rhythmPatters.items()))

        """
        とりあえず
        [A, A, B, B]
        Keyをはじめの小節に固定しているので変だったら変更してみて。
        """

        if len(keyProg) >= 8:
            a = patterns[np.random.randint(len(patterns))]
            a1 = patterns2[np.random.randint(len(patterns2))]
            a.extend(a1)
            bar1 = self._romeria(keyProg[0], a, range, 1, 2)
            bar2 = bar1

            b = patterns[np.random.randint(len(patterns))]
            b1 = patterns2[np.random.randint(len(patterns2))]
            b.extend(b1)
            bar3 = self._romeria(keyProg[0], b, range, 1, 0)
            bar4 = bar3

            melody = np.array([bar1, bar2, bar3, bar4]).flatten() #the bar-arg's length is 2bars
            key = keyProg[0:8]
            chord = chordProg[0:8]


        elif len(keyProg) >= 4:
            a = patterns[np.random.randint(len(patterns))]
            a1 = patterns2[np.random.randint(len(patterns2))]
            a.extend(a1)
            bar1 = self._romeria(keyProg[0], a, range, 1, 0)
            bar2 = bar1

            melody = np.array([bar1, bar2] ).flatten()
            key = np.append(keyProg[0:4], keyProg[0:4] , axis = 0)
            chord = np.append(chordProg[0:4], chordProg[0:4], axis = 0)

        elif len(keyProg) >= 2:
            a = patterns[np.random.randint(len(patterns))]
            a1 = patterns2[np.random.randint(len(patterns2))]
            a.extend(a1)
            bar1 = self._romeria(keyProg[0], a, range, 1, 0)

            melody = np.array([bar1] ).flatten()
            key = np.append(keyProg[0:2], keyProg[0:2] , axis = 0)
            key = np.append(key, key , axis = 0)
            chord = np.append(chordProg[0:2], chordProg[0:2], axis = 0)
            chord = np.append(chord, chord, axis = 0)

        return key, chord, melody

    def oxgame(self, keyProg=None, chordProg=None, range = [69,101]):
        grp_name, patterns = random.choice(list(self._rhythmPatters.items()))

        """
        とりあえず
        [A, B, A, B,    D, E, D, F]
        Keyをはじめの小節に固定しているので変だったら変更してみて。
        """

        if len(keyProg) >= 8:
            a = patterns[np.random.randint(len(patterns))]
            bar1 = self._oxgame(keyProg[0], a, range, 0, 4)
            bar3 = bar1

            b = patterns[np.random.randint(len(patterns))]
            bar4 = self._oxgame(keyProg[0], b, range, 2, 2)
            bar2 = self._oxgame(keyProg[0], b, range, 0, 0)

            c = patterns[np.random.randint(len(patterns))]
            bar5 = self._oxgame(keyProg[0], c, range, 0, 0)
            bar7 = self._oxgame(keyProg[0], c, range, 0, 4)

            d = patterns[np.random.randint(len(patterns))]
            bar6 = self._oxgame(keyProg[0], d, range, 0, 0)

            f = patterns[np.random.randint(len(patterns))]
            bar8 = self._oxgame(keyProg[0], f, range, 0, 0)

            melody = np.array([bar1, bar2, bar3, bar4,   bar5, bar6, bar7, bar8]).flatten()
            key = keyProg[0:8]
            chord = chordProg[0:8]


        elif len(keyProg) >= 4:
            a = patterns[np.random.randint(len(patterns))]
            bar1 = self._oxgame(keyProg[0], a, range, 0, 4)
            bar3 = bar1

            b = patterns[np.random.randint(len(patterns))]
            bar2 = self._oxgame(keyProg[0], b, range, 0, 0)
            bar4 = self._oxgame(keyProg[0], b, range, 2, 2)

            melody = np.array([bar1, bar2, bar3, bar4] * 2).flatten()
            key = np.append(keyProg[0:4], keyProg[0:4] , axis = 0)
            chord = np.append(chordProg[0:4], chordProg[0:4], axis = 0)

        elif len(keyProg) >= 2:
            a = patterns[np.random.randint(len(patterns))]
            b = patterns[np.random.randint(len(patterns))]
            bar1 = self._oxgame(keyProg[0], a, range, 0, 4)
            bar2 = self._oxgame(keyProg[0], b, range, 0, 0)

            melody = np.array([bar1, bar2] * 4).flatten()
            key = np.append(keyProg[0:2], keyProg[0:2] , axis = 0)
            key = np.append(key, key , axis = 0)
            chord = np.append(chordProg[0:2], chordProg[0:2], axis = 0)
            chord = np.append(chord, chord, axis = 0)

        return key, chord, melody

    def zenzenzense(self, keyProg=None, chordProg=None, range = [69,101]):
        grp_name, patterns = random.choice(list(self._rhythmPatters.items()))

        """
        とりあえず
        [A, B, A, B,    D, E, D, F]
        Keyをはじめの小節に固定しているので変だったら変更してみて。
        """

        if len(keyProg) >= 8:
            a = patterns[np.random.randint(len(patterns))]
            bar1 = self._zenzenzense(keyProg[0], a, range, 4, 4)
            bar3 = bar1

            b = patterns[np.random.randint(len(patterns))]
            bar4 = self._zenzenzense(keyProg[0], b, range, 2, 2)
            bar2 = self._zenzenzense(keyProg[0], b, range, 4, 0)

            c = patterns[np.random.randint(len(patterns))]
            bar5 = self._zenzenzense(keyProg[0], c, range, 4, 0)
            bar7 = self._zenzenzense(keyProg[0], c, range, 4, 4)

            d = patterns[np.random.randint(len(patterns))]
            bar6 = self._zenzenzense(keyProg[0], d, range, 4, 0)

            f = patterns[np.random.randint(len(patterns))]
            bar8 = self._zenzenzense(keyProg[0], f, range, 4, 0)

            melody = np.array([bar1, bar2, bar3, bar4,   bar5, bar6, bar7, bar8]).flatten()
            key = keyProg[0:8]
            chord = chordProg[0:8]


        elif len(keyProg) >= 4:
            a = patterns[np.random.randint(len(patterns))]
            bar1 = self._zenzenzense(keyProg[0], a, range, 4, 4)
            bar3 = bar1

            b = patterns[np.random.randint(len(patterns))]
            bar2 = self._zenzenzense(keyProg[0], b, range, 4, 0)
            bar4 = self._zenzenzense(keyProg[0], b, range, 4, 2)

            melody = np.array([bar1, bar2, bar3, bar4] * 2).flatten()
            key = np.append(keyProg[0:4], keyProg[0:4] , axis = 0)
            chord = np.append(chordProg[0:4], chordProg[0:4], axis = 0)

        elif len(keyProg) >= 2:
            a = patterns[np.random.randint(len(patterns))]
            b = patterns[np.random.randint(len(patterns))]
            bar1 = self._zenzenzense(keyProg[0], a, range, 4, 4)
            bar2 = self._zenzenzense(keyProg[0], b, range, 4, 0)

            melody = np.array([bar1, bar2] * 4).flatten()
            key = np.append(keyProg[0:2], keyProg[0:2] , axis = 0)
            key = np.append(key, key , axis = 0)
            chord = np.append(chordProg[0:2], chordProg[0:2], axis = 0)
            chord = np.append(chord, chord, axis = 0)

        return key, chord, melody

    def _approach(self, tempMelody, last_key, last_chord, last_chord_tone_degree = 0, range = [69,101] ):
        on_index = np.where(tempMelody > -1)

        if self._notePerBar_n == 16:
            if len(tempMelody) < self._notePerBar_n :
                print("ALERT IN MELODY _cherryB 1 ")
            else :
                last_melody = self._threeNotesApproach(last_key, last_chord, last_chord_tone_degree)

                for idx, note in enumerate(last_melody):
                    tempMelody[on_index[idx-4]] = note

        else:
            print("ALERT IN MELODY 2, Not Prepared")

        melody = func.processing(tempMelody, range)
        melody = np.array(tempMelody)
        return melody

    def approach(self, keyProg=None, chordProg=None, _range = [69,101], otherNoteDegree = 4):
        #作りかけ
        #パターンのグループ抽出
        #grp_name, patterns = random.choice(list(self._rhythmPatters.items()))

        melody = np.full(len(keyProg)*self._notePerBar_n , -1)
        targetNote = None

        #if len(keyProg) >= 4 and len(keyProg) % 4 == 0:
        if len(keyProg) > 1:
            trial_n = len(keyProg)-1
            for num in range(trial_n ):

                grp_name, patterns = random.choice(list(self._rhythmPatters.items()))

                key = keyProg[num]
                chord_idx = chordProg[num][-1] #取り急ぎ
                if key[1] == 0:
                    scale = self._majorScale+key[0]
                    scale = func.clipping(scale[0]) -scale[0] + scale
                    scale = [scale[0], scale[1] , scale[2], scale[3], scale[4], scale[5]-12, scale[6]]
                    penta = [scale[0], scale[1] , scale[2], scale[4], scale[5]]

                elif key[1] == 1:
                    scale = self._minorScale +key[0]
                    scale = func.clipping(scale[0]) -scale[0] + scale
                    scale = [scale[0], scale[1] , scale[2], scale[3], scale[4], scale[5]-12, scale[6]]
                    penta =  [scale[0], scale[2] , scale[3], scale[4], scale[6]]


                tempMelody = np.array(patterns[np.random.randint(len(patterns))])

                #全て置換
                onIdxs = np.where(tempMelody > -1)[0]
                for idx in onIdxs:
                    tempMelody[idx] = scale[otherNoteDegree]

                if targetNote is None:
                    tempMelody[onIdxs[0]] = scale[otherNoteDegree]
                else:
                    tempMelody[onIdxs[0]] = targetNote

                appNotes = self._threeNotesApproach(keyProg[num+1], chordProg[num+1][0], degree = np.random.randint(3))

                targetNote = appNotes[-1]
                tempMelody[onIdxs[-3]] = appNotes[-4]
                tempMelody[onIdxs[-2]] = appNotes[-3]
                tempMelody[onIdxs[-1]] = appNotes[-2]



                melody[num*self._notePerBar_n : (num+1)*self._notePerBar_n] = tempMelody

            #本当はもっとよく変えたい
            melody[-self._notePerBar_n]  = targetNote

        melody = func.processing(melody, _range)
        melody = np.array(melody)

        return  keyProg, chordProg, melody

    def breaka(self,keyProg=None, chordProg = None):
        melody = np.full(len(keyProg) * self._notePerBar_n, -1)
        melody[0] = -2

        return  keyProg, chordProg, melody

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
                        [-1,0,-1,0], \
                        [-1,2,1,0], \
                        [1,-2,-1,0], \
                        [-2,-1,1,0], \
                        [2,1,-1,0] \
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
