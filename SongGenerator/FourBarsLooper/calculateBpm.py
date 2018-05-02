# coding: UTF-8
import numpy as np
import pyaudio
import wave
import sys
import math

CHUNK = 512*2

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
    bpm_iter   = range(40,240)

    # 各bpmにおいてmatch度を計算する
    for bpm in bpm_iter:
        match = calc_match_bpm(data,bpm)
        match_list.append(match)

    return match_list

def calBpm(dir):
    # データの読み込み
    if len(sys.argv) > 1:
        src_name = sys.argv[1]
    else:
        src_name = dir

    input = wave.open(src_name, "rb")

    # データの読み込み
    # WAVファイルの情報を表示（別にいらん）
    """
    print("filename : ",src_name )
    print("Channel num : ", input.getnchannels())
    print ("Sample size : ", input.getsampwidth())
    print ("Sampling rate : ", input.getframerate())
    print ("Frame num : ", input.getnframes())
    print ("Prams : ", input.getparams())
    print ("Sec : ", float(input.getnframes()) / input.getframerate())
    """


    buf = input.readframes(input.getnframes())

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

    dt = np.array(dt) / (2 ** 8) #一旦これでBPM検出うまくいってた 32768.0
    print("dt size is : ",len(dt))
    input.close()

    # フレームごとの音量データ作成　フレームサイズ分，振幅二乗和を計算
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

    #for i, score in enumerate(match_list):
    #    print("bpm:", i+40, score)

    bpm = most_match + 40

    #ピーク位置検出　各値は決め打ち。
    peaks_f = find_peaks(dt, max(abs(dt))* 0.2, local_width = int(60*44100/ bpm /4), min_peak_distance = int(60*44100/ bpm /4)) #localwidth は10000がちょうどよい
    peaks_f_dur = []

    #ピーク間幅算出
    pre_f = 0
    peaks_f_dur = np.zeros(len(peaks_f[0]), dtype=np.int64)
    for i, value in enumerate(peaks_f[0]):
        if i + 1 >= len(peaks_f[0]):
            peaks_f_dur[i] = 15000 #決め打ちはバグる原因なので対策必要
        else:
            peaks_f_dur[i] =  peaks_f[0][i + 1] - value


    #開始位置検出
    ##idx = calc_start_idx(dt, bpm)
    idx = peaks_f[0][0]


    #ピッチ算出
    pitch_list = calcPitch(dt, peaks_f[0])


    return bpm, idx, peaks_f, peaks_f_dur, pitch_list

def calcPitch(dt, peak_list, fs = 44100):
    x = dt
    pitch_list = []

    for i in range(len(peak_list)): #最後の処理がださい、エラー出でもおかしくない
        #fft
        if i == len(peak_list) - 1 :
            last_peak_frame = peak_list[i] + int(i + fs*0.13) #最後の処理がださい、エラー出でもおかしくない
            X = np.fft.fft(x[peak_list[i]:last_peak_frame])
            amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
            N = len(x[peak_list[i]:last_peak_frame])   # FFTのサンプル数
        else:
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
        return idx + 21

def calcTimeSeries(bpm ,start_frame = 0, fs = 44100, max_s = 600):
    """
    INDEXが16分のひとつひとつに対応
    """
    a16beat_disitance_s = 60/bpm/4
    a16beat_disitance_frame = a16beat_disitance_s * fs
    timeSeries = np.zeros(int(max_s/a16beat_disitance_s))
    for idx, value in enumerate(timeSeries):
        timeSeries[idx] = start_frame + a16beat_disitance_frame*idx
    return timeSeries

def waveToMidi(timeSeries_f, peaks_f, peaks_f_dur, pitch_list):
    melody = np.full(len(timeSeries_f), -1)
    melody_peak = np.full(len(timeSeries_f), -1)
    melody_duration = np.full(len(timeSeries_f), -1)

    for i, value in enumerate(peaks_f):
        idx = np.abs(np.asarray(timeSeries_f) - value).argmin()
        melody[idx] = pitch_list[i]
        melody_peak[idx] = value
        melody_duration[idx] = peaks_f_dur[i]

    return melody, melody_peak, melody_duration




if __name__ == '__main__':
    wav_dir = r'C:\\work\\ai_music\\freesound\\newSong_80.wav'
    #bpm, idx, peaks_f, , pitch_list

    bpmObj = calBpm(wav_dir)
    print("IN MAIN")
    print("bpm : " , bpmObj[0])
    print("idx : " , bpmObj[1])
    print("peaks_f : " , bpmObj[2][0])
    print("peaks_f_dur : " , bpmObj[3])
    print("pitch_list: " , bpmObj[4])

    ts = calcTimeSeries(bpmObj[0] ,bpmObj[1], fs = 44100, max_s = 60)
    print("ts is :",ts)
    melody = waveToMidi(ts, bpmObj[2][0], bpmObj[3], bpmObj[4])
    print(melody[0])
    print(melody[1])
    print(melody[2])
