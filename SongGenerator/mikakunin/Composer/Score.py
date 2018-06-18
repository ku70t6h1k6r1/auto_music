# coding:utf-8
from Composer import Section as sct
from Composer import ChordProgression as cp
from Composer import Melody as mel
from Composer import Drums as dr
from Composer import Bass as bs
from Composer import VoiceProgression as vp
from Composer.common import CommonSettings as cs

import json
import os

"""
1.ChordProgression
2.Melody
3.Drums
4.Bass
5.VoiceProgression

"""


class Score:
    def __init__(self):
        self.sctObj = sct.Section()
        self._chordProgressionObj = cp.ChordProgression()
        self._melodyObj = mel.Melody()
        self._drumObj = dr.Drums()
        self._bassObj = bs.Bass()
        self._VoiceProgressionObj = vp.VoiceProgression()

    def load(self, dir = './Composer/json/test.json'):
        name = os.path.dirname(os.path.abspath(__name__))
        joined_path = os.path.join(name, dir)
        data_path = os.path.normpath(joined_path)

        score_json = json.load(open(data_path, 'r'))

        form = score_json['form']
        formObj = self.sctObj.create(form['name'])
        for i, scoreObj in enumerate(sorted(set(formObj), key = formObj.index)):
            self._chordProgressionObj.create(scoreObj, score_json[form['args'][i]]['ChordProgression']['name'], **score_json[form['args'][i]]['ChordProgression']['args'])
            self._chordProgressionObj.update(scoreObj, score_json[form['args'][i]]['ChordProgressionChild']['name'])
            self._melodyObj.create(scoreObj, score_json[form['args'][i]]['Melody']['name'], score_json[form['args'][i]]['Melody']['range'],  **score_json[form['args'][i]]['Melody']['args'])
            self._drumObj.create(scoreObj, score_json[form['args'][i]]['Drums']['name'])
            self._bassObj.create(scoreObj, score_json[form['args'][i]]['Bass']['name'], score_json[form['args'][i]]['Bass']['range'])
            self._VoiceProgressionObj.create(scoreObj, score_json[form['args'][i]]['VoiceProgression']['name'], score_json[form['args'][i]]['VoiceProgression']['range'], **score_json[form['args'][i]]['VoiceProgression']['args'])

        masterScoreObj = cs.Score()
        for j, scoreObj in enumerate(formObj):
            masterScoreObj.addScoreObj(scoreObj)

        return masterScoreObj

    def create(self):
        formObj = self.sctObj.create("ab")
        for i, scoreObj in enumerate(sorted(set(formObj), key = formObj.index)):
            if i == 0:
                self._chordProgressionObj.create(scoreObj, self._chordProgressionObj.cherry, **{'rotate':-1, 'keyMm':[0,1], 'chordDeg':[0,5]})
                self._melodyObj.create(scoreObj, self._melodyObj.cherryA, range = [69,101],  **{'reverce':False})
                self._drumObj.create(scoreObj, self._drumObj.random)
                self._bassObj.create(scoreObj, self._bassObj.synchroniseKick, range = [28,60])
                self._VoiceProgressionObj.create(scoreObj, self._VoiceProgressionObj.triad, [45,80], **{'subMethodName':self._VoiceProgressionObj.synchroniseBass})
            else :
                self._chordProgressionObj.create(scoreObj, self._chordProgressionObj.cherry, **{'rotate':-1, 'keyMm':[1,0], 'chordDeg':[0,4]})
                self._chordProgressionObj.update(scoreObj, self._chordProgressionObj.cherryB)
                self._melodyObj.create(scoreObj, self._melodyObj.cherryB, range = [69,93],  **{'reverce':True})
                self._drumObj.create(scoreObj, self._drumObj.random)
                self._bassObj.create(scoreObj, self._bassObj.eightBeat, range = [28,40])
                self._VoiceProgressionObj.create(scoreObj, self._VoiceProgressionObj.powerChord, [45,80], **{'subMethodName':self._VoiceProgressionObj.eightBeat})

        masterScoreObj = cs.Score()
        for i, scoreObj in enumerate(formObj):
            masterScoreObj.addScoreObj(scoreObj)

        return masterScoreObj

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
