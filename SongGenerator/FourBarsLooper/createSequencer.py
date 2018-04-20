# -*- coding: utf-8 -*-
import common_function as func
import numpy as np

class Sequencer:
    def __init__(self):
        """
        Each part-index is
        withCode = 0
        HiHat = 1
        Snare = 2
        BaDrum = 3
        """
        self.master = func.softmax([0.1 ,0.1 ,0.1 ,0.15])

        self.noteWeight = {}
        self.sequence = np.zeros(0)

        # OUT / LOOP
        self.noteWeight[0] = func.softmax([0.5,0.5]).tolist()
        self.noteWeight[1] = func.softmax([0.4,0.2]).tolist()
        self.noteWeight[2] = func.softmax([0.4,0.2]).tolist()
        self.noteWeight[3] = func.softmax([0.4,0.2]).tolist()

        self.loopFlg = 1

    def createStepSequence(self, partIdx = 0, notePerBar_n = 16, onePhrase_bars = 4):
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
                if cnt > 3 :
                    self.loopFlg = False

    def stamentUpdate(self, chObj):
        """
        Each statement-index is
        None = 0
        One-Bar = 1
        Two-Bars = 2
        Four-Bars = 3
        """

        if chObj.statement  == 0:
            chObj.setStatement(1)
            return chObj
        elif chObj.statement == 1:
            chObj.setStatement(2)
            return chObj
        elif chObj.statement  == 2:
            chObj.setStatement(3)
            return chObj
        else :
            return chObj

    def pointerUpdate(self, chObj):
        if chObj.statement  == 1:
            chObj.setPointer(np.randint(4)) #4bars
            return chObj
        elif chObj.statement == 2:
            chObj.setPOinter(np.randint(2)*2)
            return chObj
        else  :
            chObj.setPOinter(0)

class Channel:
    def __init__(self):
        """
        Each statement-index is
        None = 0
        One-Bar = 1
        Two-Bars = 2
        Four-Bars = 3
        """
        self.statement = 0
        self.pointer = 0
        self.loopFlg = 0

    def setStatement(self, stamentNum):
         self.statement = stamentNum

    def setPointer(self, pointerNum):
        self.statement = pointerNum

    def setLoopFlg(self, loopFlg):
        self.loopFlg = loopFlg
