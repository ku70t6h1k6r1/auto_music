# coding:utf-8
import numpy as np
from Composer import Score as sc
from AnalogSynthesizer import AnalogSynthesizer as aSynthe
from AnalogSynthesizer import Sampler as samp
from common import function as func
import pyaudio
import wave as wv
from datetime import datetime
import argparse

class Play:
    def __init__(self):
        #Objects
        self.scoreObj = sc.Score()
        self.audio  = pyaudio.PyAudio()

        #Output Format
        self.format = pyaudio.paInt32
        self.sampwidth = 4 #formatが16だと2
        self.channels = 1
        self.rate = 44100
        self.o = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, output=True)

        #Dirs
        self.scoreDir = './Composer/score/'
        self.outputDir = './wav/'

        #Effecters
        self.amp = aSynthe.Amp()
        self.delay = aSynthe.Delay()
        self.comp = aSynthe.Compressor()
        self.dist = aSynthe.Distortion()


    def setScore(self, name):
        self.scoreName = name
        self.score = self.scoreObj.load(self.scoreDir + self.scoreName + '.json')

    def setBpm(self, bpm):
        self.bpm = bpm
        self.bassObj = midiNotesToWave('bass',bpm = self.bpm)
        self.leadObj = midiNotesToWave('lead',bpm = self.bpm)
        self.lead2Obj = midiNotesToWave('lead2',bpm = self.bpm)
        self.voiceObj = midiNotesToWave('voice',bpm = self.bpm)
        #self.kickObj = midiNotesToWave('kick',bpm = self.bpm)
        self.kickObj = midiNotesToWave_Sampler('kick',bpm = self.bpm)
        self.kick2Obj = midiNotesToWave_Sampler('kick2',bpm = self.bpm)
        self.hihatObj = midiNotesToWave('hihat',bpm = self.bpm)
        self.hihat2Obj = midiNotesToWave_Sampler('hihat2',bpm = self.bpm)
        #self.snareObj = midiNotesToWave('snare',bpm = self.bpm)
        self.snareObj = midiNotesToWave_Sampler('snare',bpm = self.bpm)
        self.snare2Obj = midiNotesToWave_Sampler('snare2',bpm = self.bpm)

        self.fx1Obj = midiNotesToWave_Sampler('fx1',bpm = self.bpm)
        self.fx4Obj = midiNotesToWave_Sampler('fx4',bpm = self.bpm)

    def execute(self, writeStream = True, fileOut = False):
        melody = self.leadObj.convert(self.score.melodyLine)
        melody = self.dist.hardClipping(melody,10)
        melody = self.comp.sigmoid(melody,1)
        melody = self.delay.reverb(melody, 0.9)

        melody2 = self.lead2Obj.convert(self.score.melodyLine)
        melody2 = self.dist.hardClipping(melody2,9)

        bass =  self.bassObj.convert(self.score.bassLine)
        bass = self.dist.hardClipping(bass,3)
        bass = self.comp.sigmoid(bass,3)

        #voicing2 =  self.voice2Obj.convert(self.score.drumObj.kick)
        voicing =  self.voiceObj.convertPoly(self.score.voiceProg)
        voicing = self.dist.hardClipping(voicing,1)
        bass = self.comp.sigmoid(bass,1)

        kick = self.kickObj.convert(self.score.drumObj.kick) #convertPerc(50)
        kick = self.dist.hardClipping(kick,0.2)
        #kick = self.delay.delay(kick)
        kick = self.amp.maxStd(kick)
        #kick = self.comp.sigmoid(kick,5)
        kick2 = self.kick2Obj.convert(self.score.drumObj.kick)

        #snare =  self.snareObj.convertPerc(self.score.drumObj.snare, 40)
        #snare = self.dist.hardClipping(snare,0.1)
        #snare  = self.amp.maxStd(snare)
        snare =  self.snareObj.convert(self.score.drumObj.snare)
        snare2 =  self.snare2Obj.convert(self.score.drumObj.snare)

        fx1 = self.fx1Obj.convert(self.score.effectsObj.pt1)
        fx1 = self.dist.hardClipping(fx1,4)
        fx1 = self.delay.reverb(fx1, 0.8)

        fx4 = self.fx4Obj.convert(self.score.effectsObj.pt4)
        fx4 = self.dist.hardClipping(fx4,4)
        fx4 = self.delay.reverb(fx4, 0.8)

        hihat =  self.hihatObj.convertPerc(self.score.drumObj.hihat, 800)
        hihat2 =  self.hihat2Obj.convert(self.score.drumObj.hihat)

        drums = func.add([kick, kick2, fx1, snare, snare2, fx4, hihat, hihat2], [4.0 ,4.0 , 1.0, 1.0/2, 2.0, 1.0, 4.0, 4.0])

        #drums = self.amp.threeSigma(drums, 10)
        #drums = self.dist.hardClipping(drums,0.4)
        drums = self.comp.sigmoid(drums,2)
        #drums = self.amp.threeSigma(drums,10)
        drums = self.delay.reverb(drums, 0.3)
        drums = self.comp.sigmoid(drums,1)
        #drums = self.vcf(drums, aSynthe.FilterName.bandpass, [1,800])

        #wave = drums

        wave = func.add([drums, bass, voicing, melody, melody2], [30.0, 4.0, 5.0, 12, 3.5])

        wave_bin = func.toBytes(wave)

        if writeStream:
            self.o.write(wave_bin)

        if fileOut:
            dt = datetime.now().strftime("%Y%m%d_%H%M%S")
            fileName = self.scoreName + '_' + str(self.bpm) + '__' + dt + '.wav'

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
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.2], [1.0, 1.0], aSynthe.FilterName.lowpass, [5000], [0.0, 0.05, 0.8, 0.01], 44100)
        elif instName == 'lead':
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandpass, [1000,12000], [0.05, 0.01, 0.4, 0.01], 44100)
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.sawtooth], [1.0, 1.5], [1.0, 0.02], aSynthe.FilterName.lowpass, [4000], [0.1, 0.1, 0.05, 0.01], 44100)
        elif instName == 'lead2':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.whitenoise], [1.0, 0.2], [1.01, 0.75], aSynthe.FilterName.bandcut, [10, 10000], [0.01, 0.1, 0.05, 0.01], 44100)
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.sine], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandcut, [5000,12000], [0.03, 0.2, 0.1, 0.01], 44100)
        #elif instName == 'voice':
        #    self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.05], [1.0, 0.01], aSynthe.FilterName.bandpass, [10,10000], [0.001, 0.02, 0.6, 0.2], 44100)
        elif instName == 'voice':#2.1は音痴
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sine], [1.0, 0.8], [1.0, 1.001], aSynthe.FilterName.highpass, [100], [0.01, 0.2, 0.8, 0.1], 44100)割といい
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sine], [1.0, 0.8], [1.0, 1.001], aSynthe.FilterName.bandcut, [20,200], [0.01, 0.2, 0.8, 0.1], 44100)
        elif instName == 'kick':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [0.8, 0.8], [1.0, 0.0], aSynthe.FilterName.lowpass, [60], [0.0, 0.04, 0.2 ,0.1], 44100)
        elif instName == 'snare':
            #self.sampler = samp.Synthesizer("C:/work/python/kick.wav", FilterName.highpass, [1000], [0.001, 0.02, 0.6, 0.02], 44100)
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0, 1.0], [1.0, 0.5], aSynthe.FilterName.bandcut, [500,20000], [0.0001, 0.02, 0.02, 0.1], 44100)
        elif instName == 'hihat':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0,0.2], [1.0,0.0], aSynthe.FilterName.bandcut, [10,16000], [0.0001, 0.01, 0.001, 0.01], 44100)


    def convertPerc(self, score, constHz):
        list = self._midiNotesToHzAndSec(score)
        wave = np.zeros(0)
        for hz, sec in list:
            wave = np.r_[wave, self._midiNoteToWave(constHz, sec)] if hz >= 0 else np.r_[wave, self._midiNoteToWave(hz, sec)]

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
        if score[0] < 0:
            list.append([-2.0,0.0]) #元々は[-1.0, 0.0]

        #self._notePerBar_nが前提
        for note in score:
            if note != -1: #-2:無音対策
                list.append([func.midiNoteToHz(note), self._noteMinLen_sec])
            else:
                list[-1][1] += self._noteMinLen_sec
        return list

    def _midiNoteToWave(self, hz, sec):
        if hz > 0 :
            wave = self.synthesizer.setPitch(hz,sec)
        else :
            wave = self.synthesizer.soundless(sec)
        return wave

    #def _midiNoteToWave_sampler(self, sec):
    #    if hz > -1 :
    #        wave = self.self.sampler.setPitch(sec)
    #    else :
    #        wave = self.sampler.soundless(sec)
    #    return wave

class midiNotesToWave_Sampler:
    def __init__(self, instName, notePerBar_n = 16, bpm = 120):
        self._notePerBar_n = notePerBar_n
        self._bpm = bpm
        self._noteMinLen_sec = func.a16beatToSec(self._bpm)

        if instName == 'bass':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sine], [1.0, 0.1], [1.0, 2.0], aSynthe.FilterName.lowpass, [6000], [0.03, 0.02, 0.9, 0.01], 44100)
        elif instName == 'lead':
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandpass, [1000,12000], [0.05, 0.01, 0.4, 0.01], 44100)
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.lowpass, [500], [0.01, 0.01, 0.1, 0.01], 44100)
        elif instName == 'lead2':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.square], [1.0, 0.8], [1.02, 1.02], aSynthe.FilterName.bandpass, [10000, 12000], [0.05, 0.01, 0.4, 0.01], 44100)
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.sine], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandcut, [5000,12000], [0.03, 0.2, 0.1, 0.01], 44100)
        #elif instName == 'voice':
        #    self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.05], [1.0, 0.01], aSynthe.FilterName.bandpass, [10,10000], [0.001, 0.02, 0.6, 0.2], 44100)
        elif instName == 'voice':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 2.02], aSynthe.FilterName.bandpass, [50,1200], [0.01, 0.1, 0.8, 0.1], 44100)
        elif instName == 'fx1':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/venova_proc_20180628_175220.wav", samp.FilterName.bandpass, [10,8000], [0.3, 0.02, 0.8, 0.02], 44100)
        elif instName == 'kick':
            self.sampler = samp.Synthesizer("C:/work/python/kick.wav", samp.FilterName.lowpass, [100], [0.001, 0.02, 0.6, 0.02], 44100)
        elif instName == 'kick2':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/box_proc_20180628_174821.wav", samp.FilterName.lowpass, [100], [0.001, 0.02, 0.6, 0.02], 44100)
        elif instName == 'snare':
            self.sampler = samp.Synthesizer("C:/work/python/snare.wav", samp.FilterName.bandcut, [100,2000], [0.001, 0.02, 0.6, 0.02], 44100)
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0, 1.0], [1.0, 0.5], aSynthe.FilterName.bandcut, [500,20000], [0.0001, 0.02, 0.02, 0.1], 44100)
        elif instName == 'snare2':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/keyboard_proc_20180628_175123.wav", samp.FilterName.bandcut, [300,8000], [0.001, 0.02, 0.6, 0.02], 44100)
        elif instName == 'snare3':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/rindarinda_proc_20180628_175248.wav", samp.FilterName.bandpass, [300,8000], [0.3, 0.02, 0.3, 0.02], 44100)
        elif instName == 'fx4':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/rindarinda_proc_20180628_180349.wav", samp.FilterName.bandpass, [300,8000], [0.3, 0.02, 0.3, 0.02], 44100)
        elif instName == 'hihat':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0,0.2], [1.0,0.0], aSynthe.FilterName.bandpass, [8000,16000], [0.0001, 0.01, 0.001, 0.01], 44100)
        elif instName == 'hihat2':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/eSkateBoard_proc_20180628_175042.wav", samp.FilterName.bandpass, [1600,8000], [0.001, 0.02, 0.1, 0.02], 44100)



    #def convertPerc(self, score):
    #    list = self._midiNotesToHzAndSec(score)
    #    wave = np.zeros(0)
    #    for hz, sec in list:
    #        wave = np.r_[wave, self._midiNoteToWave(sec)]

    #    return wave

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
        if score[0] < 0:
            list.append([-2.0,0.0])

        #self._notePerBar_nが前提
        for note in score:
            if note != -1:
                list.append([func.midiNoteToHz(note), self._noteMinLen_sec])
            else:
                list[-1][1] += self._noteMinLen_sec
        return list

    def _midiNoteToWave(self, hz, sec):
        if hz > 0 :
            wave = self.sampler.setLength(sec)
        else :
            wave = self.sampler.soundless(sec)
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
