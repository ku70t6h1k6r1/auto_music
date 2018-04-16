# coding: UTF-8
import numpy as np
import common_function as func

def pickUpAccent(melody, notePerBar_n = 16):
    output = np.zeros(0)
    oneBar = np.zeros(len(melody))

    for j in range(int(len(melody)/notePerBar_n)):
        for i in range(notePerBar_n):
            if melody[notePerBar_n*j + i] != -1:
                oneBar[notePerBar_n*j + i] = oneBar[notePerBar_n*j + i]  + 1
    output = np.r_[output, func.softmax(oneBar)]
    return output

def pickUpSectionAccent(melody, notePerBar_n = 16, barsPerOneSection = 4):
    output = np.zeros(0)
    oneBar = np.zeros(notePerBar_n)

    # minimum beat length sixteen-beat and then 16
    for j in range(int(len(melody)/notePerBar_n)):
        for i in range(notePerBar_n):
            if melody[j*notePerBar_n + i] != -1:
                oneBar[i] = oneBar[i]  + 1
        if j % barsPerOneSection == barsPerOneSection - 1:
            for k in range(barsPerOneSection):
                output = np.r_[output, func.softmax(oneBar)] #ランダム性はコントロールできる。*3でいけないのか。
            oneBar = np.zeros(notePerBar_n)
    return output

def Create(melody, notePerBar_n = 16, barsPerOneSection = 4, temperature = 0.0005):
    merge =  pickUpAccent(melody, notePerBar_n) * pickUpSectionAccent(melody, notePerBar_n, barsPerOneSection)

    output = np.zeros(0)
    oneBar = np.zeros(notePerBar_n)

    for j in range(int(len(merge)/notePerBar_n )):
        for i in range(notePerBar_n ):
            oneBar[i] = merge[j*notePerBar_n  + i]
        output = np.r_[output, func.softmax(oneBar, t = temperature)] #0.0005がちょうどよい
        oneBar = np.zeros(notePerBar_n )
    return output


#print "#############"
#melody = create()
#merge(pickUpAccent(melody), pickUpSecAccent(melody))
