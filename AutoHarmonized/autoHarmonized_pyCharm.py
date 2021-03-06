# coding: UTF-8
import math
import random
import numpy as np

# シグモイド関数
def sigmoid(a):
    return 1.0 / (1.0 + math.exp(-a)) #GAIN設定したほうが良い

# ソフトマックス関数
def softmax(a):
    temp = np.empty(len(a))
    
    for i in range(len(a)):
        temp[i] = math.exp(a[i])
    
    return temp / temp.sum()

# ニューロン
class Neuron:
    input_sum = 0.0
    output = 0.0

    def setInput(self, inp):
        self.input_sum += inp

    def getOutput(self):
        self.output = sigmoid(self.input_sum)
        return self.output

    def reset(self):
        self.input_sum = 0.0
        self.output = 0.0


# ニューラルネットワーク
class NeuralNetwork:

    #リスト初期値
    w_im = []
    w_om = []
    input_layer = []
    middle_layer = []
    output_layer = []

    inputBP_layer = []
    middleBP_layer = []
    outputBP_layer = []
    
    def initialize(self, in_n, middle_n, out_n):
        self.in_n = in_n
        self.middle_n = middle_n
        self.out_n = out_n
        
        #重み初期値
        self.w_im = [[0.0] * self.middle_n for i in range(self.in_n + 1 )]
        self.w_mo = [[0.0] * self.out_n for i in range(self.middle_n + 1 )]
        self.resetW()
        
        #各層の初期値
        self.input_layer = [0.0] * self.in_n
        self.input_layer.append(1.0)
        
        for iMID in range (self.middle_n):
            self.middle_layer.append(Neuron())
        self.middle_layer.append(1.0)

        for iOUT in range (self.out_n):
            self.output_layer.append(Neuron())

        #BP用
        for iMID in range (self.middle_n):
            self.middleBP_layer.append(Neuron())

        for iOUT in range (self.out_n):
            self.outputBP_layer.append(Neuron())

    # ----重み初期値設定
    def resetW(self):
        for post in range(self.middle_n):
            for pre in range(self.in_n + 1):
                self.w_im[pre][post] = random.uniform(-1,1)
        for post in range(self.out_n):
            for pre in range(self.middle_n + 1):
                self.w_mo[pre][post] = random.uniform(-1,1)

    # 実行
    def commit(self, input_data):
        # 各層のリセット
        for iIN in range (self.in_n):
            self.input_layer[iIN] = input_data[iIN]

        for iMID in range (self.middle_n):
            self.middle_layer[iMID].reset()

        for iOUT in range (self.out_n):
            self.output_layer[iOUT].reset()

        # 入力層→中間層
        for iIN in range (self.in_n + 1):
            for iMID in range (self.middle_n):
                self.middle_layer[iMID].setInput(self.input_layer[iIN] * self.w_im[iIN][iMID])

        # 中間層→出力層
        
        for iMID in range (self.middle_n ):
            for iOUT in range (self.out_n):
                self.output_layer[iOUT].setInput(self.middle_layer[iMID].getOutput() * self.w_mo[iMID][iOUT])

        for iOUT in range (self.out_n):
            self.output_layer[iOUT].setInput(self.middle_layer[self.middle_n] * self.w_mo[self.middle_n][iOUT])
            self.output_layer[iOUT].getOutput()

        return self.output_layer

    def learn(self, inputData, outputData):
        # 各層のリセット
        for iMID in range (self.middle_n):
            self.middleBP_layer[iMID].reset()

        for iOUT in range (self.out_n):
            self.outputBP_layer[iOUT].reset()

        #NW出力
        nwResult = self.commit(inputData)
        
        nwOutputData = [] #0-1
        for i in range(self.out_n):
            nwOutputData.append(nwResult[i].output)
            print nwResult[i].output

        #学習係数
        k = 0.8


        #出力層
        for iOUT in range(self.out_n):
            self.outputBP_layer[iOUT].setInput( (1.0 -  nwOutputData[iOUT] ) *  nwOutputData[iOUT] * 2.0 * ( nwOutputData[iOUT] - outputData[iOUT] ) )


        #中間層
        for iMID in range(self.middle_n):
            for iOUT in range(self.out_n):
                self.middleBP_layer[iMID].setInput(self.outputBP_layer[iOUT].input_sum * self.w_mo[iMID][iOUT]) 
            self.middleBP_layer[iMID].output = self.middleBP_layer[iMID].input_sum * ( 1.0 - self.middle_layer[iMID].output ) * self.middle_layer[iMID].output

        #出力層→中間層
        for post in range(self.out_n):
            for pre in range(self.middle_n):
                self.w_mo[pre][post] -= k * self.outputBP_layer[post].input_sum  *  self.middle_layer[pre].output

        #中間層→入力層
        for post in range(self.middle_n):
            for pre in range(self.in_n):
                self.w_im[pre][post] -= k * self.middleBP_layer[post].output *  self.input_layer[pre] 
                #self.input_layer[pre].output sigmoidじゃない Neuron()じゃない

        return self
#コード
class Chord:
    IM7 = [0,4,7,11]
    I7 = [0,4,7,10]
    Isus4M7 = [0,5,7,11]
    Isus47 = [0,5,9,10]
    Im7 = [0,3,7,10]
    ImM7 = [0,3,7,11]
    Imb57= [0,3,6,10]
    Idim7 = [0,3,6,9]

    chordTones = []

    def convertNote(notes,num):
        outputNotes = []
        for i in range(len(notes)):
            if notes[i] + num > 11:
                outputNotes.append(notes[i] + num - 12)
            else:
                outputNotes.append(notes[i] + num)
        return outputNotes

    for i in range(12):
        tempChordTones = []
        tempChordTones.append(convertNote(IM7,i))
        tempChordTones.append(convertNote(I7,i))
        tempChordTones.append(convertNote(Isus4M7,i))
        tempChordTones.append(convertNote(Isus47,i))
        tempChordTones.append(convertNote(Im7,i))
        tempChordTones.append(convertNote(ImM7,i))
        tempChordTones.append(convertNote(Imb57,i))
        tempChordTones.append(convertNote(Idim7,i))
        chordTones.append(tempChordTones)

    def output(self):
        return self.chordTones


class CreateLearningData:
    t = 0.01
    rootDeg = 0
    chordIndex = 0


    def initialize(self,t,rootDeg,chordIndex):
        self.t = t
        self.rootDeg = rootDeg
        self.chordIndex = chordIndex
        self.chordTones = Chord().output()
        print self.chordTones

    def input(self):
        temp = np.zeros(12)

        for i in range(4):
            temp[self.chordTones[self.rootDeg][self.chordIndex][i]] = 1.0 / self.t
        return softmax(temp)

    def output(self):
        temp = np.zeros(96)
        temp[self.rootDeg * 8 + self.chordIndex] = 1
        return temp

#テスト実行

testNW = NeuralNetwork()
NeuralNetwork.initialize(testNW, 12, 8, 96)
NeuralNetwork.resetW(testNW)

for i in range(100):
    rootDeg = int(random.uniform(0,11))
    chordIndex = int(random.uniform(0,8))
    learningData = CreateLearningData()
    learningData.initialize(1.0 ,rootDeg, chordIndex)
    print i
    NeuralNetwork.learn(testNW, learningData.input(), learningData.output())

np.savetxt('out_im.csv', testNW.w_im, delimiter=',')
np.savetxt('out_mo.csv', testNW.w_mo, delimiter=',')

#print test.chordTones[2][1] #ROOT度,コード,コードトーン
print "#TEST##################"
testData = CreateLearningData()
testData.initialize(1.0,0,0)
print testNW.learn(testData.input(),testData.output())
