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

    def setStartTime(self, start_time, latency = 25):
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

    def setSequence(self, setPointer, loopFlg, length_16beat): #setPointer is the position of 16beat IDX, length_16beat 16 x 1 OR 2 OR 4
        self.preparedScore = np.full(16 * 4, -1) #16beat * 4bars
        if loopFlg :
            self.preparedScore = np.tile(self.score[setPointer : setPointer + length_16beat], lenth(self.preparedScore ) / length_16beat )
        else:
            self.preparedScore[0:length_16beat] = self.score[setPointer : setPointer + length_16beat]

    def setControlChange(self, no, value):
        self.o.write_short(0xb0 + self.ch, no, value)

    def setInstrument(self):
        self.o.set_instrument(self.inst_no, self.ch)

    def play(self, past_note = 0, nowBeat = 0):
        """
        16 * 4 実行しっぱなし
        """
        nowBeat = nowBeat #共有メモリで実装？
        lastBeat = nowBeat  + 16*96 #これで変更
        preNote = past_note

        self.setInstrument() #ここでいいの？

        while True:
            nowTime = time.time()
            if nowTime >= self.tsObj.abs_time_series[lastBeat]:
                self.o.note_off(preNote, 100, self.ch)
                break
            elif nowTime >= self.tsObj.abs_time_series[nowBeat] :
                note = self.score[nowBeat]
                if note > -1 :
                    self.o.note_off(preNote, 100, self.ch)
                    self.o.note_on(note, int(self.articuration[nowBeat]) ,self.ch)
                    preNote = note
                nowBeat += 1

class MidiOutHomo:
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

    #def setSequence(self, setPointer, loopFlg, length_16beat): #setPointer is the position of 16beat IDX, length_16beat 16 x 1 OR 2 OR 4
    #    self.preparedScore = np.full(16 * 4, -1) #16beat * 4bars
    #    if loopFlg :
    #        #ちゃんと修正
    #        self.preparedScore = np.tile(self.score[setPointer : setPointer + length_16beat], lenth(self.preparedScore ) / length_16beat )
    #    else:
    #        self.preparedScore[0:length_16beat] = self.score[setPointer : setPointer + length_16beat]

    def setControlChange(self, no, value):
        self.o.write_short(0xb0 + self.ch, no, value)

    def setInstrument(self):
        self.o.set_instrument(self.inst_no, self.ch)

    def play(self, past_note = 0, nowBeat = 0):
        """
        16 * 4 実行しっぱなし
        """
        nowBeat = nowBeat #共有メモリで実装？
        lastBeat = nowBeat  + 16*96 #これで変更
        preNote = np.full(len(self.score[0]), 0)  #past_note

        self.setInstrument() #ここでいいの？

        while True:
            nowTime = time.time()
            if nowTime >= self.tsObj.abs_time_series[lastBeat] or nowBeat >= len(self.score) :  #あとで要調整
                for note in preNote:
                    self.o.note_off(note, 100, self.ch)
                break
            elif nowTime >= self.tsObj.abs_time_series[nowBeat] :
                notes = self.score[nowBeat]
                for v, note in enumerate(notes):
                    if note > -1:
                        self.o.note_off(preNote[v], 100, self.ch)
                        self.o.note_on(note, int(self.articuration[nowBeat][v]) ,self.ch)
                        preNote[v] = note
                nowBeat += 1

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
    def __init__(self, device_no, ch, inst_no, score, articuration, timeSeriesObj ):
        self.device_no = device_no
        self.ch = ch
        self.inst_no = inst_no
        self.score  = score
        self.articuration = articuration
        self.timeSeriesObj = timeSeriesObj

    def defaultSet(self):
        pygame.init()
        pygame.midi.init()
        self.o = pygame.midi.Output(self.device_no)
        self.midi = MidiOut(self.ch, self.inst_no, self.score, self.articuration, self.timeSeriesObj, self.o)
        self.midi.setSequence(0, False, 16*1)#これも変数に

    def play(self):
        self.midi.play(0,0) #これも変数に
        self.o.close()
        pygame.midi.quit()
        pygame.quit()
        exit()

    def execute(self):
        self.defaultSet()
        self.play()

class ChildProcessHomo:
    def __init__(self, device_no, ch, inst_no, score, articuration, timeSeriesObj ):
        self.device_no = device_no
        self.ch = ch
        self.inst_no = inst_no
        self.score  = score
        self.articuration = articuration
        self.timeSeriesObj = timeSeriesObj

    def defaultSet(self):
        pygame.init()
        pygame.midi.init()
        self.o = pygame.midi.Output(self.device_no)
        self.midi = MidiOutHomo(self.ch, self.inst_no, self.score, self.articuration, self.timeSeriesObj, self.o)
        #self.midi.setSequence(0, False, 16*1)#これも変数に

    def play(self):
        self.midi.play(0,0) #これも変数に
        self.o.close()
        pygame.midi.quit()
        pygame.quit()
        exit()

    def execute(self):
        self.defaultSet()
        self.play()

class ParentProcess:
    def __init__(self):
        self.score = np.full(16*40, 36)
        self.articuration = np.full(16*40, 100)
        self.timeSeriesObj = TimeSeries()
        self.timeSeriesObj.setBpm(120)
        self.timeSeriesObj.setStartTime(time.time())
        self.cprocess = ChildProcess(1,0, 1, self.score, self.articuration, self.timeSeriesObj)

        #Wav test
        self.cprocessWave = ChildProcessWave(r'C:\\work\\ai_music\\freesound\\yukio_mishima.wav')
        self.cprocessWave2 = ChildProcessWave(r'C:\\work\\ai_music\\freesound\\yukio_mishima_l.wav')

    def execute(self):
        p1 = Process(target = self.cprocess.execute)
        #p2 = Process(target = self.cprocess.execute, args = (1, 70, self.score, self.articuration, self.timeSeriesObj))
        p1.start()
        #p2.start()
        p1.join()
        #p2.join()

        #pWave = Process(target = self.cprocessWave.execute)
        #sleep(3)
        #pWave2 = Process(target = self.cprocessWave2.execute)

        #print("start")
        ##    pWave = Process(target = self.cprocessWave.execute)
        #    pWave.start()
        #    sleep(1)
        #    pWave.terminate()

        #pWave2.start()
        #pWave.join()
        #pWave2.join()

if __name__ == '__main__':
    #pprocess = ParentProcess()
    #pprocess.execute()


    # multiprocessing setting
    timeSeriesObj = TimeSeries()
    timeSeriesObj.setBpm(180)
    print("SET START TIME")
    timeSeriesObj.setStartTime(time.time())
    device = 0
    artculation = np.array([1 ,1, 1, 1,  1 ,1, 1, 1,  2 ,2, 2, 2,  2 ,2, 2, 2])
    artculation2 = np.array([2 ,2, 2, 2,  1 ,1, 1, 1,  1 ,1, 1, 1,  1 ,1, 1, 1])
    art = np.stack([artculation * 50], axis = -1)

    cHH = np.array([1 ,1, 1, 1,  1 ,1, 1, 1,  1 ,1, 1, 1,  1 ,1, 1, 1])
    bDr = np.array([1 ,1, 1, 1,  1 ,1, 1, 1,  1 ,1, 1, 1,  1 ,1, 1, 1])
    dr = np.stack([cHH * 42], axis = -1)

    sp_Dr =  ChildProcessHomo(device, 9, 0, dr, art, timeSeriesObj)

    p1 = Process(target = sp_Dr.execute)
    p1.start()
    p1.join()
