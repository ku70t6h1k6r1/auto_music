# coding:utf-8
from Composer import Section as sct

class Score:
    def create(self):
        sectionObj = sct.Section()
        song = sectionObj.create(sectionObj.defaultChoise)
        return song

if __name__ == '__main__':
    sectionObj = sct.Section()
    song = sectionObj.create(sectionObj.defaultChoise)
    print(song.chordProg)
    print(song.melodyLine)
    print(song.voiceProg)
    print(song.bassLine)

    #DRUM
    print("DRUM")
    print(song.drumObj.hihat)
    print(song.drumObj.snare)
    print(song.drumObj.kick)
