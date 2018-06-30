# coding:utf-8
#default
import numpy as np

#option
import pygame
import pyaudio
import wave as wv
import struct
import scipy.signal
from enum import Enum

class Waveform(Enum):
    sine = "sine"
    sawtooth = "sawtooth"
    square = "square"
    whitenoise = "whitenoise"

class FilterName(Enum):
    bandpass = "bandpass"
    bandcut = "bandcut"
    highpass = "highpass"
    lowpass = "lowpass"

class Oscillator(object):
    def __init__(self, waveform, volume, freq_transpose=1.0):
        self._waveform = waveform
        self._volume = max(0.0, min(1.0, volume))
        self._freq_transpose = freq_transpose

    @property
    def volume(self):
        return self._volume

    #@property
    def _wave_func(self,phases):
        if self._waveform is Waveform.sine:
            return np.sin(phases)
        elif self._waveform is Waveform.sawtooth:
            return scipy.signal.sawtooth(phases)
        elif self._waveform is Waveform.square:
            return scipy.signal.square(phases)
        elif self._waveform is Waveform.whitenoise:
            wn = np.random.normal(0, 1, size=len(phases))
            threshold = 1.96
            for idx, val in enumerate(wn):
                if val > threshold:
                    wn[idx] = threshold
                elif -val >  threshold:
                    wn[idx] = -threshold
            wn = wn / max(np.absolute(wn)) if max(np.absolute(wn)) > 0 else wn
            return wn
        raise TypeError("unknown waveform: {}".format(self._waveform))

    def generate_wave(self, phases):
        phases = np.copy(phases) * self._freq_transpose
        return self._volume * self._wave_func(phases)

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

        if FilterName.bandpass == self._filterName :
            b = self._bandPass(self._frequency)
        elif FilterName.bandcut == self._filterName :
            b = self._bandCut(self._frequency)
        elif FilterName.lowpass == self._filterName :
            b = self._lowPass(self._frequency[0])
        elif FilterName.highpass == self._filterName :
            b = self._highPass(self._frequency[0])
        else:
            b = None

        filtered_wave = scipy.signal.lfilter(b, 1, wave) #wave -1～1 多分マストではない
        return filtered_wave

    def processing(self, wave):
        return self._wave_func(wave)

class VCO(object):
    def __init__(self, \
                osc1_waveform=Waveform.sine, \
                osc1_volume=1.0, \
                use_osc2=False,  \
                osc2_waveform=Waveform.sine, \
                osc2_volume=0.3, \
                osc2_freq_transpose=2.0, \
                rate=44100):

        self._osc1 = Oscillator(waveform=osc1_waveform, volume=osc1_volume)
        self._use_osc2 = use_osc2
        if self._use_osc2:
            self._osc2 = Oscillator(waveform=osc2_waveform, volume=osc2_volume, freq_transpose=osc2_freq_transpose)
        else:
            self._osc2 = None
        self._rate = rate

    def _generate_wave(self, phases):
        wave = self._osc1.generate_wave(phases)
        if self._use_osc2:
            wave += self._osc2.generate_wave(phases)
            wave *= (1.0 / (self._osc1.volume + self._osc2.volume))
        return wave

    def generate_constant_wave(self, frequency, length):
        phases = np.cumsum(2.0 * np.pi * frequency / self._rate * np.ones(int(self._rate * float(length))))
        return self._generate_wave(phases)

class Amp(object):
    def maxStd(self, wave):
        #print(max(wave /max(abs(wave))))
        return wave /max(abs(wave)) if  max(abs(wave)) > 0 else wave

    def threeSigma(self, wave, gain):
        absMax = np.mean(wave) + gain*1.0 * np.std(wave)
        for idx, val in enumerate(wave):
            if val > absMax:
                wave[idx] = absMax
            elif val <  -absMax:
                wave[idx] = -absMax

        wave = wave /max(abs(wave)) if max(abs(wave)) > 0 else wave
        return wave



#Effector類は基本、bufごとでは使わない。
class Compressor(object):
    def sigmoid(self, wave, gain):
        wave = wave*gain*0.5 /max(abs(wave)) if max(abs(wave)) > 0 else wave
        wave = np.tanh(wave)
        return  wave /max(abs(wave)) if max(abs(wave)) > 0 else wave

class Distortion(object):
    def hardClipping(self, wave, gain): #
        threshold = np.mean(wave) +  0.5/gain * 3.0 * np.std(wave)
        for idx, val in enumerate(wave):
            if val > threshold:
                wave[idx] = threshold
            elif -val >  threshold:
                wave[idx] = -threshold
        return wave /max(abs(wave))  if max(abs(wave)) > 0 else wave

class Delay(object):
    def reverb(self, wave, depth):
        delay = int(0.01 * 44100)
        wave_output = wave

        n = 0.0
        while depth**n > 0.00001:
            sirence = np.array([0]* delay * int(n) )
            wave_output = wave_output + np.r_[sirence, wave[0:int(len(wave)-delay * n)]*(depth**n) ]
            n += 1.0

        wave_output = wave_output/max(abs(wave_output)) if max(abs(wave_output)) > 0 else wave_output
        return wave_output

    def delay(self, data,frame=1500,amp=0.2,repeat=100):
        out = []
        amp_list = [amp ** i for i in range(repeat+1)]

        for i in range(len(data)):
            # y(i)を適宜計算
            d = 0
            for j in range(repeat + 1):
                index = i - frame * j # delay元となるindexを計算
                if index >= 0:
                    d += data[index] * amp_list[j]
                    #d *= 0.7 # 加算しているので適宜クリッピング
            out.append(d) # y(i)をlistに格納

        out = np.array(out)/max(abs(np.array(out))) if max(abs(np.array(out))) > 0 else np.array(out)
        return np.array(out)

class Synthesizer():
    def __init__(self, waveform, volume, freqtranspose, filterName ,frequency ,adsr, rate):
        self._waveform = waveform #[seine, saw]
        self._volume = volume #[1,0.3]
        self._freqtranspose = freqtranspose #[1,1]
        self._filterName = filterName #lowpass
        self._frequency = frequency #[100,1000]
        self._adsr = adsr #[0.001, 0.02, 0.6, 0.02]
        self._rate = rate #44100

        if len(self._waveform) > 1:
            self._vco = VCO(self._waveform[0], self._volume[0], True, self._waveform[1], self._volume[1], self._freqtranspose[1], self._rate)
        else :
            self._vco = VCO(self._waveform[0], self._volume[0], False, self._rate)

        self._vcf = VCF(self._filterName, self._frequency, self._rate)
        self._vca = VCA(self._adsr[0], self._adsr[1], self._adsr[2], self._adsr[3], self._rate)
        self._amp = Amp()


    def setPitch(self, frequency, length):
        buf = self._vco.generate_constant_wave(frequency, length) #length is sec
        buf = self._vcf.processing(buf)
        buf = self._vca.processing(buf)
        buf = self._amp.maxStd(buf)
        #buf = (buf * float(2 ** 15 - 1)).astype(np.int16).tobytes()
        return buf

    def soundless(self, length):
        return np.zeros(int(length * self._rate), dtype = 'float')

    def toBytes(self, wave):
        return (wave * float(2 ** (16 - 1) ) ).astype(np.int16).tobytes()

if __name__ == '__main__' :
    audio  = pyaudio.PyAudio()
    o = audio.open(format=audio.get_format_from_width(2),
                                channels=1,
                                rate=44100,
                                output=True)



    #SNARE?
    #synthesizer = Synthesizer([Waveform.whitenoise, Waveform.square], [1.0, 0.8], [1.0, 1.0], FilterName.lowpass, [3000], [0.001, 0.02, 0.0001, 0.1], 44100)
    #wave = synthesizer.setPitch(150,2)

    #KICK?
    synthesizer = Synthesizer([Waveform.whitenoise, Waveform.square], [1.0, 0.8], [1.0, 1.0], FilterName.lowpass, [1000], [0.001, 0.02, 0.0001, 0.1], 44100)
    #wave = synthesizer.setPitch(100,2)

    #HAT?
    #synthesizer = Synthesizer([Waveform.whitenoise], [1.0], [1.0], FilterName.highpass, [7000], [0.0, 0.02, 0.0001, 0.4], 44100)
    #wave = synthesizer.setPitch(100,2)

    #Synthe
    #synthesizer = Synthesizer([Waveform.sine, Waveform.sine], [1.0, 0.2], [1.0, 1.005], FilterName.bandpass, [500,5000], [0.01, 0.02, 0.9, 0.2], 44100)

    #Bass
    #synthesizer = Synthesizer([Waveform.sine, Waveform.sine], [1.0, 0.1], [1.0, 1.09], FilterName.bandpass, [2,2000], [0.01, 0.02, 0.6, 0.2], 44100)


    import time

    for i in range(2):
        wave = synthesizer.setPitch(100,2)
        dist = Distortion()
        delay = Delay()
        wave = dist.hardClipping(wave,2)
        wave = delay.delay(wave)
        o.write(synthesizer.toBytes(wave))
        time.sleep(0.1)
