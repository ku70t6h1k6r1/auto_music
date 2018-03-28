# -*- coding: utf-8 -*-
import common_function as func
import numpy as np

class Sequencer:
    def __init__(self):
        self.master = func.softmax([1 ,0.5 ,0.3 ,0.2, 0.5, 0.4, 0.7])

        self.noteWeight = {}
        self.sequence = np.zeros(0)
        # OUT / LOOP
        self.noteWeight[0] = func.softmax([0.5,0.2]).tolist() #Lead1
        self.noteWeight[1] = func.softmax([0.5,0.5]).tolist() #Lead2
        self.noteWeight[2] = func.softmax([0.5,0.8]).tolist() #Bucking
        self.noteWeight[3] = func.softmax([0.5,0.6]).tolist() #Bass
        self.noteWeight[4] = func.softmax([0.4,0.5]).tolist() #HiHat
        self.noteWeight[5] = func.softmax([0.4,0.5]).tolist() #Snare
        self.noteWeight[6] = func.softmax([0.4,0.5]).tolist() #BaDrum

        self.loopFlg = True
    def crateStepSequence(self, partIdx = 0, notePerBar_n = 16, onePhrase_bars = 4):
        cnt = 0
        part = func.dice(self.master)
        self.sequence  = np.r_[self.sequence, part]

        while self.loopFlg:
            loopFlg = func.dice(self.noteWeight[part])
            if loopFlg > 0 :
                self.sequence  = np.r_[self.sequence, part]
            else:
                part = func.dice(self.master)
                self.sequence  = np.r_[self.sequence, part]

            if part == partIdx:
                cnt += 1
                if cnt > 12 :
                    self.loopFlg = False

    def update(self, msg, update_n):
        if update_n % 5 == 0:
            return np.tile(msg[0:4], len(msg)/4 )
        elif update_n % 5 == 1:
            return np.tile(msg[0:8], len(msg)/8 )
        elif update_n % 5 == 2:
            return np.tile(msg[0:16], len(msg)/16 )
        elif update_n % 5 == 3:
            return np.tile(msg[0:32], len(msg)/32 )
        elif update_n % 5 == 4:
            return np.tile(msg[0:64], len(msg)/64 )
        else:
            return np.tile(msg[0:64], len(msg)/64 )
