# coding:utf-8
#default
import numpy as np

#option
import wave as wv
import struct
import scipy.signal
import math
from enum import Enum

"""
TODO:
エフェクターっぽいのは消す。Effector.pyに移行。
"""

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
        if self._waveform == "sine":
            return np.sin(phases)
        elif self._waveform == "sawtooth":
            return scipy.signal.sawtooth(phases)
        elif self._waveform == "square":
            return scipy.signal.square(phases)
        #elif self._waveform == "gausspulse":
        #    return scipy.signal.gausspulse(phases)
        elif self._waveform == "whitenoise":
            wn = np.random.normal(0, 1, size=len(phases))
            threshold = 1.96
            for idx, val in enumerate(wn):
                if val > threshold:
                    wn[idx] = threshold
                elif -val >  threshold:
                    wn[idx] = -threshold
            wn = wn / max(np.absolute(wn)) if max(np.absolute(wn)) > 0 else wn
            return wn
        elif self._waveform == "sine_kick":
            return np.sin(phases)

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

    def _variabeFreq(self, frequency):
        return None

    def _wave_func(self, wave):

        if "bandpass" == self._filterName :
            b = self._bandPass(self._frequency)
        elif "bandcut" == self._filterName :
            b = self._bandCut(self._frequency)
        elif "lowpass" == self._filterName :
            b = self._lowPass(self._frequency[0])
        elif "highpass" == self._filterName :
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
                osc1_freq_transpose=1.0, \
                use_osc2=False,  \
                osc2_waveform=Waveform.sine, \
                osc2_volume=0.3, \
                osc2_freq_transpose=2.0, \
                rate=44100):

        self._osc1 = Oscillator(waveform=osc1_waveform, volume=osc1_volume, freq_transpose=osc1_freq_transpose)
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
        if isinstance(frequency, list):
            wave = self.gererate_shifted_wave(frequency, length)
            return wave

        else :
            phases = np.cumsum(2.0 * np.pi * frequency / self._rate * np.ones(int(self._rate * float(length))))
            return self._generate_wave(phases)

    def generate_unconstant_wave(self, frequency, length):

        phases = None
        sigma = np.random.normal(0, 1)
        for n in range( int(self._rate * float(length)) ):
            if phases is None :
                phases = [2.0 * np.pi * ( frequency+sigma) / self._rate]
            else :
                if n % 2000 == 0:
                    sigma = np.random.normal(0, 1)

                phases.append(phases[-1] + 2.0 * np.pi * ( frequency+sigma ) / self._rate)

        return self._generate_wave(phases)

    def gererate_shifted_wave(self, frequency, length):
        frame_n = int(self._rate * float(length))
        t = np.linspace(0, length, frame_n )
        w = scipy.signal.chirp(t, f0=frequency[0], f1=frequency[1], t1=length, method='linear')
        return w

    def _gererate_shifted_wave(self, frequency, length):
        """
        e^(-5) ≒ 0
        クリッピングしてる。サイズが極端に変わる
        """
        if frequency[0] > frequency[1] :
            freq_list = np.arange(frequency[0] , frequency[1], -1)
            len_list =  []
            for freq in freq_list :
                freq_proc = (freq - frequency[1]) / abs(frequency[0] - frequency[1])
                len_list.append(math.exp(-5 * freq_proc))

            len_list = np.array(len_list)
            len_list = len_list * length / np.sum(len_list)

            phases_pre = []
            for idx, freq in enumerate(freq_list):
                phases_pre.extend( 2.0 * np.pi * freq / self._rate * np.ones(int(self._rate * float(len_list[idx]))) )

            phases = np.cumsum(phases_pre)
            return self._generate_wave(phases)

        elif frequency[0] < frequency[1] :
            freq_list = np.arange(frequency[0] , frequency[1], 1)
            len_list =  []
            for freq in freq_list :
                freq_proc = (freq - frequency[0]) / abs(frequency[0] - frequency[1])
                len_list.append(math.exp( freq_proc - 5 ))

            len_list = np.array(len_list)
            len_list = len_list * length / np.sum(len_list)

            phases_pre = []
            for idx, freq in enumerate(freq_list):
                phases_pre.extend( 2.0 * np.pi * freq / self._rate * np.ones(int(self._rate * float(len_list[idx]))) )

            phases = np.cumsum(phases_pre)
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
#廃止予定。
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

class FilterController():
    def lowfi_stereo(self, wave, bpm, start = [0], end = [0], filterName = 'bandpass', filter = [[1000,6000]]):
        wave_r =  wave[1::2]
        wave_l = wave[0::2]

        start = np.array(start) * int(60 / bpm / 4 * 44100 )
        end = np.array(end) * int(60 / bpm / 4 * 44100 )

        for idx, s in enumerate(start):
            vcf = VCF(filterName, filter[idx], 44100)
            proc_wave_r = wave_r[start[idx]:end[idx]+1]
            proc_wave_l = wave_l[start[idx]:end[idx]+1]

            proc_wave_r = vcf.processing(proc_wave_r)
            proc_wave_l = vcf.processing(proc_wave_l)

            wave_r[start[idx] : start[idx] + len(proc_wave_r)] = proc_wave_r
            wave_l[start[idx] : start[idx] + len(proc_wave_l)] = proc_wave_l

            wave[1::2] = wave_r
            wave[0::2] = wave_l

        return wave

class VolumeController():
    def ending(self, wave, len_sec):
        len_frame = int(len_sec *  44100)
        step = 3.0/len_frame
        x = np.arange(0, 3, step)
        x = x[::-1]
        curve = np.tanh(x)
        wave[-len(curve):len(wave)] = wave[-len(curve):len(wave)] * curve
        return wave

    def sidechain(self, wave, bpm, sec_list_ctrl):
        max_frame  = int(60/bpm/2 *44100)
        bank = 4.0 #3～
        curve = np.full(0, 0.0)
        for hz, len_sec in sec_list_ctrl:
            if hz > 0 :
                len_frame = int(len_sec *  44100)
                if len_frame > 0 and len_frame <= max_frame :
                    step = (bank-0.0)/len_frame
                    x = np.arange(0.0, bank, step)
                    curve = np.r_[curve, np.tanh(x)]
                elif len_frame > max_frame :
                    step = (bank-0.0)/max_frame
                    x = np.arange(0.0, bank, step)
                    fix = np.full(len_frame - max_frame , 1.0)
                    curve = np.r_[curve, np.tanh(x), fix]
            else:
                len_frame = int(len_sec *  44100)
                curve = np.r_[curve, np.full(len_frame, 1.0)]

        if len(curve) < len(wave):
            fix = np.full((len(wave) - len(curve)), 1.0)
            curve = np.r_[curve, fix]
        elif len(curve) > len(wave):
            curve = curve[0:len(wave)]

        return wave * curve

    def sidechain_stereo(self, wave, bpm, sec_list_ctrl):
        """
        長さ変わらない
        """
        wave_r =  wave[1::2]
        wave_l = wave[0::2]

        max_frame  = int(60/bpm/2 *44100)
        bank = 4.0 #3～
        curve = np.full(0, 0.0)
        for hz, len_sec in sec_list_ctrl:
            if hz > 0 :
                len_frame = int(len_sec *  44100)
                if len_frame > 0 and len_frame <= max_frame :
                    step = (bank-0.0)/len_frame
                    x = np.arange(0.0, bank, step)
                    curve = np.r_[curve, np.tanh(x)]
                elif len_frame > max_frame :
                    step = (bank-0.0)/max_frame
                    x = np.arange(0.0, bank, step)
                    fix = np.full(len_frame - max_frame , 1.0)
                    curve = np.r_[curve, np.tanh(x), fix]
            else:
                len_frame = int(len_sec *  44100)
                curve = np.r_[curve, np.full(len_frame, 1.0)]

        if len(curve) < len(wave_r):
            fix = np.full((len(wave_r) - len(curve)), 1.0)
            curve = np.r_[curve, fix]
        elif len(curve) > len(wave_r):
            curve = curve[0:len(wave_r)]

        wave[1::2] = wave_r * curve
        wave[0::2] = wave_l * curve

        return wave

    def fourBeat_stereo(self, wave, bpm, start = [0], end = [0],  min = [2.0], max = [4.0]):
        """
        長さ変わらない
        """
        wave_r =  wave[1::2]
        wave_l = wave[0::2]

        volume = np.full(len(wave_r), 1.0)
        start = np.array(start) * int(60 / bpm / 4 * 44100 )
        end = np.array(end) * int(60 / bpm / 4 * 44100 )

        frame_len  = int(60/bpm * 44100)
        frame_n = int( (end -  start) / frame_len)
        curve = np.full(0, 0.0)

        for idx, s in enumerate(start):
            for n in range(frame_n):
                x = np.linspace(min[idx], max[idx], frame_len)
                curve = np.r_[curve, np.tanh(x)]
            volume[start[idx]:start[idx] + len(curve)] = curve

        wave[1::2] = wave_r * volume
        wave[0::2] = wave_l * volume

        return wave

    def fourBeat(self, wave, bpm, start = [0], end = [0],  min = [2.0], max = [4.0]):
        """
        長さ変わらない
        """
        volume = np.full(len(wave), 1.0)
        start = np.array(start) * int(60 / bpm / 4 * 44100 )
        end = np.array(end) * int(60 / bpm / 4 * 44100 )

        frame_len  = int(60/bpm * 44100)
        frame_n = int( (end -  start) / frame_len)
        curve = np.full(0, 0.0)

        for idx, s in enumerate(start):
            for n in range(frame_n):
                x = np.linspace(min[idx], max[idx], frame_len)
                curve = np.r_[curve, np.tanh(x)]
            volume[start:start + len(curve)] = curve

        return wave * volume

    def feedIn(self, wave, bpm, start = [0], end = [0], depth = [0.0]): #depth must be lower than 1
        """
        長さ変わらない
        """
        volume = np.full(len(wave), 1.0)
        start = np.array(start) * int(60 / bpm / 4 * 44100 )
        end = np.array(end) * int(60 / bpm / 4 * 44100 )

        for idx, s in enumerate(start):
            curve = np.full(( end[idx] - start[idx] + 1) , 0.0)
            step = len(curve) * ( 1.0 - depth[idx] )
            x = np.linspace(0.0, 3.0, num = step)
            tan_curve = np.tanh(x)
            curve[-len(tan_curve) : len(curve)] = tan_curve
            volume[start[idx]:end[idx]+1] = curve

        return wave * volume

    def feedIn2(self, wave, bpm, start = [0], end = [0], depth = [0.0]): #depth must be lower than 1
        """
        長さ変わらない
        """
        volume = np.full(len(wave), 1.0)
        start = np.array(start) * int(60 / bpm / 4 * 44100 )
        end = np.array(end) * int(60 / bpm / 4 * 44100 )

        for idx, s in enumerate(start):
            curve = np.full(( end[idx] - start[idx] + 1) , 0.0)
            step = len(curve) * ( 1.0 - depth[idx] )
            x = np.linspace(0.0, 1.0, num = step)
            curve[-len(x) : len(curve)] = x
            volume[start[idx]:end[idx]+1] = curve

        return wave * volume

    def feedIn_stereo(self, wave, bpm, start = [0], end = [0], type = ['tanh'], depth = [0.0]):
        wave_r =  wave[1::2]
        wave_l = wave[0::2]

        volume = np.full(len(wave_r), 1.0)
        start = np.array(start) * int(60 / bpm / 4 * 44100 )
        end = np.array(end) * int(60 / bpm / 4 * 44100 )

        for idx, s in enumerate(start):
            curve = np.full(( end[idx] - start[idx] + 1) , 0.0)
            step = len(curve) * ( 1.0 - depth[idx] )

            if type[idx] == 'liner':
                x = np.linspace(0.0, 1.0, num = step)
                curve[-len(x) : len(curve)] = x

            elif type[idx] == 'tanh':
                x = np.linspace(0.0, 3.0, num = step)
                curve[-len(x) : len(curve)] = np.tanh(x)

            volume[start[idx]:end[idx]+1] = curve

        wave[1::2] = wave_r * volume
        wave[0::2] = wave_l * volume

        return wave

    def feedOut_stereo(self, wave, bpm, start = [0], end = [0], type = ['tanh'], depth = [0.0]):
        wave_r =  wave[1::2]
        wave_l = wave[0::2]

        volume = np.full(len(wave_r), 1.0)
        start = np.array(start) * int(60 / bpm / 4 * 44100 )
        end = np.array(end) * int(60 / bpm / 4 * 44100 )

        for idx, s in enumerate(start):
            curve = np.full(( end[idx] - start[idx] + 1) , 0.0)
            step = len(curve) * ( 1.0 - depth[idx] )

            if type[idx] == 'liner':
                x = np.linspace(0.0, 1.0, num = step)
                curve[-len(x) : len(curve)] = x

            elif type[idx] == 'tanh':
                x = np.linspace(0.0, 3.0, num = step)
                curve[-len(x) : len(curve)] = np.tanh(x)

            volume[start[idx]:end[idx]+1] = curve[::-1]

        wave[1::2] = wave_r * volume
        wave[0::2] = wave_l * volume

        return wave

    def deepSidechain(self, wave, bpm, sec_list_ctrl, min = 2.0, max = 4.0):
        max_frame  = int(60/bpm *44100)
        bank = max #3～
        minVol = min
        curve = np.full(0, 0.0)
        for hz, len_sec in sec_list_ctrl:
            len_frame = int(len_sec *  44100)
            if len_frame > 0 and len_frame <= max_frame :
                step = (bank-minVol)/len_frame
                x = np.arange(minVol, bank, step)
                curve = np.r_[curve, np.tanh(x)]
            elif len_frame > max_frame :
                step = (bank-minVol)/max_frame
                x = np.arange(minVol, bank, step)
                fix = np.full(len_frame - max_frame , 1.0)
                curve = np.r_[curve, np.tanh(x)]

        if len(curve) < len(wave):
            fix = np.full((len(wave) - len(curve)), 1.0)
            curve = np.r_[curve, fix]
        elif len(curve) > len(wave):
            curve = curve[0:len(wave)]

        return wave * curve

    def _fourBeat(self, wave, bpm, min = 2.0, max = 4.0): #old
        frame_len  = int(60/bpm *44100)
        frame_n = int(len(wave) / frame_len)
        curve = np.full(0, 0.0)

        for n in range(frame_n):
            step = (max-min)/frame_len
            x = np.arange(min, max, step)
            curve = np.r_[curve, np.tanh(x)]

        if len(curve) < len(wave):
            fix = np.full((len(wave) - len(curve)), 1.0)
            curve = np.r_[curve, fix]
        elif len(curve) > len(wave):
            curve = curve[0:len(wave)]

        return wave * curve

class Tremolo():
    '''
    参考：http://ism1000ch.hatenablog.com/
    member
        depth : 変調深度
        freq  : 変調周波数[hz]
        rate  : サンプリングレート[hz]v
        n     : 現在フレーム
    '''

    def am(self, data, depth=0.2, freq=2, rate=44100):
        self.depth = depth
        self.freq  = freq
        self.rate  = rate
        self.n     = 0

        vfunc = np.vectorize(self.effect)
        return vfunc(data)

    def effect(self,d):
        d = d * (1.0 + self.depth * np.sin(self.n * ( 2 * np.pi * self.freq / self.rate)))
        self.n += 1
        return d


class Vibrato():
    '''
    参考：http://ism1000ch.hatenablog.com/
    member
        depth : 変調具合[frame]
        freq  : 変調周波数[hz]
        rate  : サンプリングレート[hz]
        n     : 現在フレーム[frame]
    '''

    def sine(self, data, depth=1, freq=1, rate=44100):
        self.n = 0
        self.depth = int(rate * depth / 1000) # input:[ms]
        self.freq  = freq
        self.rate  = rate

        # 時間軸をゆがめる
        frames = self.calc_frames(np.arange(data.size))

        # 対応するシグナルを線形補完する
        data = self.calc_signal(frames,data)
        return data

    def random(self, data, depth=1, rate = 44100):
        """
        あんま意味ない
        """
        self.rate  = rate
        self.depth = int(rate * depth / 1000)
        frames = self.calc_random_frames(data)

        # 対応するシグナルを線形補完する
        data = self.calc_signal(frames, data)
        return data

    # 時間軸をゆがめる. N(n)の計算
    # input  : 時間軸[ 0,   1,   2, 3,..]
    # output : 時間軸[ 0, 0.5, 2.5, 3,..]
    def calc_frames(self,frames):
        vfunc = np.vectorize(self.calc_frame)
        return vfunc(frames)
        #return frames

    def calc_frame(self,n):
        # n = n ~ n + 2*depth
        n = n + self.depth * (1 + np.sin(self.n * (2 * np.pi * self.freq / self.rate)))
        self.n += 1
        return n

    # N(n)を与え，線形補完してy(n)を計算
    def calc_signal(self,frames,data):
        # frames: N(n)のリスト
        # framesのlimit番目以降に対し処理を行う
        limit = self.depth * 2

        #indexオーバー対策
        frames_int = np.array(frames, dtype = 'int')
        frameList = np.where(frames_int < len(data)-2)

        calc_data = [self.calc_interp(frame,data) for frame in frames[limit:np.max(frameList)]]
        calc_data = np.hstack([data[:limit],calc_data])
        return np.array(calc_data)

    def calc_interp(self,frame,data):
        x = int(np.floor(frame))
        d = np.interp(frame,[x,x+1],data[x:x+2]) #indexオーバーする可能性アリ
        return d

    def calc_random_frames(self, data):
        frames = np.arange(len(data))
        rand_float = 1/2 - np.random.rand(len(data))
        frames = frames + rand_float
        frames[-1] = len(frames) -1 #最後のやつは固定
        return frames

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
            self._vco = VCO(self._waveform[0], self._volume[0], self._freqtranspose[0], True, self._waveform[1], self._volume[1], self._freqtranspose[1], self._rate)
        else :
            self._vco = VCO(self._waveform[0], self._volume[0], self._freqtranspose[0], False, self._rate)

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

class Synthesizer_Poly():
    def __init__(self, waveform, volume, freqtranspose, filterName, frequency ,adsr, rate):
        self._waveform = waveform #[seine, saw]
        self._volume = volume #[1,0.3]
        self._freqtranspose = freqtranspose #[1,1]
        self._filterName = filterName #lowpass
        self._frequency = frequency #[100,1000]
        self._adsr = adsr #[0.001, 0.02, 0.6, 0.02]
        self._rate = rate #44100

        self._vcos = []
        for idx, wf in enumerate(self._waveform):
            self._vcos.append(VCO(wf, self._volume[idx], self._freqtranspose[idx], False, self._rate))

        self._vcf = VCF(self._filterName, self._frequency, self._rate)
        self._vca = VCA(self._adsr[0], self._adsr[1], self._adsr[2], self._adsr[3], self._rate)
        self._amp = Amp()

    def setPitch(self, frequency, length):
        buf = None
        for vco in self._vcos:
            if buf is None:
                buf = vco.generate_unconstant_wave(frequency, length) #length is sec
            else :
                buf += vco.generate_unconstant_wave(frequency, length)

        buf = self._vcf.processing(buf)
        buf = self._vca.processing(buf)
        buf = self._amp.maxStd(buf)
        return buf

    def soundless(self, length):
        return np.zeros(int(length * self._rate), dtype = 'float')

    def toBytes(self, wave):
        return (wave * float(2 ** (16 - 1) ) ).astype(np.int16).tobytes()

if __name__ == '__main__' :
    import pyaudio
    import Effector as fx


    def add(wav_list, w_list):
        len_list = []
        for np_a in wav_list:
            len_list.append(len(np_a))

        length = np.min(np.array(len_list))

        wave = np.zeros(length)
        for idx, np_a in enumerate(wav_list):
            wave = wave + np_a[0:length] * w_list[idx]

        return wave/sum(w_list)

    preset = fx.Preset()
    audio  = pyaudio.PyAudio()
    o = audio.open(format=audio.get_format_from_width(2),
                                channels=1,
                                rate=44100,
                                output=True)

    #いい感じ electro piano
    #synthesizer = Synthesizer_Poly(['sawtooth', 'sine', 'sine', 'sine', 'sine', 'sine', 'sine'], [0.07, 2.0, 0.9, 1.4, 0.2, 1.2, 0.2], [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'highpass', [180], [0.01, 0.05, 0.0, 0.0], 44100)

    #悪くはないがなんの音
    #synthesizer = Synthesizer_Poly(['sine', 'sine', 'sawtooth', 'sawtooth', 'square', 'square', 'whitenoise'], [0.1, 2.0, 0.9, 0.8, 0.2, 0.2, 0.9], [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'bandcut', [3000, 10000], [0.05, 0.18, 0.2, 0.0], 44100)

    #electro piano
    #synthesizer = Synthesizer_Poly(['sawtooth', 'square', 'sine', 'sine', 'sine', 'sawtooth', 'sawtooth'], [0.7, 1.0, 0.9, 0.8, 0.4, 0.4, 0.4], [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'lowpass', [5000], [0.0, 0.25, 0.0, 0.0], 44100)

    #Drawer Piano
    #synthesizer = Synthesizer_Poly(['sine', 'sine', 'sine', 'sine', 'sine', 'sine', 'sine'], [1.0, 1.0, 0.2, 0.4, 0.4, 0.4, 0.8], [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'lowpass', [15000], [0.02, 0.3, 0.9, 0.01], 44100)
    #wave = preset.Distortion(wave, 3, 5)

    #Church Organ?
    #synthesizer = Synthesizer_Poly(['sine', 'sawtooth', 'sine', 'square', 'square', 'square', 'square'], [1.0, 1.0, 0.2, 0.4, 0.4, 0.4, 0.8], [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'bandpass', [500,10000], [0.02, 0.005, 0.9, 0.01], 44100)

    #金管っぽいなにか
    #synthesizer = Synthesizer_Poly(["sawtooth", "sawtooth", "sawtooth", "sine"], [0.2, 2.0,  0.1, 0.9], [0.5, 1.0, 2.0, 3.001], 'bandpass', [600,8000], [0.03, 0.02, 0.6, 0.01], 44100)

    #バッキングに使えそう
    #synthesizer = Synthesizer_Poly(['sine', 'sine', 'sine', 'sawtooth', 'sawtooth', 'sawtooth', 'whitenoise'], [0.7, 1.0, 0.9, 0.8, 0.8, 0.8, 1.2], [1.001, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'lowpass', [2000], [0.0, 0.4, 0.1, 0.0], 44100)


    #リード用（鍵盤っぽい）
    #synthesizer = Synthesizer_Poly(["sawtooth", "square", "sine", "sine", "sine", "sawtooth", "sawtooth"], [0.5, 1.0, 0.2, 0.1, 0.1, 0.2, 0.2], [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'bandpass', [500,13000], [0.1, 0.001, 0.0, 0.1], 44100)

    #
    #synthesizer = Synthesizer_Poly(["sine", "sine", "sine", "sine", "whitenoise"], [0.05, 1.4, 0.8, 0.8, 0.5], [0.5, 1.0, 2.0, 3.0, 1.0], 'lowpass', [600], [0.05, 0.1, 0.8, 0.02], 44100)
    #synthesizer2 = Synthesizer_Poly([ "sine", "sine", "sine", "sawtooth", "sine"], [0.8, 0.4, 0.4, 0.4, 0.4], [ 4.0, 5.0, 6.0, 7.01, 7.992], 'lowpass', [600], [0.1, 0.1, 0.8, 0.02], 4410)

    #synthesizer = Synthesizer(["sine", "sine"], [1.0, 0.8], [1.0, 1.0], 'lowpass', [200], [0.0, 0.04, 0.3, 0.1], 44100)

    #guitar
    synthesizer = Synthesizer_Poly(["square", "square", "square", "sine", "sine", "whitenoise"], [0.8, 0.2, 0.1, 0.2, 0.2, 0.3], [1.0, 2.0, 3.0, 4.01, 5.01, 6.0], 'bandpass', [10,18000], [0.02, 0.15, 0.9, 0.1], 44100)

    scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25] * 1
    #scale = [261.63/4] * 16
    #scale = [[60, 2], [60, 2], [60, 2], [60, 2]]

    wave = np.full(0, 0.0)
    for note in scale:
        wave = np.r_[wave, synthesizer.setPitch(note,0.5)]
    #scale2 = [261.63 * 1.5/4 , 293.66 * 1.5/4,   329.63 * 1.5/4,  349.23 * 1.5/4, 392.00 * 1.5/4, 440.00 * 1.5/4, 493.88 * 1.5/4, 523.25 * 1.5/4] * 1

    #scale2 = [261.63*1.5/4] * 16

    #wave2 = np.full(0, 0.0)
    #for note in scale2:
    #    wave2 = np.r_[wave2, synthesizer.setPitch(note,0.2)]

    #wave = add([wave, wave2], [1.0, 1.0])



    #wave = preset.Distortion(wave, 5, 3)
    wave = preset.Filter(wave, 'bandpass', [200, 15000])

    swave = preset.Flanger(wave,  gain = 4, depth = 2.0, freq = 0.8, balance = 1.0)
    #wave = preset.Vibrato(wave, 1.0, 1.7)
    #wave = (wave[0:44100*20] + bass_wave[0:44100*20]) / 2
    #wave = preset.Radio(wave, 0.2)
    #wave = preset.Tape(wave, 0.1, 1.4)
    wave = preset.Reverb(wave, 0.05, 0.2, 0.8)


    wave_bin = (wave * float(2 ** (16 - 2) ) ).astype(np.int16).tobytes()
    o.write(wave_bin)
    #SNARE?
    #synthesizer = Synthesizer([Waveform.whitenoise, Waveform.square], [1.0, 0.8], [1.0, 1.0], FilterName.lowpass, [3000], [0.001, 0.02, 0.0001, 0.1], 44100)
    #wave = synthesizer.setPitch(150,2)

    #KICK?
    #synthesizer = Synthesizer([Waveform.whitenoise, Waveform.square], [1.0, 0.8], [1.0, 1.0], FilterName.lowpass, [1000], [0.001, 0.02, 0.0001, 0.1], 44100)
    #wave = synthesizer.setPitch(100,2)
    #vcoObj = VCO('sine', 1, False, 44100)
    #wave = vcoObj.gererate_shifted_wave([100,10], 1)

    #HAT?
    #synthesizer = Synthesizer([Waveform.whitenoise], [1.0], [1.0], FilterName.highpass, [7000], [0.0, 0.02, 0.0001, 0.4], 44100)
    #wave = synthesizer.setPitch(100,2)

    #Synthe
    #synthesizer = Synthesizer([Waveform.sine, Waveform.sine], [1.0, 0.2], [1.0, 1.005], FilterName.bandpass, [500,5000], [0.01, 0.02, 0.9, 0.2], 44100)

    #Bass
    #synthesizer = Synthesizer([Waveform.sine, Waveform.sine], [1.0, 0.1], [1.0, 1.09], FilterName.bandpass, [2,2000], [0.01, 0.02, 0.6, 0.2], 44100)


    #import time

    #for i in range(2):
    #    wave = synthesizer.setPitch(100,2)

    #    wave = delay.delay(wave)
    #    o.write(synthesizer.toBytes(wave))
    #    time.sleep(0.1)

if __name__ == '__main2__' :
    import pyaudio
    import Effector as fx

    def add_stereo(wav_list, w_list):

        min_len = None
        for w in wav_list :
            if min_len is None :
                min_len = len(w)
            else :
                if min_len > len(w):
                    min_len = len(w)

        wave_r = np.zeros(min_len)
        wave_l = np.zeros(min_len)
        wave = np.zeros(min_len*2)

        for idx, w in enumerate(wav_list):
            wave_r += w[0:min_len] * w_list[idx]['vol'] * w_list[idx]['r']  / (w_list[idx]['r'] + w_list[idx]['l'])
            wave_l += w[0:min_len] * w_list[idx]['vol'] * w_list[idx]['l']  / (w_list[idx]['r'] + w_list[idx]['l'])

        wave_r = wave_r / max(np.abs(wave_r)) if max(np.abs(wave_r)) > 0 else wave_r
        wave_l = wave_l / max(np.abs(wave_l)) if max(np.abs(wave_l)) > 0 else wave_l

        wave[1::2] = wave_r
        wave[0::2] = wave_l

        return wave

    def add(wav_list, w_list):
        len_list = []
        for np_a in wav_list:
            len_list.append(len(np_a))

        length = np.min(np.array(len_list))

        wave = np.zeros(length)
        for idx, np_a in enumerate(wav_list):
            wave = wave + np_a[0:length] * w_list[idx]

        return wave/sum(w_list)

    preset = fx.Preset()
    audio  = pyaudio.PyAudio()
    o = audio.open(format=audio.get_format_from_width(2),
                                channels=1,
                                rate=44100,
                                output=True)


    #リード用（鍵盤っぽい）
    synthesizer = Synthesizer_Poly(["sawtooth", "sawtooth", "sine", "sine", "sine", "sawtooth", "sawtooth"], [0.05, 1.0, 0.2, 0.1, 0.1, 0.2, 0.2], [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 'bandpass', [300,10000], [0.0, 0.001, 0.01, 0.02], 44100)


    scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25] * 4

    wave = np.full(0, 0.0)
    for note in scale:
        wave = np.r_[wave, synthesizer.setPitch(note,0.5)]

    #vol = VolumeController()
    #wave = vol.feedIn2(wave, 120, [0], [4*8*3-1], [0.3])

    wave = add_stereo([wave, wave],[{"vol": 1.0, "r":0.8, "l":0.2}, {"vol": 1.0, "r":0.8, "l":0.2}])
    fil = FilterController()
    wave = fil.lowfi_stereo(wave, 120,  [0], [4*8*3-1]  ,'bandpass' ,[[3000,10000]])


    wave_bin = (wave * float(2 ** (16 - 2) ) ).astype(np.int16).tobytes()
    o.write(wave_bin)
