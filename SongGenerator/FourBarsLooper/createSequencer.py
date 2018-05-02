# -*- coding: utf-8 -*-
import common_function as func
import numpy as np

class Sequencer:
    def __init__(self, startPointer):
        #self.length = length # 16 * 4 * n
        self.rythm_seq = np.zeros(0) #1
        self.rythm_seq_base = base_Patterns(startPointer)
        self.harmony_seq = np.zeros(0) #2
        self.harmony_seq_base = base_Patterns(startPointer)

        # 1 2消えちゃった時用
        self.etc1_seq = np.zeros(0) #
        self.etc1_seq_base = base_Patterns(startPointer)
        self.harmony_off = True
        self.rythm_off = True

        """
        現状、大きくHarmonic, Rytmicなものの状態遷移があり、その中でON OFFを決めていく
        Each part-index is
        hold = 0 0は必ずhold
        rythm = 1
        harmony = 2
        """
        self.node_prob_control = func.softmax([0.2, 0.2 ,0.2])

        # OUT / LOOP
        self.loopWeight = {}
        self.loopWeight[0] = func.softmax([0.8,0.1]).tolist()
        self.loopWeight[1] = func.softmax([0.4,0.2]).tolist()
        self.loopWeight[2] = func.softmax([0.4,0.6]).tolist()

    def create_stepSequencer(self, startPartIndex, stopPartIdx) :
        self.loopFlg = 1
        cnt = 0
        part = startPartIndex
        self.sequence = np.zeros(0)
        self.sequence  = np.r_[self.sequence, part]

        while self.loopFlg:
            loopFlg = func.dice(self.loopWeight[part])
            if loopFlg > 0 :
                self.sequence  = np.r_[self.sequence, part]
            else:
                part = func.dice(self.node_prob_control)
                self.sequence  = np.r_[self.sequence, part]

            if part == stopPartIdx:
                cnt += 1
                if cnt > 4 :
                    self.loopFlg = False
        print(self.sequence)

        #On OffのSequencer
        self.rythm_seq_OnOff = np.full(len(self.sequence) * 16 * 4, -1)
        self.harmony_seq_OnOff = np.full(len(self.sequence) * 16 * 4, -1)
        self.etc1_seq_OnOff = np.full(len(self.sequence) * 16 * 4, -1)
        self.rythm_seq_OnOff[0] = 0
        self.harmony_seq_OnOff[0] = 0
        self.etc1_seq_OnOff[0] = 0

        for beat, statement in enumerate(self.sequence) :
            self.etc1_seq = np.r_[self.etc1_seq, self.etc1_seq_base.patterns[0]]

            if statement  == 1:
                self.rythm_seq_base.update_Statement()
                self.rythm_seq = np.r_[self.rythm_seq, self.rythm_seq_base.patterns[self.rythm_seq_base.statement]]
                self.harmony_seq = np.r_[self.harmony_seq, self.harmony_seq_base.patterns[self.harmony_seq_base.statement]]
                if self.rythm_seq_base.statement == 1 :
                    self.rythm_seq_OnOff[beat*16*4] = 1
                    self.rythm_off = False
                elif self.rythm_seq_base.statement == 0 :
                    self.rythm_seq_OnOff[beat*16*4] = 0
                    self.rythm_off = True

                if  self.rythm_off and self.harmony_off:
                    self.etc1_seq_OnOff[beat*16*4]  = 1
                #他のが消えた時の保険としてだけ使いたいときは下のを調整
                #else:
                #    self.etc1_seq_OnOff[beat*16*4]  = 0 # etc keep alive mode

            elif statement  == 2:
                self.harmony_seq_base.update_Statement()
                self.harmony_seq = np.r_[self.harmony_seq, self.harmony_seq_base.patterns[self.harmony_seq_base.statement]]
                self.rythm_seq = np.r_[self.rythm_seq, self.rythm_seq_base.patterns[self.rythm_seq_base.statement]]
                if self.harmony_seq_base.statement == 1 :
                    self.harmony_seq_OnOff[beat*16*4] = 1
                    self.harmony_off = False
                elif self.harmony_seq_base.statement == 0 :
                    self.harmony_seq_OnOff[beat*16*4] = 0
                    self.harmony_off = True

                if  self.rythm_off and self.harmony_off:
                    self.etc1_seq_OnOff[beat*16*4]  = 1
                #他のが消えた時の保険としてだけ使いたいときは下のを調整
                #else:
                #    self.etc1_seq_OnOff[beat*16*4]  = 0 # etc keep alive mode

            else:
                self.rythm_seq = np.r_[self.rythm_seq, self.rythm_seq_base.patterns[self.rythm_seq_base.statement]]
                self.harmony_seq = np.r_[self.harmony_seq, self.harmony_seq_base.patterns[self.harmony_seq_base.statement]]

        #floatになっちゃう対策
        self.rythm_seq = self.rythm_seq.astype(np.int64)
        self.harmony_seq = self.harmony_seq.astype(np.int64)
        self.etc1_seq = self.etc1_seq.astype(np.int64)
        print("etc1 is ",self.etc1_seq_OnOff)

class base_Patterns:
    def __init__(self, startPointer):
        """
        4bars is  1 A.U.
        Each statement-index is
        None = 0 内部状態はここに設定した配列に依存する。つまりetc1の演奏内容はindex=0の配列。
        One-Bar = 1
        Two-Bars = 2
        Four-Bars = 3
        """
        self.statement = 0
        self.patterns = [\
            [startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1  ,-1,-1,-1,-1,     startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1,      startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1     ,startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ]\
            ,[startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1  ,-1,-1,-1,-1,     startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1,      startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1     ,startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ]\
            ,[startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1  ,-1,-1,-1,-1,     -1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1,      startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1     ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ]\
            ,[startPointer,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1  ,-1,-1,-1,-1,     -1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1,      -1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1     ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ,-1,-1,-1,-1 ]\
        ]

    def update_Statement(self):
        self.statement = (self.statement + 1) % 4

"""
class Sequencer_OnOff:
    def __init__(self, seq_OnOff):
        self.seq = seq_OnOff

    def update(self):
"""


if __name__ == '__main__':
    obj = Sequencer(0)
    obj.create_stepSequencer(2,1)
    print(len(obj.sequence), obj.sequence)
    print(len(obj.harmony_seq), obj.harmony_seq)
    print(len(obj.rythm_seq), obj.rythm_seq)
    print("###")
    print(len(obj.harmony_seq_OnOff), obj.harmony_seq_OnOff)
    print(len(obj.rythm_seq_OnOff), obj.rythm_seq_OnOff)
