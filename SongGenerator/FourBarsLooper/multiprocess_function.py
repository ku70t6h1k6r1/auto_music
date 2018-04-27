# -*- coding: utf-8 -*-
import numpy as np
from multiprocessing import Process, Queue, Value, Array
import pygame.midi
import time
from time import sleep
import pyaudio
import wave
#play.py作るならそっち？
import createSequencer as seq

class TimeSeries:
    """
    For 16beat * 4 Bars
    """

    def setBpm(self, bpm, max_length = 600):
        self.bpm = bpm
        self.max_length = max_length
        self.dist_time_16 = 60 / self.bpm / 4
        self.max_bars = int(self.max_length/self.dist_time_16/16)
        self.beat_idx = np.zeros(self.max_bars * 16)
        self.time_series = np.zeros(len(self.beat_idx))
        for i in range(len(self.beat_idx)):
            self.beat_idx[i] = i % 16
            self.time_series[i] = self.dist_time_16 * i
        self.abs_time_series =  self.time_series

    def setStartTime(self, start_time, latency = 40):
        self.abs_time_series =  self.time_series + start_time + latency

class MidiOut:
    """
    For Use pygame.midi
    """
    def __init__(self, ch, inst_no, score, articuration, TimeSeriesObj ,o):
        self.ch = ch
        self.inst_no = inst_no
        self.o = o
        self.score = score
        self.articuration = articuration
        self.tsObj = TimeSeriesObj

    def setScore(self, score):
        self.score = score

    def setArticuration(self, articuration):
        self.articuration = articuration

    def setTimeSeriesObj(self, TimeSeriesObj):
        self.tsObj = TimeSeriesObj

    def setSequence(self, pointer, loopFlg, length_16beat): #setPointer is the position of 16beat IDX, length_16beat 16 x 1 OR 2 OR 4
        self.preparedScore = np.full(16 * 4 * len(self.score[0]), -1 ) #16beat * 4bars
        self.preparedScore =  np.reshape(self.preparedScore, (16 * 4 , len(self.score[0])))

        print(self.score)
        print(self.preparedScore)
        if loopFlg :
            #ちゃんと修正
            self.preparedScore = np.tile(self.score[pointer.value : pointer.value + length_16beat], lenth(self.preparedScore ) / length_16beat )
        else:
            self.preparedScore[0:length_16beat] = self.score[pointer.value : pointer.value + length_16beat]
        print(self.preparedScore)

    def setControlChange(self, no, value):
        self.o.write_short(0xb0 + self.ch, no, value)

    def setInstrument(self):
        self.o.set_instrument(self.inst_no, self.ch)

    def play(self, pointer, currentBeat, playFlg) :

        preNote = np.full(len(self.score[0]), 0)  #past_note
        self.setInstrument() #ここでいいの？

        while True:
            nowTime = time.time()

            if playFlg.value == 0 or pointer.value >= len(self.score) :  #あとで要調整
                for note in preNote:
                    self.o.note_off(note, 100, self.ch)

            elif nowTime >= self.tsObj.abs_time_series[currentBeat.value] :
                notes = self.score[pointer.value]
                for v, note in enumerate(notes):
                    if note > -1:
                        self.o.note_off(preNote[v], 100, self.ch)
                        self.o.note_on(note, int(self.articuration[pointer.value][v]) ,self.ch)
                        preNote[v] = note

class WaveOut:
    """
    for use pyaudio
    """
    def __init__(self, i, chunk, score, articuration, TimeSeriesObj ,o):
        self.i = i
        self.o = o
        self.chunk = chunk
        self.score = score
        self.articuration = articuration
        self.tsObj = TimeSeriesObj

    def setScore(self, score):
        self.score = score

    def setArticuration(self, articuration):
        self.articuration = articuration

    def setTimeSeriesObj(self, TimeSeriesObj):
        self.tsObj = TimeSeriesObj

    def setSequence(self, setPointer, loopFlg, length_16beat): #setPointer is the position of 16beat IDX, length_16beat 16 x 1 OR 2 OR 4
        self.preparedScore = np.full(16 * 4, -1) #16beat * 4bars
        if loopFlg :
            self.preparedScore = np.tile(self.score[setPointer : setPointer + length_16beat], lenth(self.preparedScore ) / length_16beat )
        else:
            self.preparedScore[0:length_16beat] = self.score[setPointer : setPointer + length_16beat]

    def play(self, playing = True, nowBeat = 0):
        self.i.setpos(10000)
        while playing:
            data = self.i.readframes(self.chunk)
            if len(data) > 0:
                self.o.write(data)
            else:
                self.playing = False

class ChildProcessWave:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def defaultSet(self):
        self.audio  = pyaudio.PyAudio()
        self.i = wave.open(self.audio_file, "rb")
        self.o = self.audio.open(format=self.audio.get_format_from_width(self.i.getsampwidth()),
                                channels=self.i.getnchannels(),
                                rate=self.i.getframerate(),
                                output=True)
        self.i.setpos(10000)
        self.wave = WaveOut(self.i, self.chunk, self.score, self.articulation, self.timeSeriesObj, self.o)

    def play(self):
        self.wave.play()
        self.o.stop_stream()
        self.o.close()
        self.i.close()
        self.audio.terminate()

    def execute(self, score = 1, articuration = 1, timeSeriesObj = 1):
        self.chunk = 1024
        self.playing = True
        self.score = score
        self.articulation = articuration
        self.timeSeriesObj = timeSeriesObj
        self.defaultSet()
        self.play()

class ChildProcess:
    def __init__(self, device_no, ch, inst_no, pointer, currentBeat, score, articuration, timeSeriesObj, playFlg):
        self.device_no = device_no
        self.ch = ch
        self.inst_no = inst_no
        self.pointer = pointer
        self.currentBeat = currentBeat
        self.score  = score
        self.articuration = articuration
        self.timeSeriesObj = timeSeriesObj
        self.playFlg = playFlg

    def defaultSet(self):
        pygame.init()
        pygame.midi.init()
        self.o = pygame.midi.Output(self.device_no)
        self.midi = MidiOut(self.ch, self.inst_no, self.score, self.articuration, self.timeSeriesObj, self.o)
        #self.midi.setSequence(self.pointer, False, 1*16)#これも変数に

    def play(self):
        self.midi.play(self.pointer,self.currentBeat,self.playFlg) #これも変数に
        self.o.close()
        pygame.midi.quit()
        pygame.quit()
        exit()

    def execute(self):
        self.defaultSet()
        self.play()

class StepSequencer:
    def __init__(self, pointer_a, sequencer, playFlg_a, sequencer_OnOff):
        self.playFlg_a = playFlg_a
        self.pointer_a = pointer_a
        self.sequencer = sequencer
        self.sequencer_OnOff = sequencer_OnOff

    def execute(self, timeSeriesObj, currentBeat):
        self.tsObj = timeSeriesObj

        while True:
            nowTime = time.time()
            if  currentBeat.value >= len(self.sequencer) :  #今はいい感じに動いているけど、更新がすべてのパートに先行して行われることを担保する必要がある。
                for playFlg in self.playFlg_a:
                    playFlg.value = 0
                break
            elif nowTime >= self.tsObj.abs_time_series[currentBeat.value] :
                beat = currentBeat.value #今はいい感じに動いているけど、更新がすべてのパートに先行して行われることを担保する必要がある。これでお茶濁し中。
                currentBeat.value += 1
                directions = self.sequencer[beat]

                for v, direction in enumerate(directions):
                    if  direction > -1:
                        self.pointer_a[v].value = direction
                    else:
                        self.pointer_a[v].value  += 1

                for v2, playFlg in enumerate(self.playFlg_a):
                    if self.sequencer_OnOff[beat][v2] > -1 :
                        playFlg.value = self.sequencer_OnOff[beat][v2]


if __name__ == '__main__':
    # multiprocessing setting
    timeSeriesObj = TimeSeries()
    timeSeriesObj.setBpm(140)
    print("SET START TIME")
    timeSeriesObj.setStartTime(time.time())
    device = 0

    #Rythm Section
    artculation = np.array([2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2    ,2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2    ,2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2    ,2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2])
    art = np.stack([artculation * 50], axis = -1)
    cHH = np.array([1,1,1,1,  1,1,1,1,  1,1,1,1,  1,-1,-1,1    ,1,-1,1,-1,  1,-1,1,-1,  1,-1,1,-1,  1,-1,1,-1    ,1,-1,-1,1,  1,-1,-1,1,  1,-1,-1,1,  1,-1,-1,1    ,1,-1,1,1,  1,-1,1,1,  1,-1,1,1,  1,-1,1,1])
    dr = np.stack([cHH * 42], axis = -1)

    #Harmoney Section
    melody = np.array([2,0,4,5,  7,9,11,12,  0,2,4,5,  7,9,11,12     ,0,2,0,2,  0,4,0,4,  0,5,0,5,  0,7,0,7    ,0,-1,-1,-1,  2,-1,-1,-1,  4,-1,-1,-1,  5,-1,-1,-1    ,0,-1,-1,-1,  2,-1,-1,-1,  4,-1,-1,-1,  5,-1,-1,-1])
    pf = np.stack([melody+60], axis = -1)

    #For Shared Memory
    pointer_dr = Value('i', 0)
    pointer_pf = Value('i', 0)
    currentBeat = Value('i', 0)
    playFlg_dr = Value('i', 1)
    playFlg_pf = Value('i', 1)

    #Create SubProcess
    sp_Dr =  ChildProcess(device, 9, 0, pointer_dr, currentBeat, dr, art, timeSeriesObj, playFlg_dr)
    sp_Pf =  ChildProcess(device, 0, 0, pointer_pf, currentBeat, pf, art, timeSeriesObj, playFlg_pf)

    #createSequencer
    rythm_seq = np.array([0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1 \
                                ,16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1 \
                                ,16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1 \
                                ])

    harmony_seq = np.array([0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ])

    #createSequencerOnOff
    rythm_seq_onoff = np.array([1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ,1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ,-1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ,0,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ])

    harmony_seq_onoff = np.array([1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ,-1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ,-1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ,-1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1,  -1,-1,-1,-1 \
                                ])

    seq = StepSequencer( [pointer_dr, pointer_pf], np.stack([rythm_seq, harmony_seq], axis = -1), [playFlg_dr, playFlg_pf], np.stack([rythm_seq_onoff, harmony_seq_onoff], axis = -1))
    p = Process(target = seq.execute, args=(timeSeriesObj, currentBeat) ) #pointerとflgの整理
    p1 = Process(target = sp_Dr.execute)
    p2 = Process(target = sp_Pf.execute)

    p.start()
    p1.start()
    p2.start()
    p.join()
    sleep(1)
    p1.terminate()
    p2.terminate()
