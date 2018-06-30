# coding:utf-8
import numpy as np

class Mixer:
    def __init__(self):
        self._methodObject = Methods()
        self._setMethodName()

    def _setMethodName(self):
        self.default = 'default'
        self.demo20180702 = 'demo20180702'
        self.pattern1 = 'pattern1'

    def create(self, formObj, methodName):
        if methodName == self.default:
            return self._methodObject.default(formObj)
        elif methodName == self.pattern1:
            return self._methodObject.pattern1(formObj)
        elif methodName == self.demo20180702:
            return self._methodObject.demo20180702(formObj)


class Methods:
    def __init__(self):
        return None

    def default(self, section):
        all_on = {'melodyLine':True, 'bassLine':True, 'voiceProg':True, 'drums':False}
        output = []
        for num in section:
            output.append(all_on)

        return output

    def demo20180702(self, section):
        all_on = {'melodyLine':True, 'bassLine':True, 'voiceProg':True, 'drums':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'bassLine':False, 'voiceProg':False, 'drums':False}
            output[1] = {'melodyLine':False, 'bassLine':False, 'voiceProg':False, 'drums':True}
            output[2] = {'melodyLine':True, 'bassLine':True, 'voiceProg':True, 'drums':True}
            output[3] = {'melodyLine':False, 'bassLine':True, 'voiceProg':False, 'drums':True}
            output[-1] = {'melodyLine':False, 'bassLine':False, 'voiceProg':True, 'drums':True}
        return output

    def pattern1(self, section):
        all_on = {'melodyLine':True, 'bassLine':True, 'voiceProg':True, 'drums':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'bassLine':False, 'voiceProg':False, 'drums':True}
            output[1] = {'melodyLine':True, 'bassLine':True, 'voiceProg':True, 'drums':True}
            output[2] = {'melodyLine':True, 'bassLine':True, 'voiceProg':False, 'drums':True}
            output[-1] = {'melodyLine':False, 'bassLine':False, 'voiceProg':True, 'drums':True}
        return output
