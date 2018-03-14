# coding: UTF-8
import numpy as np
import common_function as func

class Chord:
    def __init__(self):
        self.IM7 = [0,4,11]
        self.I7 = [0,4,10]
        self.Isus4M7 = [0,5,11]
        self.Isus47 = [0,5,10]
        self.Im7 = [0,3,10]
        self.ImM7 = [0,3,11]
        self.Imb57= [0,3,10]
        self.Idim7 = [0,3,9]

        self.tones = []

        for i in range(12):
            tempChordTones = []
            tempChordTones.append(self.convertNote(self.IM7,i))
            tempChordTones.append(self.convertNote(self.I7,i))
            tempChordTones.append(self.convertNote(self.Isus4M7,i))
            tempChordTones.append(self.convertNote(self.Isus47,i))
            tempChordTones.append(self.convertNote(self.Im7,i))
            tempChordTones.append(self.convertNote(self.ImM7,i))
            tempChordTones.append(self.convertNote(self.Imb57,i))
            tempChordTones.append(self.convertNote(self.Idim7,i))
            self.tones.append(tempChordTones) #numpyじゃなくてよいか

    def convertNote(self, notes,num):
        outputNotes = []
        for i in range(len(notes)):
            if notes[i] + num > 11:
                outputNotes.append(notes[i] + num - 12)
            else:
                outputNotes.append(notes[i] + num)
        return outputNotes

#TEST
#test = Chord()
#print test.tones
