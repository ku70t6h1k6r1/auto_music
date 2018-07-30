# coding:utf-8
import numpy as np

class Mixer:
    def __init__(self):
        self._methodObject = Methods()
        self._setMethodName()

    def _setMethodName(self):
        self.default = 'default'
        self.demo20180702 = 'demo20180702'
        self.demo20180716 = 'demo20180716'
        self.pattern1 = 'pattern1'
        self.edm1 = 'edm1'

    def create(self, formObj, methodName):
        if methodName == self.default:
            return self._methodObject.default(formObj)
        elif methodName == self.pattern1:
            return self._methodObject.pattern1(formObj)
        elif methodName == self.demo20180702:
            return self._methodObject.demo20180702(formObj)
        elif methodName == self.demo20180716:
            return self._methodObject.demo20180716(formObj)
        elif methodName == self.edm1:
            return self._methodObject.edm1(formObj)


class Methods:
    def __init__(self):
        return None

    def default(self, section):
        all_on = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        return output

    def demo20180702(self, section):
        all_on = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True}
            output[1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':False, 'drums':True, 'effects':True}
            output[2] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':False}
            output[3] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':False, 'drums':True, 'effects':True}
            output[-1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':True, 'drums':True, 'effects':True}
        return output

    def demo20180716(self, section):
        all_on = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[1] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':False, 'drums':True, 'effects':True}
            output[2] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[-1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        return output

    def pattern1(self, section):
        all_on = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':True, 'effects':True}
            output[1] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[2] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':False, 'drums':True, 'effects':True}
            output[-1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':True, 'drums':True, 'effects':True}
        return output

    def edm1(self, section):
        all_on = {'melodyLine':True, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True}
            output[1] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':False, 'voiceProg':True, 'drums':False, 'effects':True}
            output[2] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[3] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True}
            output[4] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':False, 'drums':True, 'effects':True}
            output[5] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[6] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[-2] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':False, 'voiceProg':False, 'drums':True, 'effects':True}
            output[-1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':False}
        return output
