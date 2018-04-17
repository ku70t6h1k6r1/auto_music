# -*- coding: utf-8 -*-
import numpy as np
from multiprocessing import Process, Queue, Value, Array
import pygame.midi
import time

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

    def setStartTime(self, start_time, latency = 7):
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
        lastBeat = nowBeat  + 16*4
        note = past_note

        self.setInstrument() #ここでいいの？

        while True:
            nowTime = time.time()
            if nowTime >= self.tsObj.abs_time_series[lastBeat]:
                self.o.note_off(note, 100, self.ch)
                break
            elif nowTime >= self.tsObj.abs_time_series[nowBeat]:
                self.o.note_off(note, 100, self.ch)
                note = self.score[nowBeat]
                self.o.note_on(note, int(95*self.articuration[nowBeat]) ,self.ch)
                nowBeat += 1

class ChildProcess:
    def defaultSet(self):
        pygame.init()
        pygame.midi.init()
        self.o = pygame.midi.Output(1)
        self.part1 = MidiOut(self.ch, self.inst_no, self.score, self.articuration, self.timeSeriesObj, self.o)
        self.part1.setSequence(0, False, 16*1)#これも変数に

    def play(self):
        self.part1.play(0,0) #これも変数に
        self.o.close()
        pygame.midi.quit()
        pygame.quit()
        exit()

    def execute(self, ch, inst_no, score, articuration, timeSeriesObj ):
        self.ch = ch
        self.inst_no = inst_no
        self.score  = score
        self.articuration = articuration
        self.timeSeriesObj = timeSeriesObj
        self.defaultSet()
        self.play()


class ParentProcess:
    def __init__(self):
        self.score = np.full(16*40, 36)
        self.articuration = np.full(16*40, 100)
        self.timeSeriesObj = TimeSeries()
        self.timeSeriesObj.setBpm(120)
        self.timeSeriesObj.setStartTime(time.time())
        self.cprocess = ChildProcess()

    def execute(self):
        p1 = Process(target = self.cprocess.execute, args = (0, 1, self.score, self.articuration, self.timeSeriesObj))
        p2 = Process(target = self.cprocess.execute, args = (1, 70, self.score, self.articuration, self.timeSeriesObj))
        p1.start()
        p2.start()
        p1.join()
        p2.join()



if __name__ == '__main__':
    pprocess = ParentProcess()
    pprocess.execute()
