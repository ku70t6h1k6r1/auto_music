# coding: UTF-8
import math
import random
import numpy as np
import common_function as func
import chord_voices as cv

# ニューロン
class Neuron:
    input_sum = 0.0
    output = 0.0

    def setInput(self, inp):
        self.input_sum += inp

    def getOutput(self):
        self.output = func.sigmoid(self.input_sum)
        return self.output

    def reset(self):
        self.input_sum = 0.0
        self.output = 0.0


# ニューラルネットワーク
class NeuralNetwork:
    # リスト初期値
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

        # 重み初期値
        self.w_im = [[0.0] * self.middle_n for i in range(self.in_n + 1)]
        self.w_mo = [[0.0] * self.out_n for i in range(self.middle_n + 1)]
        self.resetW()

        # 各層の初期値
        self.input_layer = [0.0] * self.in_n
        self.input_layer.append(1.0)

        for iMID in range(self.middle_n):
            self.middle_layer.append(Neuron())
        self.middle_layer.append(1.0)

        for iOUT in range(self.out_n):
            self.output_layer.append(Neuron())

        # BP用
        for iMID in range(self.middle_n):
            self.middleBP_layer.append(Neuron())

        for iOUT in range(self.out_n):
            self.outputBP_layer.append(Neuron())

    # ----重み初期値設定
    def resetW(self):
        self.w_im = np.loadtxt("out_im.csv", delimiter=",")
        self.w_mo = np.loadtxt("out_mo.csv", delimiter=",")

    # 実行
    def commit(self, input_data):
        # 各層のリセット
        for iIN in range(self.in_n):
            self.input_layer[iIN] = input_data[iIN]

        for iMID in range(self.middle_n):
            self.middle_layer[iMID].reset()

        for iOUT in range(self.out_n):
            self.output_layer[iOUT].reset()

        # 入力層→中間層
        for iIN in range(self.in_n + 1):
            for iMID in range(self.middle_n):
                self.middle_layer[iMID].setInput(self.input_layer[iIN] * self.w_im[iIN][iMID])

        # 中間層→出力層

        for iMID in range(self.middle_n):
            for iOUT in range(self.out_n):
                self.output_layer[iOUT].setInput(self.middle_layer[iMID].getOutput() * self.w_mo[iMID][iOUT])

        for iOUT in range(self.out_n):
            self.output_layer[iOUT].setInput(self.middle_layer[self.middle_n] * self.w_mo[self.middle_n][iOUT])
            self.output_layer[iOUT].getOutput()

        return self.output_layer

#コード
class Harmonize:
    def __init__(self):
        chordObj = cv.Chord()
        self.voice = chordObj.tones
        self.chordNo = -1
        self.chordIndex = -1
        self.root = -1

    def translateMelody(self,melody):
        output = []
        oneNote = np.zeros(12)
        # minimum beat length sixteen-beat and then 16
        for i in range(8):
            if melody[i] != -1:
                oneNote[melody[i]] = oneNote[melody[i]]  + 1
        output = func.softmax(oneNote)
        return output

    def chord(self,chords):
        self.chordNo = chords.argmax()
        #self.root = int(self.chordNo * 1.0 / 8)
        #self.chordIndex = self.chordNo % 8

def Create(melody, noteParChord_n = 16): #8か12か16でしょう。
    harmonizeNW = NeuralNetwork()
    NeuralNetwork.initialize(harmonizeNW , 12, 8, 96)
    NeuralNetwork.resetW(harmonizeNW)

    chordObj = Harmonize()
    chords = np.full(len(melody), -1)

    for i in range(len(melody)/noteParChord_n):
        noteFreq = chordObj.translateMelody(melody[i*noteParChord_n : (i+1)*noteParChord_n])
        tempOutputLayer = harmonizeNW.commit(noteFreq)
        outputLayer = np.zeros(96)
        for j in range(96):
            outputLayer[j] = tempOutputLayer[j].output
        chordObj.chord(outputLayer)
        chords[i*noteParChord_n : (i+1)*noteParChord_n] = chordObj.chordNo

    return chords
