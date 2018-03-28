# coding: UTF-8
import numpy as np
import common_function as func

class PitchWeight:
    def __init__(self):
        #self.pitchWeight_a = [5.5, 1.5, 5, 1.5, 5, 5, 1.5, 5.1, 1.5, 5, 1.5, 5]
        self.pitchWeight_a = [5.5, 0, 5, 0, 5, 6, 0, 5.1, 0, 0, 0, 8]
        self.degreeWeight_a = [1, 0.1, 2, 1.2, 1.2, 0.7, 0.7, 0.7, 1.2, 1.2, 2, 1.2]
        self.pitchWeight = func.softmax(self.pitchWeight_a,t = 0.2)
        self.degreeWeight = func.softmax(self.degreeWeight_a)

    def updateDW(self, t):
        self.degreeWeight = func.softmax(self.degreeWeight_a, t = t)

    def updateRelPW(self, pitchIndex):
        if pitchIndex > 0 :
            tmpDegreeWeight = np.r_[ self.degreeWeight [ 12 - pitchIndex : ] , self.degreeWeight [0: 12 - pitchIndex] ]
        else :
            tmpDegreeWeight = self.degreeWeight
        self.relPitchWeight = func.softmax(self.pitchWeight * tmpDegreeWeight)


#TEST
#test = PitchWeight()
#test.updateRelPW(0)
#test.updateRelPW(2)
#test.updateRelPW(5)
#test.updateRelPW(7)
