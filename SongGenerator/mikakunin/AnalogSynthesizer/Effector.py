# coding:utf-8
#default
import numpy as np
import wave as wv
import wave as wv
import struct
import scipy.signal

from common import function as func

class Effector:
    def __init__(self):
        self._presetObject = Preset()
        self._setPresetName()

    def setBpm(self, bpm):
        self._bpm = bpm

    def _setPresetName(self):
        self.trueBypass = "trueBypass"
        self.comp = "comp"
        self.dist = "dist"
        self.tremolo = "tremolo"
        self.flanger = "flanger"
        self.reverb = "reverb"

    def Set(self, wave, presetName, **arg):
        if presetName == self.trueBypass:
            return wave
        elif presetName == self.comp:
            o = self._presetObject.Compressor(wave, arg["depth"])
            return o
        elif presetName == self.dist:
            o = self._presetObject.Distortion(wave, arg["gain"], arg["depth"])
            return o
        elif presetName == self.tremolo:
            o = self._presetObject.Tremolo(wave, arg["depth"], self._bpm)
            return o
        elif presetName == self.flanger:
            o = self._presetObject.Flanger(wave, arg["depth"], arg["freq"], arg["balance"])
            return o
        elif presetName == self.reverb:
            o = self._presetObject.Reverb(wave, arg["delay"], arg["amp"], arg["depth"])
            return o

class Preset:
    def Compressor(self, wave, depth = 2):
        wave =  Compressor.sigmoid(Compressor(), wave, depth)
        return wave

    def Distortion(self, wave, gain = 2, depth = 2):
        wave = Distortion.hardClipping(Distortion(), wave, gain)
        wave = Compressor.sigmoid(Compressor(), wave, depth)
        return wave

    def Tremolo(self, wave, depth = 1, bpm = 120):
        freq = 1/(60.0/bpm)
        wave = wave#self.Distortion(wave, gain = 0.01)
        wave = Tremolo.am(Tremolo(), wave, depth, freq)
        return wave

    def Flanger(self, wave, gain = 2, depth = 0.5, freq = 0.3, balance = 1.0):
        wave = self.Distortion(wave, gain = gain)
        wave_proc = Vibrato.sine(Vibrato(), wave, depth, freq)
        wave = func.add([wave, wave_proc], [1.0, balance])
        return wave

    def Reverb(self, wave, delay = 0.05, amp = 0.2, depth = 0.9):
        #wave = Delay.delay(Delay(), wave, 10000, 0.5, 1000)
        wave = Delay.reverb(Delay(), wave, delay, amp, depth)
        return wave

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
    def delay(self, wave, delay, amp, depth):
        delay = int(delay * 44100)
        wave_output = wave

        n = 0.0
        while depth**n > 0.00001:
            sirence = np.array([0]* delay * int(n) )
            if len(sirence) > len(wave):
                break
            else:
                wave_output = wave_output + np.r_[sirence, wave[0:int(len(wave)-delay * n)]*amp*(depth**n ) ]
                n += 1.0

        wave_output = wave_output/max(abs(wave_output)) if max(abs(wave_output)) > 0 else wave_output
        return wave_output

    def reverb(self, wave, delay_s, amp, depth):
        #delay = int(delay * 44100)
        wave_output = wave

        n = 0.0
        while depth**n > 0.00001:
            delay = int(np.random.normal(delay_s, delay_s/8) * 44100)
            sirence = np.array([0]* delay * int(n) )
            if len(sirence) > len(wave):
                break
            else:
                wave_output = wave_output + np.r_[sirence, wave[0:int(len(wave)-delay * n)]*amp*(depth**n ) ]
                n += 1.0

        wave_output = wave_output/max(abs(wave_output)) if max(abs(wave_output)) > 0 else wave_output
        return wave_output

    def _delay(self, data,frame=1500,amp=0.2,repeat=100):
        """
        ネットで拾ったやつ。未使用。
        """
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

class VolumeController():
    """
    tanh(2～3)≒1 →とりあえずの3
    """
    def ending(self, wave, len_sec):
        len_frame = int(len_sec *  44100)
        step = 3.0/len_frame
        x = np.arange(0, 3, step)
        x = x[::-1]
        curve = np.tanh(x)
        wave[-len(curve):len(wave)] = wave[-len(curve):len(wave)] * curve
        return wave


class Tremolo():
    '''
    参考：http://ism1000ch.hatenablog.com/
    member
        depth : 変調深度
        freq  : 変調周波数[hz]
        rate  : サンプリングレート[hz]
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

if __name__ == '__main__':
    fxObj = Effector()
    fxObj.setBpm(120)
    wave = np.arange(1000000)
    o = fxObj.Set(wave, "dist", **{"gain":2. ,"depth":2})
    print(len(o))
    o1 = fxObj.Set(wave, "comp", **{"depth":2})
    print(len(o1))
    o2 = fxObj.Set(wave, "tremolo", **{"depth":2})
    print(len(o2))
    o3 = fxObj.Set(wave, "flanger", **{"gain":3, "depth":2, "freq":0.3, "balance":1.0})
    print(len(o3))
