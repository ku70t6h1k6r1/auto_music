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
        self.volCtrl = aSynthe.VolumeController()
        self.vib = aSynthe.Vibrato()
        self.tre = aSynthe.Tremolo()

    def setScore(self, name):
        self.scoreName = name
        self.score = self.scoreObj.load(self.scoreDir + self.scoreName + '.json')

    def setBpm(self, bpm):
        #Score
        self.bpm = bpm
        self.bassObj = midiNotesToWave('bass',bpm = self.bpm)
        self.leadObj = midiNotesToWave('lead',bpm = self.bpm)
        self.lead2Obj = midiNotesToWave('lead2',bpm = self.bpm)
        self.voiceObj = midiNotesToWave('voice',bpm = self.bpm)
        self.kickObj = midiNotesToWave('kick',bpm = self.bpm)
        self.kick2Obj = midiNotesToWave_Sampler('kick',bpm = self.bpm)
        self.hihatObj = midiNotesToWave('hihat',bpm = self.bpm)
        self.hihat2Obj = midiNotesToWave_Sampler('hihat',bpm = self.bpm)
        self.snareObj = midiNotesToWave('snare',bpm = self.bpm)
        self.snare2Obj = midiNotesToWave_Sampler('snare',bpm = self.bpm)

        #Effects
        self.fx1Obj = midiNotesToWave_Sampler('fx1',bpm = self.bpm)
        self.fx2Obj = midiNotesToWave_Sampler('fx2',bpm = self.bpm)
        self.fx3Obj = midiNotesToWave_Sampler('fx3',bpm = self.bpm)
        self.fx4Obj = midiNotesToWave_Sampler('fx4',bpm = self.bpm)

    def execute(self, writeStream = True, fileOut = False):
        melody = self.leadObj.convert(self.score.melodyLine)
        melody = self.dist.hardClipping(melody,10)
        melody = self.comp.sigmoid(melody,1)
        melody = self.delay.reverb(melody, 0.9)

        melody2 = self.lead2Obj.convert(self.score.melodyLine)
        melody2 = self.dist.hardClipping(melody2,9)
        melody2 = self.tre.am(melody2, 0.4, 1/(60.0/self.bpm))


        bass =  self.bassObj.convert(self.score.bassLine)
        bass = self.dist.hardClipping(bass,3)
        bass = self.comp.sigmoid(bass,3)
        bass = func.add([self.vib.sine(bass, depth = 1.0/2, freq = 0.3), bass], [1.0, 1.0])

        voicing =  self.voiceObj.convertPoly(self.score.voiceProg)
        voicing = self.dist.hardClipping(voicing,2)
        voicing = func.add([self.vib.sine(voicing, depth = 3, freq = 0.1), voicing], [1.0, 1.0])

        kick = self.kickObj.convertPerc(self.score.drumObj.kick, 50)
        kick = self.dist.hardClipping(kick,0.2)
        #kick = self.delay.delay(kick)
        kick = self.amp.maxStd(kick)
        #kick = self.comp.sigmoid(kick,5)
        kick2 = self.kick2Obj.convert(self.score.drumObj.kick)

        #snare =  self.snareObj.convertPerc(self.score.drumObj.snare, 40)
        #snare = self.dist.hardClipping(snare,0.1)
        #snare  = self.amp.maxStd(snare)
        snare =  self.snareObj.convertPerc(self.score.drumObj.snare, 40)
        snare2 =  self.snare2Obj.convert(self.score.drumObj.snare)

        hihat =  self.hihatObj.convertPerc(self.score.drumObj.hihat, 800)
        hihat2 =  self.hihat2Obj.convert(self.score.drumObj.hihat)

        fx1 = self.fx1Obj.convert(self.score.effectsObj.pt1)
        fx1 = self.dist.hardClipping(fx1,4)
        fx1 = self.delay.reverb(fx1, 0.8)

        fx2 = self.fx2Obj.convert(self.score.effectsObj.pt2)

        fx3 = self.fx3Obj.convert(self.score.effectsObj.pt3)
        fx3 = self.dist.hardClipping(fx3,4)
        fx3 = self.delay.reverb(fx3, 0.8)

        #fx4 = self.fx4Obj.convert(self.score.effectsObj.pt4)

        harm = func.add([bass, voicing, melody, melody2], [1.25, 1.5, 4.5, 1.0])
        #harm = func.add([self.vib.sine(harm, depth = 1, freq = 0.3), harm], [1.0, 1.0])

        harm  = self.volCtrl.ending(harm , 15)

        drums = func.add([kick, kick2, snare, snare2, hihat, hihat2], [2.0, 5.0, 1.0, 3.0, 1.0, 2.0])
        drums = self.comp.sigmoid(drums,2)
        drums = self.delay.reverb(drums, 0.5)
        drums = self.comp.sigmoid(drums,1)
        drums  = self.volCtrl.ending(drums , 15)

        fx = func.add([fx1, fx2, fx3], [1.0, 1.0, 1.0])
        fx = self.tre.am(fx, 0.3, 0.5)

        wave = func.add([harm, drums, fx], [2, 2.2, 2])
        #wave = self.vib.sine(wave, depth = 4, freq = 0.8)
        #wave_vib = self.vib.sine(wave, 0.5, 0.4)
        #wave = func.add([wave, wave_vib], [1, 1])
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
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sine], [1.0, 0.8], [1.0, 1.001], aSynthe.FilterName.bandcut, [20,200], [0.01, 0.2, 0.8, 0.1], 44100)割といい
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.8], [1.0, 1.00], aSynthe.FilterName.lowpass, [7000], [0.01, 0.2, 0.8, 0.1], 44100)
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
            wave = self.synthesizer.setPitch(hz,sec)
        else :
            wave = self.synthesizer.soundless(sec)
        return wave

class midiNotesToWave_Sampler:
    def __init__(self, instName, notePerBar_n = 16, bpm = 120):
        self._notePerBar_n = notePerBar_n
        self._bpm = bpm
        self._noteMinLen_sec = func.a16beatToSec(self._bpm)

        if instName == 'kick':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/box_proc_20180628_174821.wav", samp.FilterName.lowpass, [100], [0.001, 0.02, 0.6, 0.02], 44100)
        elif instName == 'snare':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/keyboard_proc_20180628_175123.wav", samp.FilterName.bandcut, [300,8000], [0.001, 0.02, 0.6, 0.02], 44100)
        elif instName == 'hihat':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/eSkateBoard_proc_20180628_175042.wav", samp.FilterName.bandpass, [1600,8000], [0.001, 0.02, 0.1, 0.02], 44100)
        #elif instName == 'snare3':
        #    self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/rindarinda_proc_20180628_175248.wav", samp.FilterName.bandpass, [300,8000], [0.3, 0.02, 0.3, 0.02], 44100)
        elif instName == 'fx1':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/venova_proc_20180628_175220.wav", samp.FilterName.bandpass, [10,8000], [0.3, 0.02, 0.8, 0.02], 44100)
        elif instName == 'fx2':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/eSkateBoard_proc_20180628_175042.wav", samp.FilterName.bandpass, [1600,8000], [0.001, 0.02, 0.1, 0.02], 44100)
        elif instName == 'fx3':
            self.sampler = samp.Synthesizer("C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/rindarinda_proc_20180628_180349.wav", samp.FilterName.bandpass, [300,8000], [0.3, 0.02, 0.3, 0.02], 44100)
        elif instName == 'fx4':
            return None

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
