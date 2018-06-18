# coding:utf-8
import numpy as np
from Composer import Score as sc
from AnalogSynthesizer import AnalogSynthesizer as aSynthe
from common import function as func
import pyaudio
import wave as wv

class Play:
    def __init__(self):
        self.scoreObj = sc.Score()
        self.audio  = pyaudio.PyAudio()
        self.o = self.audio.open(format=self.audio.get_format_from_width(2),channels=1,rate=44100,output=True)

    def setScore(self):
        self.score = self.scoreObj.load()

    def setBpm(self, bpm):
        self.bassObj = midiNotesToWave('bass',bpm = bpm)
        self.kickObj = midiNotesToWave('kick',bpm = bpm)
        self.hihatObj = midiNotesToWave('hihat',bpm = bpm)
        self.snareObj = midiNotesToWave('snare',bpm = bpm)

    def execute(self, writeStream = True, fileOut = False):
        melody = self.bassObj.convert(self.score.melodyLine)
        bass =  self.bassObj.convert(self.score.bassLine)
        voicing =  self.bassObj.convertPoly(self.score.voiceProg)
        kick = self.kickObj.convertPerc(self.score.drumObj.kick, 100)
        snare =  self.snareObj.convertPerc(self.score.drumObj.snare, 150)
        hihat =  self.hihatObj.convertPerc(self.score.drumObj.hihat, 100)

        wave = func.add([melody, bass, kick, snare, hihat, voicing], [1.0, 0.8, 1.5, 1, 0.7, 1])
        wave_bin = func.toBytes(wave)
        self.o.write(wave_bin)


class midiNotesToWave:
    def __init__(self, instName, notePerBar_n = 16, bpm = 120):
        self._notePerBar_n = notePerBar_n
        self._bpm = bpm
        self._noteMinLen_sec = func.a16beatToSec(self._bpm)

        if instName == 'bass':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.square], [1.0, 0.3], [1.0, 1.0], aSynthe.FilterName.bandpass, [1,3500], [0.001, 0.02, 0.6, 0.01], 44100)
        elif instName == 'kick':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.0], aSynthe.FilterName.lowpass, [1000], [0.001, 0.02, 0.0001, 0.1], 44100)
        elif instName == 'snare':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.0], aSynthe.FilterName.lowpass, [3000], [0.001, 0.02, 0.0001, 0.1], 44100)
        elif instName == 'hihat':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise], [1.0], [1.0], aSynthe.FilterName.highpass, [7000], [0.0, 0.001, 0.0001, 0.01], 44100)


    def convertPerc(self, score, constHz):
        list = self._midiNotesToHzAndSec(score)
        wave = np.zeros(0)
        for hz, sec in list:
            wave = np.r_[wave, self._midiNoteToWave(constHz, sec)]

        return wave

    def convertPoly(self, score):

        wave_sum = None
        for i in range(len(score[0,:])):
            list = self._midiNotesToHzAndSec(score[:,i])
            wave = np.zeros(0)
            for hz, sec in list:
                wave = np.r_[wave, self._midiNoteToWave(hz, sec)]
            if wave_sum is None:
                wave_sum = wave
            else:
                if len(wave_sum) > len(wave) :
                    wave_sum[0:len(wave)] += wave
                else:
                    wave_sum += wave[0:len(wave_sum)]

        return wave_sum/len(score[0,:])

    def convert(self, score):
        list = self._midiNotesToHzAndSec(score)
        wave = np.zeros(0)
        for hz, sec in list:
            wave = np.r_[wave, self._midiNoteToWave(hz, sec)]

        return wave

    def _midiNotesToHzAndSec(self,score):
        list = []

        #最初無音から始まる対策
        if score[0] == -1:
            list.append([-1.0,0.0])

        #self._notePerBar_nが前提
        for note in score:
            if note > -1:
                list.append([func.midiNoteToHz(note), self._noteMinLen_sec])
            else:
                list[-1][1] += self._noteMinLen_sec
        return list

    def _midiNoteToWave(self, hz, sec):
        if hz > -1 :
            wave = self.synthesizer.setPitch(hz,sec)
        else :
            wave = self.synthesizer.soundless(sec)
        return wave

if __name__ == '__main__':

    #import json
    #import os
    #スクリプトのあるディレクトリの絶対パスを取得
    #name = os.path.dirname(os.path.abspath(__name__))
    #joined_path = os.path.join(name, './Composer/json/001_composition.json')
    #data_path = os.path.normpath(joined_path)

    #jsonFile = json.load(open(data_path, 'r'))
    #a = jsonFile.a
    #if a["Melody"][0]["args"][0]["reverce"] :
    #    print(jsonFile["Melody"][0]["args"][0]["reverce"])

    playObj = Play()
    playObj.setScore()
    playObj.setBpm(120)
    playObj.execute()
