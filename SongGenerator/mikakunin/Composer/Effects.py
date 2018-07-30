# coding:utf-8
#default
import numpy as np

from Composer.common import CommonSettings as cs
#from common import CommonSettings as cs
from Composer import CommonFunction as func
#import CommonFunction as func

class Effects:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n
        self._methodsObject = Methods(notePerBar_n = 16)
        self._setMethodName()

    def _setMethodName(self):
        self.accentRandom = "accentRandom"
        self.onBeat = "onbeat"
        self.onBeat_manual = "onBeat_manual"

    def create(self, scoreObj, methodName, **arg):
#    def accentRandom(self, melody, hihat, snare, kick , barsPerOneSection = 4, temperature = {'melody':0.0005, 'hihat':0.0005, 'snare':0.0005, 'kick':0.0005}):

        if methodName == self.accentRandom:
            """
            The N of bars must be > 2bars and Even
            """
            effectsObj = self._methodsObject.accentRandom(scoreObj.melodyLine, scoreObj.drumObj.hihat, scoreObj.drumObj.snare, scoreObj.drumObj.kick, 2, arg['temperature'], arg['tryN'])
            scoreObj.setEffectsObj(effectsObj)
        elif methodName == self.onBeat:
            effectsObj = self._methodsObject.onBeat(scoreObj.melodyLine, 4, arg['temperature'], arg['tryN'])
            scoreObj.setEffectsObj(effectsObj)
        elif methodName == self.onBeat_manual:
            effectsObj = self._methodsObject.onBeat_manual(scoreObj.keyProg)
            scoreObj.setEffectsObj(effectsObj)

class Methods:
    def __init__(self, notePerBar_n = 16):
        self._notePerBar_n = notePerBar_n

    def _pickUpAccent(self, melody, notePerBar_n = 16):
        output = np.zeros(0)
        oneBar = np.zeros(len(melody))

        for j in range(int(len(melody)/notePerBar_n)):
            for i in range(notePerBar_n):
                if melody[notePerBar_n*j + i] > -1:
                    oneBar[notePerBar_n*j + i] = oneBar[notePerBar_n*j + i]  + 1
        output = np.r_[output, func.softmax(oneBar)]
        return output

    def _pickUpSectionAccent(self, melody, notePerBar_n = 16, barsPerOneSection = 4):
        output = np.zeros(0)
        oneBar = np.zeros(notePerBar_n)

        # minimum beat length sixteen-beat and then 16
        for j in range(int(len(melody)/notePerBar_n)):
            for i in range(notePerBar_n):
                if melody[j*notePerBar_n + i] > -1:
                    oneBar[i] = oneBar[i]  + 1
            if j % barsPerOneSection == barsPerOneSection - 1:
                for k in range(barsPerOneSection):
                    output = np.r_[output, func.softmax(oneBar)] #ランダム性はコントロールできる。*3でいけないのか。
                oneBar = np.zeros(notePerBar_n)
        return output

    def _tranBinary(self, probArray, tryN = 1):
        output = np.full(len(probArray), -1)

        for i, p in enumerate(probArray):
            output[i] = func.throwSomeCoins(p,tryN) -1 #On:0 Off:-1にするため

        return output

    def _accentRandom(self, score, barsPerOneSection = 4, temperature = 0.0005, n = 2):
        merge =  self._pickUpAccent(score, self._notePerBar_n) * self._pickUpSectionAccent(score, self._notePerBar_n, barsPerOneSection)

        output = np.zeros(0)
        oneBar = np.full(self._notePerBar_n, -1)

        for j in range(int(len(merge)/self._notePerBar_n )):
            for i in range(self._notePerBar_n ):
                oneBar[i] = merge[j*self._notePerBar_n  + i]
            output = np.r_[output, func.softmax(oneBar, t = temperature)] #0.0005がちょうどよい
            oneBar = np.zeros(self._notePerBar_n )

        return self._tranBinary( output, n) #変数にしなくていいのか

    def accentRandom(self, melody, hihat, snare, kick , barsPerOneSection = 4, temperature = {'melody':0.0005, 'hihat':0.0005, 'snare':0.0005, 'kick':0.0005}, tryN = {'melody':1, 'hihat':1, 'snare':1, 'kick':1}):
        effectsObj = cs.Effects()
        effectsObj.setPt1(self._accentRandom(melody, barsPerOneSection, temperature['melody'], tryN['melody']))
        effectsObj.setPt2(self._accentRandom(hihat, barsPerOneSection, temperature['hihat'], tryN['hihat']))
        effectsObj.setPt3(self._accentRandom(snare, barsPerOneSection, temperature['snare'], tryN['snare']))
        effectsObj.setPt4(self._accentRandom(kick, barsPerOneSection, temperature['kick'], tryN['kick']))
        return effectsObj

    def onBeat(self, melody, beat = 4, temperature = {'fx1':0.0005, 'fx2':0.0005, 'fx3':0.0005, 'fx4':0.0005}, tryN = {'fx1':1, 'fx2':1, 'fx3':1, 'fx4':1}):
        effectsObj = cs.Effects()

        frame = int(beat * self._notePerBar_n / 4)
        frame_n = int(len(melody) / frame)
        score = [1,0,1,0] * frame_n
        frame_mod = [0] * ( len(melody) - len(score) )
        score.extend(frame_mod)

        effectsObj.setPt1(self._accentRandom(score, 1, temperature['fx1'], tryN['fx1']))
        effectsObj.setPt2(self._accentRandom(score, 1, temperature['fx2'], tryN['fx2']))
        effectsObj.setPt3(self._accentRandom(score, 1, temperature['fx3'], tryN['fx3']))
        effectsObj.setPt4(self._accentRandom(score, 1, temperature['fx4'], tryN['fx4']))

        return effectsObj

    def onBeat_manual(self, keyProg):

        wholeNotes = [0,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1]
        fourBeats =  [0,-1,-1,-1, 0,-1,-1,-1, 0,-1,-1,-1, 0,-1,-1,-1]
        a16Beats =  [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

        effectsObj = cs.Effects()

        score = np.tile(wholeNotes, len(keyProg))
        score[-4*self._notePerBar_n:-2*self._notePerBar_n] = np.tile(fourBeats, 2)
        score[-2*self._notePerBar_n: len(score)] = np.tile(a16Beats, 2)

        effectsObj.setPt1(score)
        effectsObj.setPt2(score)
        effectsObj.setPt3(score)
        effectsObj.setPt4(score)

        return effectsObj

if __name__ == '__main__':
    melody = [1,-1,-1,-1, 1,-1,-1,-1, 1,-1,-1,-1, 1,-1,-1,-1,
              1,-1,-1,-1, 1,-1,-1,-1, 1,-1,-1,-1, 1,-1,-1,-1]

    effects = Effects()
    prob = effects.accent(melody, barsPerOneSection = 1, temperature = 0.5)
    print(prob)
    print( metho._tranBinary(prob, 2))
