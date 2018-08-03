# coding:utf-8
import numpy as np
from Composer import Score as sc
from AnalogSynthesizer import AnalogSynthesizer as aSynthe
from AnalogSynthesizer import Sampler as samp
from AnalogSynthesizer import Effector  as fxPSs

from common import function as func
import wave as wv
from datetime import datetime
import argparse
import json

class Play:
    def __init__(self):
        #Objects
        self.scoreObj = sc.Score()
        self.fxObj = fxPSs.Effector()
        #self.audio  = pyaudio.PyAudio()

        #Output Format
        #self.format = pyaudio.paInt32
        self.sampwidth = 4 #formatが16だと2
        self.channels = 2
        self.rate = 44100


        #Dirs
        self.scoreDir = './Composer/score/'
        self.outputDir = './wav/'
        self.scoreOutputDir = './json/'
        self.settingsDir = './AnalogSynthesizer/settings/'

        #Effecters
        self.amp = aSynthe.Amp()
        self.delay = aSynthe.Delay()
        self.comp = aSynthe.Compressor()
        self.dist = aSynthe.Distortion()
        self.volCtrl = aSynthe.VolumeController()
        self.filCtrl = aSynthe.FilterController()
        self.vib = aSynthe.Vibrato()
        self.tre = aSynthe.Tremolo()

    def setScore(self, name):
        self.scoreName = name
        self.score = self.scoreObj.load(self.scoreDir + self.scoreName + '.json')

    def setAudioParameters(self, name):
        self.settingName = name
        self.setting = json.load(open(self.settingsDir + self.settingName + '.json', 'r'))
        self.setting_asyn = self.setting['AnalogSynthesizer']
        self.setting_samp = self.setting['Sampler']
        self.setting_preset = self.setting['Preset']
        self.volume = self.setting['Volume']

    def setBpm(self, bpm):
        self.bpm = bpm

        #Score
        self.bassObj = midiNotesToWave(self.setting_asyn["bass"], bpm = self.bpm)
        self.bass2Obj = midiNotesToWave(self.setting_asyn["bass2"], bpm = self.bpm)
        self.leadObj = midiNotesToWave(self.setting_asyn["lead"], bpm = self.bpm)
        self.lead2Obj = midiNotesToWave(self.setting_asyn["lead2"], bpm = self.bpm)
        self.subLeadObj = midiNotesToWave(self.setting_asyn["subLead"], bpm = self.bpm)
        self.voiceObj = midiNotesToWave(self.setting_asyn["voice"], bpm = self.bpm)
        self.voice2Obj = midiNotesToWave(self.setting_asyn["voice2"], bpm = self.bpm)
        self.kickObj = midiNotesToWave(self.setting_asyn["kick"], bpm = self.bpm)
        self.kick2Obj = midiNotesToWave_Sampler(self.setting_samp["kick"], bpm = self.bpm)
        self.hihatObj = midiNotesToWave(self.setting_asyn["hihat"], bpm = self.bpm)
        self.hihat2Obj = midiNotesToWave_Sampler(self.setting_samp["hihat"],bpm = self.bpm)
        self.snareObj = midiNotesToWave(self.setting_asyn["snare"], bpm = self.bpm)
        self.snare2Obj = midiNotesToWave_Sampler(self.setting_samp["snare"], bpm = self.bpm)

        #FxPreset
        self.fxObj.setBpm(bpm)

        #Effects
        self.fx1Obj = midiNotesToWave_Sampler(self.setting_samp["fx1"], bpm = self.bpm)
        self.fx2Obj = midiNotesToWave_Sampler(self.setting_samp["fx2"], bpm = self.bpm)
        self.fx3Obj = midiNotesToWave_Sampler(self.setting_samp["fx3"], bpm = self.bpm)
        self.fx4Obj = midiNotesToWave_Sampler(self.setting_samp["fx4"], bpm = self.bpm)

    def execute(self, writeStream = True, fileOut = False):

        #melody
        melody_hz, melody = self.leadObj.convert(self.score.melodyLine)
        melody = self.fxObj.Set(melody, self.setting_preset["lead"]["presetName"], **self.setting_preset["lead"]["presetArgs"])

        #melody2
        melody2_hz, melody2 = self.lead2Obj.convert(self.score.melodyLine)
        melody2 = self.fxObj.Set(melody2, self.setting_preset["lead2"]["presetName"], **self.setting_preset["lead2"]["presetArgs"])

        #subMelody
        subMelody_hz, subMelody = self.subLeadObj.convert(self.score.melodyLine2)
        subMelody = self.fxObj.Set(subMelody, self.setting_preset["subLead"]["presetName"], **self.setting_preset["subLead"]["presetArgs"])

        #bass
        bass_hz, bass =  self.bassObj.convert(self.score.bassLine)
        bass = self.fxObj.Set(bass, self.setting_preset["bass"]["presetName"], **self.setting_preset["bass"]["presetArgs"])

        #bass2
        bass2_hz, bass2 =  self.bass2Obj.convert(self.score.bassLine)
        bass2 = self.fxObj.Set(bass2, self.setting_preset["bass2"]["presetName"], **self.setting_preset["bass2"]["presetArgs"])

        #voicing
        voicing_hz, voicing =  self.voiceObj.convertPoly(self.score.voiceProg)
        voicing = self.fxObj.Set(voicing, self.setting_preset["voice"]["presetName"], **self.setting_preset["voice"]["presetArgs"])

        #voicing2
        voicing2_hz, voicing2 =  self.voice2Obj.convertPoly(self.score.voiceProg2)
        voicing2 = self.fxObj.Set(voicing2, self.setting_preset["voice2"]["presetName"], **self.setting_preset["voice2"]["presetArgs"])

        #kick
        kick_hz, kick = self.kickObj.convertPerc(self.score.drumObj.kick, self.setting_asyn["kick"]["constHz"])
        kick = self.fxObj.Set(kick, self.setting_preset["kick"]["presetName"], **self.setting_preset["kick"]["presetArgs"])

        #Kick2
        kick2_hz, kick2 = self.kick2Obj.convert(self.score.drumObj.kick)
        kick2 = self.fxObj.Set(kick2, self.setting_preset["kick2"]["presetName"], **self.setting_preset["kick2"]["presetArgs"])

        #snare
        snare_hz, snare =  self.snareObj.convertPerc(self.score.drumObj.snare, self.setting_asyn["snare"]["constHz"])
        snare = self.fxObj.Set(snare, self.setting_preset["snare"]["presetName"], **self.setting_preset["snare"]["presetArgs"])

        #snare2
        snare2_hz, snare2 =  self.snare2Obj.convert(self.score.drumObj.snare)
        snare2 = self.fxObj.Set(snare2, self.setting_preset["snare2"]["presetName"], **self.setting_preset["snare2"]["presetArgs"])

        #hihat
        hihat_hz, hihat =  self.hihatObj.convertPerc(self.score.drumObj.hihat, self.setting_asyn["hihat"]["constHz"])
        hihat = self.fxObj.Set(hihat, self.setting_preset["hihat"]["presetName"], **self.setting_preset["hihat"]["presetArgs"])

        #hihat2
        hihat2_hz, hihat2 =  self.hihat2Obj.convert(self.score.drumObj.hihat)
        hihat2 = self.fxObj.Set(hihat2, self.setting_preset["hihat2"]["presetName"], **self.setting_preset["hihat2"]["presetArgs"])

        #fx1
        fx1_hz, fx1 = self.fx1Obj.convert(self.score.effectsObj.pt1)
        fx1 = self.fxObj.Set(fx1, self.setting_preset["fx1"]["presetName"], **self.setting_preset["fx1"]["presetArgs"])

        #fx2
        fx2_hz, fx2 = self.fx2Obj.convert(self.score.effectsObj.pt2)
        fx2 = self.fxObj.Set(fx2, self.setting_preset["fx2"]["presetName"], **self.setting_preset["fx2"]["presetArgs"])

        #fx3
        fx3_hz, fx3 = self.fx3Obj.convert(self.score.effectsObj.pt3)
        fx3 = self.fxObj.Set(fx3, self.setting_preset["fx3"]["presetName"], **self.setting_preset["fx3"]["presetArgs"])

        #fx4
        fx4_hz, fx4 = self.fx4Obj.convert(self.score.effectsObj.pt4)
        fx4 = self.fxObj.Set(fx4, self.setting_preset["fx4"]["presetName"], **self.setting_preset["fx4"]["presetArgs"])

        """
        長さ確認
        """
        print("melody : ", len(melody), len(self.score.melodyLine))
        print("melody2 : ", len(melody2), len(self.score.melodyLine))
        print("subMelody : ", len(subMelody), len(self.score.melodyLine2))
        print("bass : ", len(bass), len(self.score.bassLine), len(self.score.bassLine))
        print("bass2 : ", len(bass2), len(self.score.melodyLine), len(self.score.bassLine))
        print("voicing : ", len(voicing), len(self.score.voiceProg))
        print("voicing2 : ", len(voicing2), len(self.score.voiceProg2))
        print("kick  : ", len(kick ), len(self.score.drumObj.kick))
        print("kick2  : ", len(kick2), len(self.score.drumObj.kick))
        print("snare : ", len(snare), len(self.score.drumObj.snare))
        print("snare2 : ", len(snare2), len(self.score.drumObj.snare))
        print("hihat : ", len(hihat), len(self.score.drumObj.hihat))
        print("hihat2 : ", len(hihat2), len(self.score.drumObj.hihat))
        print("fx1 : ", len(fx1))
        print("fx2 : ", len(fx2))
        print("fx3 : ", len(fx3))
        print("fx4 : ", len(fx4))


        #melody : merge
        melody= func.add_stereo([melody, melody2, subMelody], \
            [  self.volume["melody"]["melody"],
                self.volume["melody"]["melody2"],
                self.volume["melody"]["subMelody"]   ])

        #bass:merge
        bass = func.add_stereo([bass, bass2], [self.volume["bass"]["bass"], self.volume["bass"]["bass2"]])

        #harm : merge
        harm = func.add_stereo([voicing, voicing2], \
            [   self.volume["harm"]["voicing"],
                self.volume["harm"]["voicing2"] ])

        #drums : merge
        drums = func.add_stereo([kick, kick2, snare, snare2, hihat, hihat2], \
            [   self.volume["drums"]["kick"],
                self.volume["drums"]["kick2"],
                self.volume["drums"]["snare"],
                self.volume["drums"]["snare2"],
                self.volume["drums"]["hihat"],
                self.volume["drums"]["hihat2"]  ])

        #fx : merge
        fx = func.add_stereo([fx1, fx2, fx3, fx4], \
            [   self.volume["fx"]["fx1"],
                self.volume["fx"]["fx2"],
                self.volume["fx"]["fx3"],
                self.volume["fx"]["fx4"]    ])

        """
        Mixer関係
        """
        #Melody
        melody = self.volCtrl.fourBeat_stereo(melody, self.bpm, [self.score.form[4]],  [self.score.form[6]], [0.4], [3.0])
        melody = self.volCtrl.sidechain_stereo(melody, self.bpm, snare_hz)
        #melody = self.volCtrl.feedIn_stereo(melody, self.bpm, [self.score.form[0]], [self.score.form[3]], ['liner'], [0.3])

        #BASS
        #bass = self.filCtrl.lowfi_stereo(bass, self.bpm, [self.score.form[1]], [self.score.form[3]]  ,'bandpass' ,[[1000,5000]])
        #bass = self.volCtrl.feedIn_stereo(bass, self.bpm, [self.score.form[4]], [self.score.form[5]], ['tanh'], [0.3])
        bass = self.volCtrl.sidechain_stereo(bass, self.bpm, kick_hz)

        #HARM
        #harm = self.filCtrl.lowfi_stereo(harm, self.bpm, [self.score.form[1]], [self.score.form[4]]  ,'bandpass' ,[[400,4000]])
        #harm = self.volCtrl.fourBeat_stereo(harm, self.bpm, [self.score.form[3]],  [self.score.form[6]], [0.0], [3.0])
        #harm = self.volCtrl.feedIn_stereo(harm, self.bpm, [self.score.form[0]], [self.score.form[3]], ['liner'], [0.3])

        #DRUMS
        drums = self.volCtrl.feedIn_stereo(drums, self.bpm, [self.score.form[3]], [self.score.form[4]], ['tanh'], [0.3])
        #drums = self.filCtrl.lowfi_stereo(drums, self.bpm, [self.score.form[1]], [self.score.form[3]]  ,'bandpass' ,[[3000,10000]])

        #FX
        fx = self.volCtrl.feedIn_stereo(fx, self.bpm, [self.score.form[0]], [self.score.form[1]], ['tanh'], [0.3])
        fx = self.filCtrl.lowfi_stereo(fx, self.bpm, [self.score.form[2]], [self.score.form[3]]  ,'bandpass' ,[[1000,10000]])


        #all : merge
        wave = func.add([melody, harm, bass, drums, fx], \
            [   self.volume["master"]["melody"],
                self.volume["master"]["harm"],
                self.volume["master"]["bass"],
                self.volume["master"]["drums"],
                self.volume["master"]["fx"]    ])

        #To Binary
        wave_bin = func.toBytes(wave)

        if writeStream:
            import pyaudio
            self.format = pyaudio.paInt32
            self.o = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, output=True)
            self.o.write(wave_bin)

        if fileOut:
            dt = datetime.now().strftime("%Y%m%d_%H%M%S")
            fileName = self.scoreName + '_' + self.settingName + '_' + str(self.bpm) + '__' + dt

            fileName_wv = fileName + '.wav'
            waveFile = wv.open(self.outputDir + fileName_wv , 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.sampwidth)
            waveFile.setframerate(self.rate)
            waveFile.writeframes(wave_bin)
            waveFile.close()

            score_dict = {}
            score_dict["melody"] = self.score.melodyLine.tolist()
            score_dict["chordProg"] = self.score.chordProg.tolist()
            fw = open(self.scoreOutputDir + fileName + '.json', 'w')
            json.dump(score_dict,fw,indent=4)

class midiNotesToWave:
    def __init__(self, setting, notePerBar_n = 16, bpm = 120):
        self.setting = setting
        self._notePerBar_n = notePerBar_n
        self._bpm = bpm
        self._noteMinLen_sec = func.a16beatToSec(self._bpm)

        if len(self.setting["waveForm"]) > 2 :
            self.synthesizer = aSynthe.Synthesizer_Poly(self.setting["waveForm"], self.setting["volume"], self.setting["transpose"], self.setting["freqFilterName"], self.setting["freqFilterRange"], self.setting["adsr"], self.setting["rate"])
        else:
            self.synthesizer = aSynthe.Synthesizer(self.setting["waveForm"], self.setting["volume"], self.setting["transpose"], self.setting["freqFilterName"], self.setting["freqFilterRange"], self.setting["adsr"], self.setting["rate"])


    def convertPerc(self, score, constHz):
        list = self._midiNotesToHzAndSec(score)
        wave = np.zeros(0)
        for hz, sec in list:
            wave = np.r_[wave, self._midiNoteToWave(constHz, sec)] if hz >= 0 else np.r_[wave, self._midiNoteToWave(hz, sec)]

        return list, wave

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

        return list, wave_sum/len(score[0,:])

    def convert(self, score):
        list = self._midiNotesToHzAndSec(score)
        wave = np.zeros(0)
        for hz, sec in list:
            wave = np.r_[wave, self._midiNoteToWave(hz, sec)]

        return list, wave

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
        if isinstance(hz, list) :
            wave = self.synthesizer.setPitch(hz,sec)
        elif hz > 0 :
            wave = self.synthesizer.setPitch(hz,sec)
        else :
            wave = self.synthesizer.soundless(sec)
        return wave

class midiNotesToWave_Sampler:
    def __init__(self, setting, notePerBar_n = 16, bpm = 120):
        self._notePerBar_n = notePerBar_n
        self._bpm = bpm
        self._noteMinLen_sec = func.a16beatToSec(self._bpm)
        self.setting = setting

        self.sampler = samp.Synthesizer(self.setting["file"], self.setting["freqFilterName"], self.setting["freqFilterRange"], self.setting["adsr"], self.setting["rate"])

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

        return list, wave_sum/len(score[0,:])

    def convert(self, score):
        list = self._midiNotesToHzAndSec(score)
        wave = np.zeros(0)
        for hz, sec in list:
            wave = np.r_[wave, self._midiNoteToWave(hz, sec)]

        return list, wave

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
    parser.add_argument('-p', '--parameters', type=str, default='setting')
    parser.add_argument('-b', '--bpm', type=int, default=120)
    parser.add_argument('-fo', '--fileout', action='store_true')
    parser.add_argument('-ws', '--writestream', action='store_true')
    args = parser.parse_args()
    #play
    playObj = Play()
    playObj.setScore(args.score)
    playObj.setAudioParameters(args.parameters)
    playObj.setBpm(args.bpm)
    playObj.execute(writeStream = args.writestream, fileOut = args.fileout)
