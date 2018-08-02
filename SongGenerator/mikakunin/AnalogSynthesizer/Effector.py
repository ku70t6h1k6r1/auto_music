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
        self.dist2 = "dist2"
        self.dist3 = "dist3"
        self.tremolo = "tremolo"
        self.vibrato = "vibrato"
        self.flanger = "flanger"
        self.reverb = "reverb"
        self.radio = "radio"
        self.wahwah = "wahwah"
        self.tape = "tape"

    def Set(self, wave, presetName, **arg):
        if presetName == self.trueBypass:
            return wave
        elif presetName == self.comp:
            o = self._presetObject.Compressor(wave, arg["depth"])
            return o
        elif presetName == self.dist:
            o = self._presetObject.Distortion(wave, arg["gain"], arg["depth"])
            return o
        elif presetName == self.dist2:
            o = self._presetObject.Distortion2(wave, arg["gain"], arg["depth"], arg["freq"])
            return o
        elif presetName == self.dist3:
            o = self._presetObject.Distortion3(wave, arg["gain"], arg["depth"])
            return o
        elif presetName == self.tremolo:
            o = self._presetObject.Tremolo(wave, arg["depth"], self._bpm)
            return o
        elif presetName == self.vibrato:
            o = self._presetObject.Vibrato(wave, arg["depth"], arg["freq"])
            return o
        elif presetName == self.flanger:
            o = self._presetObject.Flanger(wave, arg["depth"], arg["freq"], arg["balance"])
            return o
        elif presetName == self.reverb:
            o = self._presetObject.Reverb(wave, arg["delay"], arg["amp"], arg["depth"])
            return o
        elif presetName == self.radio:
            o = self._presetObject.Radio(wave, arg["gain"], arg["depth_pitch"], arg["freq_pitch"], arg["depth_vol"], arg["freq_vol"])
            return o
        elif presetName == self.wahwah:
            o = self._presetObject.Distortion(wave, 2, 0.6)
            o = self._presetObject.Wahwah(wave)
            return o
        elif presetName == self.tape: #self, data, depth=1, freq_mirco=2.0, freq_marco=0.1, rate = 44100
            o = self._presetObject.Tape(wave, arg["gain"], arg["depth"])
            return o

class Preset:
    def Compressor(self, wave, depth = 2):
        wave =  Compressor.sigmoid(Compressor(), wave, depth)
        return wave

    def Distortion(self, wave, gain = 2, depth = 2):
        wave = Distortion.hardClipping(Distortion(), wave, gain)
        wave = Compressor.sigmoid(Compressor(), wave, depth)
        return wave

    def _Distortion2(self, wave, gain = 3, depth = 0.5):
        """
        ギターの音と合わせたら声みたいに
        demo20180730_Test_settingTest_20180730_133__20180730_170252.wav
        """
        wave = Distortion.hardClipping(Distortion(), wave, gain)
        wave = Compressor.sigmoid(Compressor(), wave, depth)
        filter = Filter('bandpass', [50, 1000])
        wave = Delay.reverb(Delay(), wave, 0.05, 0.6, 0.97)
        wave = filter.processing(wave)
        return wave

    def Distortion2(self, wave, gain = 3, depth = 0.5, freq = [300,1000] ):
        wave = Distortion.hardClipping(Distortion(), wave, gain)
        wave = Compressor.sigmoid(Compressor(), wave, depth)
        filter = Filter('bandpass', freq)
        wave = Delay.reverb(Delay(), wave, 0.07, 0.9, 0.6)
        wave = filter.processing(wave)
        return wave

    def Distortion3(self, wave, gain = 2, depth = 2):
        wave = Distortion.hardClipping(Distortion(), wave, gain)
        wave = Compressor.sigmoid(Compressor(), wave, depth)
        #filter = Filter('bandpass', [10,10000])
        wave = Delay.reverb(Delay(), wave, 0.01, 0.3, 0.3)
        wave = Tremolo.am(Tremolo(), wave, depth=1, freq=5.0, rate=44100)
        #wave = filter.processing(wave)
        return wave

    def Filter(self, wave, filterName = 'bandpass', freqs = [18, 12000]):
        filter = Filter(filterName, freqs)
        wave = filter.processing(wave)
        return wave

    def Tremolo(self, wave, depth = 1, bpm = 120):
        freq = 1/(60.0/bpm)
        wave = wave#self.Distortion(wave, gain = 0.01)
        wave = Tremolo.am(Tremolo(), wave, depth, freq)
        return wave

    def Vibrato(self, wave, depth = 1, freq = 1):
        wave = self.Distortion(wave, gain = 2)
        wave = Vibrato.sine(Vibrato(), wave, depth, freq)
        return wave

    def Flanger(self, wave, gain = 2, depth = 0.5, freq = 0.3, balance = 1.0):
        wave = self.Distortion(wave, gain = gain)
        wave_proc = Vibrato.sine(Vibrato(), wave, depth, freq)
        wave = func.add([wave, wave_proc], [1.0, balance])
        return wave

    def Reverb(self, wave, delay = 0.05, amp = 0.2, depth = 0.2):
        #wave = Delay.delay(Delay(), wave, 10000, 0.5, 1000)
        wave = Delay.reverb(Delay(), wave, delay, amp, depth)
        return wave

    def old_Radio(self, wave, gain = 1):
        wave = Distortion.hardClipping(Distortion(), wave, gain)
        wave = Vibrato.sine(Vibrato(), wave, depth=2.3, freq=0.7, rate=44100)
        wave = Tremolo.am(Tremolo(), wave, depth=0.4, freq=3.0, rate=44100)
        filter = Filter('bandpass', [20,6000])
        wave = Delay.reverb(Delay(), wave, 0.05, 0.6, 0.82)
        wave = filter.processing(wave)
        return wave

    def Radio(self, wave, gain = 1, depth_pitch = 2.3, freq_pitch = 0.3, depth_vol = 0.4, freq_vol = 5.0):
        wave = Distortion.hardClipping(Distortion(), wave, gain)
        #filter = Filter('bandpass', [100,9000])
        filter = Filter('bandpass', [100,9000])
        wave = Delay.reverb(Delay(), wave, 0.05, 0.8, 0.9)
        wave = filter.processing(wave)
        wave = Vibrato.random(Vibrato(), wave, depth=depth_pitch, freq= freq_pitch, rate=44100)
        wave = Tremolo.am_random(Tremolo(), wave, depth=depth_vol, freq=freq_vol, rate=44100)
        return wave

    def Wahwah(self, wave):
        wave = Wahwah.sine(Wahwah(), wave)
        wave = Delay.reverb(Delay(), wave, delay_s = 0.01, amp = 0.9, depth = 0.4)
        return wave

    def Tape(self, wave, gain = 1, depth = 1):
        wave = Tape.pitch(Tape(), wave, depth=0.23, freq_mirco=0.2, freq_marco=0.3)
        wave = self.Distortion(wave, gain, depth)
        wave = Tape.volume(Tape(), wave, depth=0.032, freq_mirco=0.3, freq_marco=1.0)
        wave = Delay.reverb(Delay(), wave, 0.06, 0.1, 0.9)
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

class Wahwah():
    def multiWaveForm(self, wave, waveForm, chunk = 0.01):
        """
        chunkの大きさは？ 0.01暗いが程よい
        各種調整がむずい。
        """
        self.n = 0

        chunk = int(chunk * 44100)
        window_n =  int(len(wave) / chunk) #あまり分の処理。

        # 時間軸をゆがめる
        frames = self.calc_frames(np.arange(window_n), waveForm)

        o = np.zeros(0)
        for n in range(window_n):
            # 0 < frame < 2
            low = 1 + frames[n] * 1000
            high = low + 3500
            filter = Filter('bandpass', [low,high])
            wave_proc = wave[n*chunk:(n+1)*chunk]
            wave_proc = filter.processing(wave_proc)
            wave[n*chunk : n*chunk+len(wave_proc)] = wave_proc
            #o = np.r_[o, wave_proc]

        return wave


    def sine(self, wave, chunk = 0.01):
        """
        chunkの大きさは？ 0.01暗いが程よい
        各種調整がむずい。
        """
        self.n = 0

        chunk = int(chunk * 44100)
        window_n =  int(len(wave) / chunk) #あまり分の処理。

        # 時間軸をゆがめる
        frames = self.calc_frames(np.arange(window_n))

        o = np.zeros(0)
        for n in range(window_n):
            # 0 < frame < 2
            low = 1 + frames[n] * 1000
            high = low + 3500
            filter = Filter('bandpass', [low,high])
            wave_proc = wave[n*chunk:(n+1)*chunk]
            wave_proc = filter.processing(wave_proc)
            wave[n*chunk : n*chunk+len(wave_proc)] = wave_proc
            #o = np.r_[o, wave_proc]

        return wave

    def calc_frames(self, frames, waveForm):
        if waveForm == 'sine' or waveForm == 'square' or waveForm == 'sawtooth' :
            vfunc = np.vectorize(self.sine_frame)
            return vfunc(frames)

        elif waveForm == 'chirp':
            return None

    def sine_frame(self,n):
        # n = n ~ n + 2*depth
        n =   (1 + np.sin(self.n * (2 * np.pi * 0.001 )))
        self.n += 1
        return n

    def calc_frames_chirp(self, frames):

        return n

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



class Tape():
    def pitch(self, data, depth=1, freq_mirco=2.0, freq_marco=0.1, rate = 44100):
        #self.n = 0 なんか変なバグが、、、未使用
        self.n_macro = 0 #np.random.randint(44100*10)
        self.depth = int(rate * depth / 1000) # input:[ms]
        self.freq_macro  = freq_marco
        self.freq_micro  = freq_mirco
        self.rate  = rate

        #Freq のリストを作る。
        self.freqs = self.calc_framesFreq(np.full(data.size, self.freq_micro, dtype = float))

        # 時間軸をゆがめる
        frames = self.calc_frames(np.arange(data.size))

        # 対応するシグナルを線形補完する
        data = np.array(self.calc_signal(frames,data))
        data = data / np.max(abs(data)) if np.max(abs(data)) > 0  else data
        return data

    def volume(self, data, depth=0.1, freq_mirco=2.0, freq_marco=0.1, rate = 44100):
        self.n = -1
        self.n_macro_vol = 0 #np.random.randint(44100*10)
        self.depth = int(rate * depth / 1000) # input:[ms]
        self.freq_macro_vol  = freq_marco
        self.freq_micro_vol  = freq_mirco
        self.rate  = rate

        #Freq のリストを作る。
        self.freqs_vol = self.calc_framesFreq_vol(np.full(data.size, self.freq_micro_vol, dtype = float))

        # 時間軸をゆがめる
        data = self.calc_frames_vol(data)

        return data

    def calc_frames(self,frames):
        vfunc = np.vectorize(self.calc_frame)
        return vfunc(frames)

    def calc_frame(self, n):
        # 60cent が標準のVib 100セントが半音　半音は50～100Hz
        #sigma = (1 - 2 * np.random.random() ) * self.freq_micro * 0.0 #決め打ち
        # Micro
        n = n + self.depth * (1 + np.sin(n * (2 * np.pi * (self.freqs[n] + 0.0) / self.rate)))
        return n

    def calc_frames_vol(self,data):
        vfunc = np.vectorize(self.calc_frame_vol)
        return vfunc(data)

    def calc_frame_vol(self, d):
        #d = d * (1.0 + self.depth * np.sin(self.n * ( 2 * np.pi * self.freq / self.rate)))
        d = d *  (1.0 + self.depth * np.sin(self.n * (2 * np.pi * (self.freqs_vol[self.n]) / self.rate)))
        #d = d * 0.4
        self.n += 1
        return d

    def calc_framesFreq(self,freqs):
        vfunc = np.vectorize(self.calc_microFreq)
        return vfunc(freqs)
        #return frames

    def calc_microFreq(self, freq):
        # Macro
        #sigma = (1 - 2 * np.random.random() ) * self.freq_macro * 0.0 #決め打ち
        freq = freq + freq * 0.6 * np.sin(self.n_macro * (2 * np.pi * (self.freq_macro + 0.0) / self.rate)) #0.2決め打ち
        self.n_macro  += 1
        return freq

    def calc_framesFreq_vol(self,freqs):
        vfunc = np.vectorize(self.calc_microFreq_vol)
        return vfunc(freqs)
        #return frames

    def calc_microFreq_vol(self, freq):
        # Macro
        #sigma = (1 - 2 * np.random.random() ) * self.freq_macro * 0.0 #決め打ち
        freq = freq + freq * 0.6 * np.sin(self.n_macro_vol * (2 * np.pi * (self.freq_macro_vol + 0.0) / self.rate)) #0.2決め打ち
        self.n_macro_vol  += 1
        return freq

    # N(n)を与え，線形補完してy(n)を計算
    def calc_signal(self,frames,data):
        # frames: N(n)のリスト
        # framesのlimit番目以降に対し処理を行う
        limit = self.depth * 2

        #indexオーバー対策
        frames_int = np.array(frames, dtype = 'int')
        frameIdx_List = np.where(frames_int < len(data)-2)

        #framesDiff = np.diff(frames)
        #minus = np.where(framesDiff < 0)
        #print("314", len(minus[0]))

        calc_data = [self.calc_interp(frame,data) for frame in frames[limit:np.max(frameIdx_List)]]
        calc_data = np.hstack([data[:limit],calc_data])
        return np.array(calc_data)

    def calc_interp(self,frame,data):
        x = int(np.floor(frame))
        d = np.interp(frame,[x,x+1],data[x:x+2]) #indexオーバーする可能性アリ
        return d

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

    def am_random(self, data, depth=0.2, freq=2, rate=44100):
        self.depth = depth
        self.freq  = freq
        self.rate  = rate
        self.n     = np.random.randint(44100*10)

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
    def random(self, data, depth=1, freq=1, rate = 44100):
        self.n = np.random.randint(44100*10)
        self.depth = int(rate * depth / 1000) # input:[ms]
        self.freq  = freq
        self.rate  = rate

        # 時間軸をゆがめる
        frames = self.calc_frames(np.arange(data.size))

        # 対応するシグナルを線形補完する
        data = self.calc_signal(frames,data)
        return data


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

class Filter():
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
