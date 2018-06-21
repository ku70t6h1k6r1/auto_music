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

    def load(self, dir):
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

    def create(self, settingsDir):
        name = os.path.dirname(os.path.abspath(__name__))
        joined_path = os.path.join(name, settingsDir)
        data_path = os.path.normpath(joined_path)
        settings = json.load(open(data_path, 'r'))

        ChordProgression = {}
        for element in settings["ChordProgression"]:
            print(element["name"])


if __name__ == '__main__':
    scoreObj = Score()
    scoreObj.create('./Composer/settings/default.json')
