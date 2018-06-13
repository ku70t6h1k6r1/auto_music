# coding:utf-8
import numpy as np
from Composer import Score as sc
from AnalogSynthesizer import AnalogSynthesizer as aSynthe
from common import function as func
import pyaudio
import wave as wv

class Play:
    def __init__(self):
        self.audio  = pyaudio.PyAudio()
        o = audio.open(format=audio.get_format_from_width(2),
                                    channels=1,
                                    rate=44100,
                                    output=True)

class midiNotesToWave:
    def __init__(self, notePerBar_n = 16, bpm = 120):
        self._notePerBar_n = notePerBar_n
        self._bpm = bpm
        self._noteMinLen_sec = func.a16beatToSec(self._bpm)
        self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.square], [1.0, 0.3], [1.0, 1.0], aSynthe.FilterName.bandpass, [1,3500], [0.001, 0.02, 0.6, 0.01], 44100)

    def convert(self, score):
        return none

    def _scoreToHzAndTime(self, score):
        list = []

        #最初無音から始まる対策
        if score[0] == -1:
            list.append([-1.0,0.0])

        #self._notePerBar_nが前提
        for note in score:
            if note > -1:
                list.append([func.midiNoteToHz(note), self._noteMinLen_sec])
            else:
                list[-1][1] += self._noteMinLen_sec

        wave = np.zeros(0)
        for hz, sec in list:
            wave = np.r_[wave, self._midiNoteToWave(hz, sec)]

        return len(wave)




    def _midiNoteToWave(self, hz, sec):
        wave = self.synthesizer.setPitch(hz,sec)
        return wave


if __name__ == '__main__':
    score = [-1,-1,-1,-1, 0,-1,-1,-1, 10,-1,10,-1, 40,-1,-1,40]
    midiNotesToWaveObj = midiNotesToWave()
    print(midiNotesToWaveObj._scoreToHzAndTime(score))

if __name__ == '____':
    scoreObj = sc.Score()
    song = scoreObj.create()
    print(song.chordProg)
    print(song.melodyLine)
    print(song.voiceProg)
    print(song.bassLine)

    #DRUM
    print("DRUM")
    print(song.drumObj.hihat)
    print(song.drumObj.snare)
    print(song.drumObj.kick)
