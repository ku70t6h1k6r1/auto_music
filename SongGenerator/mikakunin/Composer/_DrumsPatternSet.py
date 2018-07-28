# coding: UTF-8
#default
import numpy as np
from Composer.common import CommonSettings as cs

class Fills:
    def __init__(self):
        self.list = []

        #Fours
        instObj = cs.Drums()
        instObj.setHihat([-2,-1,-1,-1,  -1,-1,-1,-1,    -1,-1,-1,-1,    -1,-1,-1,-1], True)
        instObj.setSnare([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        self.list.append(instObj)

        #Eights
        instObj = cs.Drums()
        instObj.setHihat([-2,-1,-1,-1,  -1,-1,-1,-1,    -1,-1,-1,-1,    -1,-1,-1,-1], True)
        instObj.setSnare([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setKick([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        self.list.append(instObj)

        #Sixteens
        instObj = cs.Drums()
        instObj.setHihat([-2,-1,-1,-1,  -1,-1,-1,-1,    -1,-1,-1,-1,    -1,-1,-1,-1], True)
        instObj.setSnare([0,0,0,0,  0,0,0,0,    0,0,0,0,    0,0,0,0], True)
        instObj.setKick([0,0,0,0,  0,0,0,0,    0,0,0,0,    0,0,0,0], True)
        self.list.append(instObj)

class Patterns:
    def __init__(self):
        self.list = []

        #Rock Beat
        instObj = cs.Drums()
        instObj.setHihat([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,0,-1,    -1,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        #Funk Beat
        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,0,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,-1,0,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,0,0,0,  0,0,0,0,    0,0,0,0,    0,0,0,0], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)



        #Dance Beat
        instObj = cs.Drums()
        instObj.setHihat([-1,0,-1,0,  -1,0,-1,0,    -1,0,-1,0,    -1,0,-1,0], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,-1,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,0,0,0,  0,0,0,0,    0,0,0,0,    0,0,0,0], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,-1,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([-1,0,-1,0,  -1,0,-1,0,    -1,0,-1,0,    -1,0,-1,0], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,0,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,-1,0,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,1,-1,  0,-1,1,-1,    0,-1,1,-1,    0,-1,1,-1], True)
        instObj.setSnare([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        self.list.append(instObj)

        #Punk beat
        instObj = cs.Drums()
        instObj.setHihat([0,-1,1,-1,  0,-1,1,-1,    0,-1,1,-1,    0,-1,1,-1], True)
        instObj.setSnare([-1,-1,0,-1,  -1,-1,0,-1,    -1,-1,0,-1,    -1,-1,0,-1], True)
        instObj.setKick([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,1,-1,  0,-1,1,-1,    0,-1,1,-1,    0,-1,1,-1], True)
        instObj.setSnare([-1,-1,0,-1,  -1,-1,0,-1,    -1,-1,0,-1,    -1,-1,0,-1], True)
        instObj.setKick([0,-1,-1,-1,  0,0,-1,-1,    0,-1,-1,-1,    0,0,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,1,-1,  0,-1,1,-1,    0,-1,1,-1,    0,-1,1,-1], True)
        instObj.setSnare([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([-1,-1,-0,-1,  -1,-1,0,-1,    -1,-1,0,-1,    -1,-1,0,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,1,-1,  0,-1,1,-1,    0,-1,1,-1,    0,-1,1,-1], True)
        instObj.setSnare([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([-1,-1,-0,-1,  -1,-1,0,-1,    -1,-1,0,0,    -1,-1,0,-1], True)
        self.list.append(instObj)

        """
        #打ち込み系は下の参照
        https://www.youtube.com/watch?v=tm2BgO1VaRY
        https://docs.google.com/spreadsheets/d/19_3BxUMy3uy1Gb0V8Wc-TcG7q16Amfn6e8QVw4-HuD0/edit#gid=0
        """

        #Breakbeats
        #8step
        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    0,-1,-1,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,0,    -1,-1,-1,-1,    0,-1,-1,0], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,-1,-1,    0,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        #16step
        instObj = cs.Drums()
        instObj.setHihat([0,0,0,0,  0,0,0,0,    0,0,0,0,    0,0,0,0], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,0,    -1,0,-1,0,    0,-1,-1,0], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,0,-1,    -1,-1,0,-1,    -1,0,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,0,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,0,    0,-1,-1,-1,    -1,-1,0,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,0,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,0,    0,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,-1,-1,    -1,-1,0,0,    -1,-1,-1,0], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,0,  -1,-1,0,-1,    0,-1,-1,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,0,-1,    -1,0,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        #32step
        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,0,    0,-1,0,-1,    0,-1,0,0], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    -1,-1,0,-1,    -1,0,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,-1,-1,  0,-1,0,0,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,0,    -1,0,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,0,  -1,-1,-1,-1,    -1,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,-1,0,    -1,0,0,0,    -1,-1,-1,0], True)
        self.list.append(instObj)

        #64step
        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-0,    -1,0,-1,-1,    0,-1,-1,0], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,-1,-1,    -1,-1,0,0,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-0,    -1,0,-1,-1,    -1,-1,0,-1], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,-1,-1,    -1,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,0,-1,-1,  0,-1,-1,-0,    -1,0,-1,-1,    -1,-1,0,-1], True)
        instObj.setKick([-1,-1,0,0,  -1,-1,-1,-1,    -1,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,0,-1,-1,  0,-1,-1,-1,    -1,0,-1,-1,    0,-1,-1,0], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,-1,    -1,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,0,-1,-1,    0,-1,-1,0], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,-1,-1,    -1,-1,0,-1,    -1,-1,-1,-1], True)
        self.list.append(instObj)

        #Rock
        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,0,-1,  -1,-1,0,-1,    0,-1,0,-1,    -1,-1,0,-1], True)
        self.list.append(instObj)

        #Techno
        instObj = cs.Drums()
        instObj.setHihat([-1,-1,0,-1,  -1,-1,0,-1,    -1,-1,0,-1,    -1,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,0,-1], True)
        self.list.append(instObj)

        #HipHop
        instObj = cs.Drums()
        instObj.setHihat([0,-1,0,-1,  0,-1,0,-1,    0,-1,0,-1,    0,-1,0,-1], True)
        instObj.setSnare([-1,-1,-1,-1,  0,-1,-1,-1,    -1,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setKick([0,-1,-1,-1,  -1,-1,-1,0,    -1,-1,0,-1,    -1,0,-1,0], True)
        self.list.append(instObj)

        #Yotsu-uchi
        instObj = cs.Drums()
        instObj.setHihat([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        instObj.setSnare([-1,-1,0,-1,  -1,-1,0,-1,    -1,-1,0,-1,    -1,-1,0,-1], True)
        instObj.setKick([0,-1,-1,-1,  0,-1,-1,-1,    0,-1,-1,-1,    0,-1,-1,-1], True)
        self.list.append(instObj)

if __name__ == '__main__':
     ptn = Patterns()
     print(ptn.list)
