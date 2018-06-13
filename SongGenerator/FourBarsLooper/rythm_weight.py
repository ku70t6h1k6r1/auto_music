# coding: UTF-8
import numpy as np
import common_function as func

class RythmWeight:
    def __init__(self):
        self.noteLength = {}
        self.noteWeight = {}
        self.noteWeightMaster = []

        #ON
        self.noteLength[0] = [1,0,0,0 ,0,0,0,0 ,0,0,0,0 ,0,0,0,0 ]
        self.noteLength[1] = [1,0,0,0 ,0,0,0,0 ]
        self.noteLength[2] = [1,0,0,0 ]
        self.noteLength[3] = [1,0 ]
        self.noteLength[4] = [1]
        #OFF
        self.noteLength[5] = [-1,0,0,0 ,0,0,0,0 ,0,0,0,0 ,0,0,0,0 ]
        self.noteLength[6] = [-1,0,0,0 ,0,0,0,0 ]
        self.noteLength[7] = [-1,0,0,0 ]
        self.noteLength[8] = [-1,0 ]
        self.noteLength[9] = [-1]

    def setWeight(self):
        # OUT / LOOP
        #ON
        self.noteWeight[0] = func.softmax([0.5,0.5]).tolist()
        self.noteWeight[1] = func.softmax([0.5,0.5]).tolist()
        self.noteWeight[2] = func.softmax([0.5,0.8]).tolist()
        self.noteWeight[3] = func.softmax([0.5,0.6]).tolist()
        self.noteWeight[4] = func.softmax([0.4,0.5]).tolist()
        #OFF
        self.noteWeight[5] = func.softmax([0.5,0.5]).tolist()
        self.noteWeight[6] = func.softmax([0.5,0.5]).tolist()
        self.noteWeight[7] = func.softmax([0.5,0.5]).tolist()
        self.noteWeight[8] = func.softmax([0.5,0.5]).tolist()
        self.noteWeight[9] = func.softmax([0.5,0.5]).tolist()

        self.noteWeightMaster = func.softmax([7,4,6,8,5,1,1,1.5,1.5,1])


#TEST
#test = RythmWeight()
#test.setWeight()
#print test.noteLength
#print test.noteWeight
#print test.noteWeightMaster
