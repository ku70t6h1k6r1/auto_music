# coding:utf-8
import numpy as np

class Mixer:
    def __init__(self):
        self._methodObject = Methods()
        self._setMethodName()

    def _setMethodName(self):
        self.default = 'default'
        self.test = 'test'
        self.demo20180702 = 'demo20180702'
        self.demo20180716 = 'demo20180716'
        self.pattern1 = 'pattern1'
        self.edm1 = 'edm1'
        self.edm2 = 'edm2'
        self.edm3 = 'edm3'
        self.edm4 = 'edm4'
        self.edm5 = 'edm5'

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
        elif methodName == self.edm2:
            return self._methodObject.edm2(formObj)
        elif methodName == self.edm3:
            return self._methodObject.edm3(formObj)
        elif methodName == self.edm4:
            return self._methodObject.edm4(formObj)
        elif methodName == self.edm5:
            return self._methodObject.edm5(formObj)
        elif methodName == self.test:
            return self._methodObject.test(formObj)


class Methods:
    def __init__(self):
        return None

    def default(self, section):
        all_on = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        return output

    def test(self, section):
        all_on = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':False}
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
            output[1] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':False, 'voiceProg':True, 'drums':False, 'effects':True}
            output[2] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[3] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True}
            output[4] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':False, 'drums':True, 'effects':True}
            output[5] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[6] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[-2] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':False, 'voiceProg':False, 'drums':True, 'effects':True}
            output[-1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':False}
        return output

    def edm2(self, section):
        all_on = {'melodyLine':True, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True}
            output[1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':True, 'drums':False, 'effects':True}
            output[2] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[3] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[4] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[5] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':False, 'voiceProg':False, 'drums':True, 'effects':True}
        return output

    def edm3(self, section): #[p,a,a,s,i,b,b,i,s]
        all_on = {'melodyLine':True, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 3:
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True} #p
            output[1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True} #a
            output[2] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True} #a
            output[3] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True} #s i
            output[5] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True} #b
            output[6] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True} #b
            output[-2] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':True, 'effects':True}
            output[-1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':False}
        return output

    def edm4(self, section): #[p,a,s,b,b,i,s]
        all_on = {'melodyLine':True, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 0:
            #p
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True}

            #a
            output[1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}

            #s
            output[2] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':True}

            #b
            output[3] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}
            output[4] = {'melodyLine':False, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'drums':True, 'effects':True}

            #i
            output[5] = {'melodyLine':True, 'melodyLine2':False, 'bassLine':True, 'voiceProg':False, 'drums':True, 'effects':True}

            #s
            output[6] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'drums':False, 'effects':False}
        return output

    def edm5(self, section): #[p,a,s,b,i,s]
        all_on = {'melodyLine':True, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'voiceProg2':True, 'drums':True, 'effects':True}
        output = []
        for num in section:
            output.append(all_on)

        if len(section) > 0:
            #p
            output[0] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'voiceProg2':False, 'drums':False, 'effects':True}

            #a
            output[1] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'voiceProg2':True, 'drums':True, 'effects':True}

            #s
            output[2] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'voiceProg2':False, 'drums':False, 'effects':True}

            #b
            output[3] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':True, 'voiceProg':True, 'voiceProg2':False, 'drums':True, 'effects':True}

            #i
            output[4] = {'melodyLine':True, 'melodyLine2':True, 'bassLine':True, 'voiceProg':True, 'voiceProg2':True, 'drums':True, 'effects':True}

            #s
            output[5] = {'melodyLine':False, 'melodyLine2':False, 'bassLine':False, 'voiceProg':False, 'voiceProg2':False, 'drums':False, 'effects':False}
        return output
