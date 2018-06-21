        # coding: UTF-8
import numpy as np

def midiNoteToHz(midiNote):
    # ref:https://drumimicopy.com/audio-frequency/
    return 440 * 2**( (midiNote - 69)/12 )

def a16beatToSec( bpm):
    return 60/bpm/4

def toBytes(wave):
    return (wave * float(2 ** (32 - 1) ) ).astype(np.int32).tobytes()

def add(wav_list, w_list):
    len_list = []
    for np_a in wav_list:
        len_list.append(len(np_a))

    length = np.min(np.array(len_list))

    wave = np.zeros(length)
    for idx, np_a in enumerate(wav_list):
        wave = wave + np_a[0:length] * w_list[idx]

    return wave/sum(w_list)
