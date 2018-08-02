# coding: UTF-8
#default
import numpy as np
from Composer.common import CommonSettings as cs
from Composer import DiatonicSet as ds
from Composer import CommonFunction as func

class VoiceProgression:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._methodsObject = Methods()
        self._setVoicingName()
        self._setRythmName()

    def _setVoicingName(self):
        self.powerChord = "powerChord"
        self.triad = "triad"
        self.doubleStop = "doubleStop"
        self.unisonBass = "unisonBass"
        self.breaka = "break"

    def _setRythmName(self):
        self.eightBeat = self._methodsObject.eightBeat
        self.synchroniseKick = self._methodsObject.synchroniseKick
        self.synchroniseBass = self._methodsObject.synchroniseBass

    def create(self, scoreObj, voicingName, range, **arg ):
        if voicingName == self.powerChord:
            voiceProg = self._methodsObject.powerChord(scoreObj.chordProg, scoreObj.drumObj.kick, scoreObj.bassLine, range, arg['subMethodName'])
            scoreObj.setVoiceProg(voiceProg)
        elif voicingName == self.triad:
            voiceProg = self._methodsObject.triad(scoreObj.chordProg, scoreObj.drumObj.kick, scoreObj.bassLine, range, arg['subMethodName'])
            scoreObj.setVoiceProg(voiceProg)
        elif voicingName == self.doubleStop:
            voiceProg = self._methodsObject.doubleStop(scoreObj.chordProg, scoreObj.drumObj.kick, scoreObj.bassLine, range, arg['subMethodName'])
            scoreObj.setVoiceProg(voiceProg)
        elif voicingName == self.unisonBass:
            voiceProg = self._methodsObject.unisonBass(scoreObj.chordProg, scoreObj.bassLine, range)
            scoreObj.setVoiceProg(voiceProg)
        elif voicingName == self.breaka:
            voiceProg = self._methodsObject.breaka(scoreObj.chordProg)
            scoreObj.setVoiceProg(voiceProg)

    def create2(self, scoreObj, voicingName, range, **arg ):
        if voicingName == self.powerChord:
            voiceProg = self._methodsObject.powerChord(scoreObj.chordProg, scoreObj.drumObj.kick, scoreObj.bassLine, range, arg['subMethodName'])
            scoreObj.setVoiceProg2(voiceProg)
        elif voicingName == self.triad:
            voiceProg = self._methodsObject.triad(scoreObj.chordProg, scoreObj.drumObj.kick, scoreObj.bassLine, range, arg['subMethodName'])
            scoreObj.setVoiceProg2(voiceProg)
        elif voicingName == self.doubleStop:
            voiceProg = self._methodsObject.doubleStop(scoreObj.chordProg, scoreObj.drumObj.kick, scoreObj.bassLine, range, arg['subMethodName'])
            scoreObj.setVoiceProg2(voiceProg)
        elif voicingName == self.unisonBass:
            voiceProg = self._methodsObject.unisonBass(scoreObj.chordProg, scoreObj.bassLine, range)
            scoreObj.setVoiceProg2(voiceProg)
        elif voicingName == self.breaka:
            voiceProg = self._methodsObject.breaka(scoreObj.chordProg)
            scoreObj.setVoiceProg2(voiceProg)

class Methods:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._subMethods = SubMethods(self._notePerBar_n)
        self._setSubMethodName()

        #SET CIRCLE OF FIFTH
        self._o5thObj = ds.CircleOfFifth()

        #SET CHORDS
        self._chordSet = self._o5thObj._chordSet
        self._chordIdx = self._chordSet.chordIdx

    def _setSubMethodName(self):
        self.eightBeat = "eightBeat"
        self.synchroniseKick = "synchroniseKick"
        self.synchroniseBass = "synchroniseBass"
        self.wholeNote = "wholeNote"
        self.kick = "kick"

    def powerChord(self, chordProg, kickScore, bassScore, range, subMethodName = "eightBeat"):
        chordScore = None
        if subMethodName == self.eightBeat:
            chordScore = self._subMethods.eightBeat(chordProg)
        elif subMethodName == self.synchroniseKick:
            chordScore = self._subMethods.synchroniseKick(chordProg, kickScore)
        elif subMethodName == self.synchroniseBass:
            chordScore = self._subMethods.synchroniseBass(chordProg, bassScore)
        elif subMethodName == self.wholeNote:
            chordScore = self._subMethods.wholeNote(chordProg)
        elif subMethodName == self.kick:
            chordScore = self._subMethods.kick(chordProg)
        else:
            print("ERROR IN VoiceProgression")
            return None

        score = np.full([len(chordProg)*self._notePerBar_n, 2], -1)
        for i, chord in enumerate(chordScore):
            if chord > -1:
                score[i][0] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[0], range[0], range[1])
                score[i][1] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[2], range[0], range[1])
            elif chord == -2:
                score[i][0] =-2
                score[i][1] =-2
        return score

    def triad(self, chordProg, kickScore, bassScore, range, subMethodName = "synchroniseKick"):
        chordScore = None

        if subMethodName == self.synchroniseKick:
            chordScore = self._subMethods.synchroniseKick(chordProg, kickScore)
        elif subMethodName == self.synchroniseBass:
            chordScore = self._subMethods.synchroniseBass(chordProg, bassScore)
        elif subMethodName == self.wholeNote:
            chordScore = self._subMethods.wholeNote(chordProg)
        elif subMethodName == self.kick:
            chordScore = self._subMethods.kick(chordProg)
        else:
            print("ERROR IN VoiceProgression")
            return None

        score = np.full([len(chordProg)*self._notePerBar_n, 3], -1)
        for i, chord in enumerate(chordScore):
            if chord > -1:
                score[i][0] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[0], range[0], range[1])
                score[i][1] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[1], range[0], range[1])
                score[i][2] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[2], range[0], range[1])
            elif chord == -2:
                score[i][0] =-2
                score[i][1] =-2
        return score

    def doubleStop(self, chordProg, kickScore, bassScore, range, subMethodName =  "synchroniseBass"):
        chordScore = None

        if subMethodName == self.synchroniseKick:
            chordScore = self._subMethods.synchroniseKick(chordProg, kickScore)
        elif subMethodName == self.synchroniseBass:
            chordScore = self._subMethods.synchroniseBass(chordProg, bassScore)
        elif subMethodName == self.wholeNote:
            chordScore = self._subMethods.wholeNote(chordProg)
        elif subMethodName == self.kick:
            chordScore = self._subMethods.kick(chordProg)
        else:
            print("ERROR IN VoiceProgression")
            return None

        score = np.full([len(chordProg)*self._notePerBar_n, 2], -1)
        for i, chord in enumerate(chordScore):
            if chord > -1:
                score[i][0] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[1], range[0], range[1])
                score[i][1] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[3], range[0], range[1])
            elif chord == -2:
                score[i][0] =-2
                score[i][1] =-2
        return score

    def unisonBass(self, chordProg, bassScore, range ):
        chordScore = None
        chordScore = self._subMethods.synchroniseBass(chordProg, bassScore)

        score = np.full([len(chordProg)*self._notePerBar_n, 3], -1)
        for i, chord in enumerate(chordScore):
            if chord > -1:
                score[i][0] = func.clipping(bassScore[i], range[0], range[1])
                score[i][1] = func.clipping(self._chordIdx.getTonesFromIdx(chord)[2], range[0], range[1])
                score[i][2] = func.clipping(bassScore[i], range[0], range[1]) + 12
        return score

    def breaka(self, chordProg):
        score = np.full([len(chordProg)*self._notePerBar_n, 2], -1)
        score[0][0] = -2
        score[0][1] = -2

        return score

class SubMethods:
    def __init__(self,  notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n

    def eightBeat(self, chordProg):
        chordScore = np.full(len(chordProg)*self._notePerBar_n ,-1)
        for bar, chords in enumerate(chordProg):
            for beat, chord in enumerate(chords):
                #issue1
                chordScore[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) : int((bar+1)*self._notePerBar_n)] \
                = np.full( int(self._notePerBar_n/(beat+1)) , chord)

        return  chordScore

    def synchroniseKick(self, chordProg, kickScore):
        chordScore = self.eightBeat(chordProg)
        for beat, note in enumerate(kickScore):
            if note < 0:
                chordScore[beat] = -1

        return  chordScore

    def synchroniseBass(self, chordProg, bassScore):
        chordScore = self.eightBeat(chordProg)
        for beat, note in enumerate(bassScore):
            if note < 0:
                chordScore[beat] = -1

        return  chordScore

    def wholeNote(self, chordProg):
        chordScore = np.full(len(chordProg)*self._notePerBar_n ,-1)
        for bar, chords in enumerate(chordProg):
            for beat, chord in enumerate(chords):
                #issue1
                chordScore[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) ] \
                = chord

        return  chordScore

    def kick(self, chordProg):
        patterns = [
            [0,-1,-1,-1, -2,-1,-1,-1, -2,-1,-1,-1, -1,-1,-1,-1 ]
            ,[0,-1,-1,-1, -1,-1,0,-1, -2,-1,-1,-1, -1,-1,-1,-1 ]
            ,[0,-1,-1,-1, -1,-1,0,-1, -1,-1,-1,-1, -1,-1,-1,-1 ]
            ,[0,-1,0,-1, -2,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1 ]
            ,[0,-1,0,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1 ]
            ,[0,0,0,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1 ]
        ]

        silent = [-2,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1]

        pattern = patterns[np.random.randint(0, len(patterns), 1)[0]]
        pattern.extend(silent)
        pattern = np.array(pattern)

        if len(chordProg) % 2 == 0 and len(chordProg) >= 2 :
            chordScore = np.tile(pattern, int(len(chordProg)/2) )

            for bar, chords in enumerate(chordProg):
                for beat, chord in enumerate(chords):
                    #issue1
                    if chordScore[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) ] > -1:
                        chordScore[int(bar*self._notePerBar_n + beat*self._notePerBar_n/4*2) ] = chord

        return  chordScore





if __name__ == '__main__':
    import Drums as dr
    import Bass as ba

    scoreObj = cs.Score()
    scoreObj.setChordProg([[1,2], [33,34], [54,55], [84,85]])
    drumObj = dr.Drums()
    drumObj.create(drumObj.random, scoreObj )
    bassObj =ba.Bass()
    bassObj.create(bassObj.synchroniseKick, scoreObj, [24,48])
    voiceObj = VoiceProgression()
    voiceObj.create(voiceObj.triad, "synchroniseKick", scoreObj , [24,48]) #self, voicingName, subMethodName, scoreObj, range

###
    #methodObj = Methods()
    #voiceProg = methodObj.powerChord(scoreObj.chordProg, scoreObj.drumObj.kick, scoreObj.bassLine, "eightBeat", [30,80])
    print(scoreObj.voiceProg)
