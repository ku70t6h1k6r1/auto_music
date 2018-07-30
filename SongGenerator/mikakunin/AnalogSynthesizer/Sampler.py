# coding:utf-8
#default
import numpy as np

#option
import wave as wv
import struct
import scipy.signal
import glob
from enum import Enum

class FilterName(Enum):
    bandpass = "bandpass"
    bandcut = "bandcut"
    highpass = "highpass"
    lowpass = "lowpass"

class Sampler(object):
    def __init__(self, rate = 44100):
        self._rate = 44100 #ファイル読み込む用
        self._rate_for_return = rate #return用
        self._channels = 1
        self._sampleSize =  2
        self.cur_dir_idx = 0

    def set_instrument(self, dir):
        u"""
        WAVのフォーマットは 44100Hz, ch = 1, sampleSize = 2
        perc以外は別にいらない
        """
        self._inst = wv.open(dir, "rb")
        self._frameSize = self._inst.getnframes()
        self._wave_bin = self._inst.readframes(self._frameSize)
        self._wave = np.frombuffer(self._wave_bin, dtype='int16')
        self._wave = self._wave/max(abs(self._wave))

    def generate_constant_wave(self, length):
        silent = np.zeros(int(length * self._rate_for_return))
        _tmp_wave = np.r_[self._wave, silent] #本当はファイル形式と出力の差を埋める必要がある。
        return _tmp_wave[0:int(length * self._rate_for_return)]

    def set_instruments(self, dir):
        files = glob.glob(dir)

        wav_files = []
        for file in files:
            if file.find('.wav') > -1:
                wav_files.append(file)

        self.wav_files = np.array(wav_files)
        np.random.shuffle(self.wav_files)
        filename = self.wav_files[self.cur_dir_idx]
        self.set_instrument(filename)

    def generate_wave(self, length):
        silent = np.zeros(int(length * self._rate_for_return))
        _tmp_wave = np.r_[self._wave, silent]

        self.cur_dir_idx = self.cur_dir_idx + 1 if self.cur_dir_idx  + 1< len(self.wav_files) else 0
        filename = self.wav_files[self.cur_dir_idx]
        self.set_instrument(filename)

        return _tmp_wave[0:int(length * self._rate_for_return)]

class VCF(object):
    def __init__(self, filterName, frequency, rate = 44100):
        self._rate = rate
        self._nyq = self._rate / 2.0
        self._numtaps = 255
        self._filterName = filterName
        self._frequency = np.array(frequency) / self._nyq #0-self._rate /2-1

    def _lowPass(self, frequency):
        return scipy.signal.firwin(self._numtaps, frequency) # Filter Func

    def _highPass(self, frequency):
        return scipy.signal.firwin(self._numtaps, frequency, pass_zero=False)

    def _bandPass(self, frequency):
        return scipy.signal.firwin(self._numtaps, frequency, pass_zero=False)

    def _bandCut(self, frequency):
        return scipy.signal.firwin(self._numtaps, frequency)

    def _wave_func(self, wave):

        if self._filterName == "bandpass" :
            b = self._bandPass(self._frequency)
        elif self._filterName == "bandcut" :
            b = self._bandCut(self._frequency)
        elif self._filterName == "lowpass" :
            b = self._lowPass(self._frequency[0])
        elif self._filterName == "highpass" :
            b = self._highPass(self._frequency[0])
        else:
            b = None

        filtered_wave = scipy.signal.lfilter(b, 1, wave) #wave -1～1 多分マストではない
        return filtered_wave

    def processing(self, wave):
        return self._wave_func(wave)

class VCA(object):
    def __init__(self, attack_time, decay_time, sustain_level, release_time, rate = 44100):
        self._a = attack_time
        self._d = decay_time
        self._s = sustain_level # <1
        self._r =  release_time
        self._rate = rate

        self._a_list = np.linspace(0, 1, self._a * self._rate)
        self._d_list = np.linspace(1, self._s, self._d * self._rate)
        self._r_list = np.linspace(self._s, 0, self._r * self._rate)

    def _wave_func(self, wave):
        #print(u"waveの長さが短くなりすぎて、ADSRに収まらないときあり"）
        s_length = len(wave)-int((self._a+self._d+self._r)*self._rate)
        if s_length > 0:
            self._s_list = np.full(s_length, self._s)
            eg = np.r_[self._a_list, self._d_list, self._s_list, self._r_list]
        else:
            self._s_list = np.full(1000, self._s)
            eg = np.r_[self._a_list, self._d_list, self._s_list, self._r_list]
            eg = eg[0:len(wave)]

        return eg

    def processing(self, wave):
        eg = self._wave_func(wave)
        return eg * wave

class Amp(object):
    def maxStd(self, wave):
        #print(max(wave /max(abs(wave))))
        return wave /max(abs(wave))

    def threeSigma(self, wave, gain):
        absMax = np.mean(wave) + gain*1.0 * np.std(wave)
        for idx, val in enumerate(wave):
            if val > absMax:
                wave[idx] = absMax
            elif val <  -absMax:
                wave[idx] = -absMax

        wave = wave /max(abs(wave))
        return wave

class Synthesizer():
    def __init__(self, dir, filterName ,frequency ,adsr, rate):
        self._waveDir = dir #"C:/work/python/kick.wav"
        self._filterName = filterName #lowpass
        self._frequency = frequency #[100,1000]
        self._adsr = adsr #[0.001, 0.02, 0.6, 0.02]
        self._rate = rate #44100

        self._sample = Sampler()

        if self._waveDir.find('.wav') > -1:
            self._sample.set_instrument(self._waveDir)
        else:
            self._sample.set_instruments(self._waveDir)

        self._vcf = VCF(self._filterName, self._frequency, self._rate)
        self._vca = VCA(self._adsr[0], self._adsr[1], self._adsr[2], self._adsr[3], self._rate)
        self._amp = Amp()

    def setLength(self, length):
        if self._waveDir.find('.wav') > -1:
            buf = self._sample.generate_constant_wave(length)   #length is sec
        else:
            buf = self._sample.generate_wave(length)
        buf = self._vcf.processing(buf)
        buf = self._vca.processing(buf)
        buf = self._amp.maxStd(buf)
        return buf

    def soundless(self, length):
        return np.zeros(int(length * self._rate), dtype = 'float')

    def toBytes(self, wave):
        return (wave * float(2 ** (16 - 1) ) ).astype(np.int16).tobytes()

if __name__ == '__main3__' :
    import glob

    dir = 'C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/*'
    files = np.array(glob.glob(dir))

    wav_files = []
    for file in files:
        if file.find('.wav') > -1:
            wav_files.append(file)

    print(wav_files)

if __name__ == '__main2__' :
    import pyaudio
    audio  = pyaudio.PyAudio()
    o = audio.open(format=audio.get_format_from_width(2),
                                channels=1,
                                rate=44100,
                                output=True)

    synthObj = Synthesizer("C:/work/python/kick.wav", FilterName.highpass, [1000], [0.001, 0.02, 0.6, 0.02], 44100)
    wave = synthObj.setLength(1)
    o.write( (wave * float(2 ** (16 - 1) ) ).astype(np.int16).tobytes())
    print(wave)



"""
    hhObj = createWave(bpm)
    hhObj.set_instrument("C:/work/python/hihat.wav")

    sDObj = createWave(bpm)
    sDObj.set_instrument("C:/work/python/snare.wav")

    bDObj = createWave(bpm)
    bDObj.set_instrument("C:/work/python/kick.wav")

    baObj = createWave(bpm)
    baObj.set_synth()
"""
