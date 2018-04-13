# coding: UTF-8
import numpy as np
import pyaudio
import wave
import sys
import math

CHUNK = 512

def find_peaks(a, amp_thre, local_width=1, min_peak_distance=1):
    """
    閾値と極大・極小を判定する窓幅、ピーク間最小距離を与えて配列からピークを検出する。
    内部的にはピーク間距離は正負で区別して算出されるため、近接した正負のピークは検出される。
    :rtype (int, float)
    :return tuple (ndarray of peak indices, ndarray of peak value)
    """
    # generate candidate indices to limit by threthold
    idxs = np.where(np.abs(a) > amp_thre)[0]

    # extend array to decide local maxima/minimum
    idxs_with_offset = idxs + local_width
    a_extend = np.r_[[a[0]] * local_width, a, [a[-1]] * local_width]

    last_pos_peak_idx = 0
    last_neg_peak_idx = 0
    result_idxs = []

    for i in idxs_with_offset:
        is_local_maximum = (a_extend[i] >= 0 and
                            a_extend[i] >= np.max(a_extend[i - local_width: i + local_width + 1]))
        is_local_minimum = (a_extend[i] <  0 and
                            a_extend[i] <= np.min(a_extend[i - local_width: i + local_width + 1]))
        if (is_local_maximum or is_local_minimum):
            if is_local_minimum:
            #if is_local_maximum:
                if (i - last_pos_peak_idx) > min_peak_distance:
                    result_idxs.append(i)
                    last_pos_peak_idx = i
                #elif a_extend[i] > a_extend[last_pos_peak_idx] and len(result_idxs) > 0:
                #    print("in addtional fileter")
                #    result_idxs[ -1 ] = i
                #    last_pos_peak_idx = i
            else:
                if (i - last_neg_peak_idx) > min_peak_distance:
                    #result_idxs.append(i)
                    last_neg_peak_idx = i

    result_idxs = np.array(result_idxs) - local_width
    return (result_idxs, a[result_idxs])


def calc_match_bpm(data,bpm):
    N       = len(data)
    f_bpm   = bpm / 60
    f_frame = 44100 / CHUNK

    phase_array = np.arange(N) * 2 * np.pi * f_bpm / f_frame
    sin_match   = (1/N) * sum( data * np.sin(phase_array)) #B
    cos_match   = (1/N) * sum( data * np.cos(phase_array)) #A
    return np.sqrt(sin_match ** 2 + cos_match ** 2)

def calc_start_sec(data, bpm):
    N       = len(data)
    f_bpm   = bpm / 60
    f_frame = 44100 / CHUNK

    phase_array = np.arange(N) * 2 * np.pi * f_bpm / f_frame
    sin_match   = (1/N) * sum( data * np.sin(phase_array)) #B
    cos_match   = (1/N) * sum( data * np.cos(phase_array)) #A
    theta = math.atan2(sin_match, cos_match)
    if theta < 0 :
        theta = theta + 2 * math.pi
    return theta/( 2 * math.pi *  f_bpm )


def calc_start_idx(data, bpm):
    N       = len(data)
    f_bpm   = bpm / 60
    f_frame = 44100 / CHUNK

    phase_array = np.arange(N) * 2 * np.pi * f_bpm / f_frame
    sin_match   = (1/N) * sum( data * np.sin(phase_array)) #B
    cos_match   = (1/N) * sum( data * np.cos(phase_array)) #A
    theta = math.atan2(sin_match, cos_match)
    if theta < 0 :
        theta = theta + 2 * math.pi

    return int(theta/( 2 * math.pi *  f_bpm ) * 44100)

def calc_all_match(data):
    match_list = []
    bpm_iter   = range(1,200)

    # 各bpmにおいてmatch度を計算する
    for bpm in bpm_iter:
        match = calc_match_bpm(data,bpm)
        match_list.append(match)

    return match_list



#if __name__ == '__main__':
def calBpm(dir):
    # データの読み込み
    if len(sys.argv) > 1:
        src_name = sys.argv[1]
    else:
        src_name = dir
        #src_name = r'C:\\work\\ai_music\\freesound\\bpm_120_4.wav'

    input = wave.open(src_name, "rb")

    # データの読み込み
    # WAVファイルの情報を表示（別にいらん）
    print("filename : ",src_name )
    print("Channel num : ", input.getnchannels())
    print ("Sample size : ", input.getsampwidth())
    print ("Sampling rate : ", input.getframerate())
    print ("Frame num : ", input.getnframes())
    print ("Prams : ", input.getparams())
    print ("Sec : ", float(input.getnframes()) / input.getframerate())



    buf = input.readframes(input.getnframes())

    #print(len(data))

    if input.getsampwidth() == 2:
        data = np.frombuffer(buf, dtype='int16')
    elif input.getsampwidth() == 4:
        data = np.frombuffer(buf, dtype='int32')

    if (input.getnchannels() == 2):
        # 左チャンネル
        left = data[::2]
        # 右チャンネル
        right = data[1::2]
        print("stereo")
    else:
        right = data[::1]
        print("mono")

    dt = []

    for i in right:
        dt.append(i)

    dt = np.array(dt) /  32768.0 #(2 ** 8)一旦これでうまくいってた
    print("dt size is : ",len(dt))
    input.close()

    # フレームごとの音量データ作成
    # フレームサイズ分，振幅二乗和を計算，
    frame_size = CHUNK
    sample_total = input.getnframes()
    sample_max = sample_total - (sample_total % frame_size) #余りフレームは切り捨てる
    frame_max  = sample_max / frame_size
    frame_list = np.hsplit(dt[0:sample_max],frame_max)

    flg = True
    amp_list = []
    for x in frame_list:
        amp_list.append(np.sqrt(np.sum(np.power(x, 2))))

    amp_list = np.array(amp_list)


    amp_diff_list = amp_list[1:] - amp_list[:-1]
    amp_diff_list = np.vectorize(max)(amp_diff_list,0)

    # bpm推定
    match_list = calc_all_match(amp_diff_list)      # 各bpmのマッチ度を計算
    most_match = match_list.index(max(match_list))  # マッチ度最大のindexを取得

    bpm = most_match + 1
    #if bpm < 10:
    #    bpm = 1
    bpm = 120

    #ピーク位置検出
    print("bpm: ",bpm)
    print("min dist : ",60*44100/ bpm /4)
    peaks_f = find_peaks(dt, max(abs(dt))* 0.2, local_width = int(60*44100/ bpm /4), min_peak_distance = int(60*44100/ bpm /4)) #localwidth は10000がちょうどよい
    peaks_f_dur = []

    pre_f = 0
    for i in peaks_f[0]:
        peaks_f_dur.append( i - pre_f )
        pre_f = i
    peaks_f_dur = np.array(peaks_f_dur)

    idx = calc_start_idx(dt, bpm)

    #ピッチ算出
    pitch_list = calcPitch(dt, peaks_f[0])


    return bpm, idx, peaks_f, peaks_f_dur, pitch_list
    #print("BPM : ", most_match + 1)

    #print("START Sec. Is : ",calc_start_sec(dt[0:sample_max] , most_match + 1))

def calcPitch(dt, peak_list, fs = 44100):
    x = dt
    pitch_list = []
    #print(peak_list)

    for i in range(len(peak_list) -1 ): #最後の処理は？
        #fft
        X = np.fft.fft(x[peak_list[i]:peak_list[i + 1]])
        amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
        N = len(x[peak_list[i]:peak_list[i + 1]])   # FFTのサンプル数
        freqList = np.fft.fftfreq(N, d=1.0/fs)
        most_match = amplitudeSpectrum.index( max( amplitudeSpectrum[ 0:int(len(amplitudeSpectrum)/2) ] ) )

        pitch_list.append(convHzToPitch(freqList[most_match]))
    return pitch_list

def convHzToPitch(hz):
        list = []
        for note in range(88):
            list.append( 27.5 * 2 ** (note  / 12) )

        idx = np.abs(np.asarray(list) - hz).argmin()
        return idx + 21#+ 12

if __name__ == "__main__":

        #print(convHzToPitch(hz = 730))

        # データの読み込み
        if len(sys.argv) > 1:
            src_name = sys.argv[1]
        else:
            #src_name = dir
            src_name = r'C:\\work\\ai_music\\freesound\\bpm_80_shifted_pitch.wav'

        input = wave.open(src_name, "rb")

        # データの読み込み
        # WAVファイルの情報を表示（別にいらん）
        print("filename : ",src_name )
        print("Channel num : ", input.getnchannels())
        print ("Sample size : ", input.getsampwidth())
        print ("Sampling rate : ", input.getframerate())
        print ("Frame num : ", input.getnframes())
        print ("Prams : ", input.getparams())
        print ("Sec : ", float(input.getnframes()) / input.getframerate())


        buf = input.readframes(input.getnframes())

        if input.getsampwidth() == 2:
            data = np.frombuffer(buf, dtype='int16')
        elif input.getsampwidth() == 4:
            data = np.frombuffer(buf, dtype='int32')
        elif input.getsampwidth() == 1:
            data = np.frombuffer(buf, dtype='int8')

        if (input.getnchannels() == 2):
            # 左チャンネル
            left = data[::2]
            # 右チャンネル
            right = data[1::2]
            print("stereo")
        else:
            right = data[::1]
            print("mono")

        dt = []

        for i in right:
            dt.append(i)

        dt = np.array(dt) /  32768.0 #(2 ** 8)一旦これでうまくいってた
        print("dt size is : ",len(dt))
        input.close()

        bpm = 120

        #ピーク位置検出
        print("bpm: ",bpm)
        print("min dist : ",60*44100/ bpm /4)
        peaks_f = find_peaks(dt, max(abs(dt))* 0.2, local_width = int(60*44100/ bpm /4), min_peak_distance = int(60*44100/ bpm /4)) #localwidth は10000がちょうどよい

        pitch = calcPitch(dt, peaks_f[0])
        for hz in pitch:
            print(hz)
