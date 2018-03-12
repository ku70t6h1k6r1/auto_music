# coding: UTF-8
import numpy as np
import common_function as func

class PitchWeight:
    def __init__(self):
        self.pitchWeight = func.softmax([5.5, 1.5, 5, 1.5, 5, 5, 1.5, 5.1, 1.5, 5, 1.5, 5]).tolist()

#TEST
#test = PitchWeight()
#print test.pitchWeight
