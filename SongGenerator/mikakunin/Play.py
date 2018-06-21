# coding:utf-8
import numpy as np
from Composer import Score as sc
from AnalogSynthesizer import AnalogSynthesizer as aSynthe
from common import function as func
import pyaudio
import wave as wv
from datetime import datetime
import argparse

class Play:
    def __init__(self):
        self.scoreObj = sc.Score()
        self.audio  = pyaudio.PyAudio()

        self.format = pyaudio.paInt32
        self.sampwidth = 4 #formatが16だと2
        self.channels = 1
        self.rate = 44100
        self.o = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, output=True)

        self.scoreDir = './Composer/score/'
        self.outputDir = './wav/'

    def setScore(self, name):
        self.scoreName = name
        self.score = self.scoreObj.load(self.scoreDir + self.scoreName + '.json')

    def setBpm(self, bpm):
        self.bassObj = midiNotesToWave('bass',bpm = bpm)
        self.leadObj = midiNotesToWave('lead',bpm = bpm)
        self.lead2Obj = midiNotesToWave('lead2',bpm = bpm)
        self.voiceObj = midiNotesToWave('voice',bpm = bpm)
        self.kickObj = midiNotesToWave('kick',bpm = bpm)
        self.hihatObj = midiNotesToWave('hihat',bpm = bpm)
        self.snareObj = midiNotesToWave('snare',bpm = bpm)

    def execute(self, writeStream = True, fileOut = False):
        melody = self.leadObj.convert(self.score.melodyLine)
        melody2 = self.lead2Obj.convert(self.score.melodyLine)
        bass =  self.bassObj.convert(self.score.bassLine)
        voicing =  self.voiceObj.convertPoly(self.score.voiceProg)
        kick = self.kickObj.convertPerc(self.score.drumObj.kick, 50)
        snare =  self.snareObj.convertPerc(self.score.drumObj.snare, 40)
        hihat =  self.hihatObj.convertPerc(self.score.drumObj.hihat, 800)
        #wave = func.add([bass, snare, hihat, voicing], [6, 2, 4, 2])
        wave = func.add([kick, snare, hihat, bass, voicing, melody, melody2], [6.0, 2.0, 2.0, 5.0, 1.0, 1.0, 0.2])
        wave_bin = func.toBytes(wave)

        if writeStream:
            self.o.write(wave_bin)

        if fileOut:
            dt = datetime.now().strftime("%Y%m%d_%H%M%S")
            fileName = self.scoreName + '__' + dt + '.wav'

            waveFile = wv.open(self.outputDir + fileName , 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.sampwidth)
            waveFile.setframerate(self.rate)
            waveFile.writeframes(wave_bin)
            waveFile.close()


class midiNotesToWave:
    def __init__(self, instName, notePerBar_n = 16, bpm = 120):
        self._notePerBar_n = notePerBar_n
        self._bpm = bpm
        self._noteMinLen_sec = func.a16beatToSec(self._bpm)

        if instName == 'bass':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sine], [1.0, 0.5], [1.0, 2.0], aSynthe.FilterName.bandpass, [1,9000], [0.001, 0.02, 0.9, 0.01], 44100)
        if instName == 'lead':
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandpass, [1000,12000], [0.05, 0.01, 0.4, 0.01], 44100)
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandcut, [5000,12000], [0.03, 0.2, 0.1, 0.01], 44100)
        if instName == 'lead2':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.square], [1.0, 0.8], [1.02, 1.02], aSynthe.FilterName.bandpass, [10000, 12000], [0.05, 0.01, 0.4, 0.01], 44100)
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.sine], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandcut, [5000,12000], [0.03, 0.2, 0.1, 0.01], 44100)
        #elif instName == 'voice':
        #    self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.05], [1.0, 0.01], aSynthe.FilterName.bandpass, [10,10000], [0.001, 0.02, 0.6, 0.2], 44100)
        elif instName == 'voice':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.8], [1.0, 2.02], aSynthe.FilterName.bandpass, [50,1200], [0.0, 0.1, 0.8, 0.1], 44100)
        elif instName == 'kick':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0, 0.8], [1.0, 0.0], aSynthe.FilterName.lowpass, [200], [0.001, 0.02, 0.1 ,0.1], 44100)
        elif instName == 'snare':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.square], [1.0, 1.0], [1.0, 0.5], aSynthe.FilterName.bandcut, [5,100], [0.0, 0.02, 0.002, 0.1], 44100)
        elif instName == 'hihat':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0,0.2], [1.0,0.0], aSynthe.FilterName.highpass, [7000], [0.0, 0.01, 0.001, 0.01], 44100)


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

#if __name__ == '__main__':
    #from Composer import Melody as mel
    #methods = mel.Methods()
    #methods._maruBatsu()


    #scoreObj = sc.Score()
    #scoreObj.create('./Composer/settings/default.json')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='MAKE SONG')
    parser.add_argument('-s', '--score', type=str, default='test')
    parser.add_argument('-b', '--bpm', type=int, default=120)
    parser.add_argument('-fo', '--fileout', action='store_true')
    parser.add_argument('-ws', '--writestream', action='store_true')
    args = parser.parse_args()
    #play
    playObj = Play()
    playObj.setScore(args.score)
    playObj.setBpm(args.bpm)
    playObj.execute(writeStream = args.writestream, fileOut = args.fileout)
