import librosa
import numpy as np
import os
import pyaudio
import wave as wv
from datetime import datetime

class Processing:
    def __init__(self, outPath):
        self.audio  = pyaudio.PyAudio()
        self.outputDir = outPath

    def execute(self, dir, proc, backtrack=True, multiple = False):

        #諸々の設定変えられないようにハードコーディング
        self._backtrack=backtrack
        y, sr = librosa.load(dir, sr=44100, mono=True)
        y = librosa.util.normalize(y) #normalize the sound

        if multiple:
            if proc == 'trim':
                yts = self.trim(y, sr, self._backtrack)
                fileName_list = []

                for yt in yts :
                    yt_bin = self.toBytes(yt)

                    directory, filename = os.path.split(dir)
                    name, ext = os.path.splitext(filename)
                    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
                    num = str(np.random.randint(1000))
                    fileName = name + '_proc_' + dt + '_'  + num + '.wav'

                    waveFile = wv.open(self.outputDir + fileName , 'wb')
                    waveFile.setnchannels(1)
                    waveFile.setsampwidth(2)
                    waveFile.setframerate(44100)
                    waveFile.writeframes(yt_bin)
                    waveFile.close()

                    fileName_list.append(fileName)
                return fileName_list

        else:
            if proc == 'trim':
                yt = self.trim_s(y, sr, self._backtrack)
                directory, filename = os.path.split(dir)
                name, ext = os.path.splitext(filename)
                dt = datetime.now().strftime("%Y%m%d_%H%M%S")
                num = str(np.random.randint(1000))
                fileName = name + '_proc_' + 'max_' + dt + '_'  + num + '.wav'

            elif proc == 'onset':
                yt = self.onset(y, sr)
                directory, filename = os.path.split(dir)
                name, ext = os.path.splitext(filename)
                dt = datetime.now().strftime("%Y%m%d_%H%M%S")
                num = str(np.random.randint(1000))
                fileName = name + '_proc_' + 'onset_' + dt + '_'  + num + '.wav'

            yt_bin = self.toBytes(yt)

            waveFile = wv.open(self.outputDir + fileName , 'wb')
            waveFile.setnchannels(1)
            waveFile.setsampwidth(2)
            waveFile.setframerate(44100)
            waveFile.writeframes(yt_bin)
            waveFile.close()

            return [fileName]

    def toBytes(self, wave):
        return (wave * float(2 ** (16 - 1) ) ).astype(np.int16).tobytes()

    def trim(self, y, sr, backtrack):
        yt = y
        yt_mono = yt

        onsets = np.array(librosa.onset.onset_detect(y=yt_mono, sr=sr, backtrack=backtrack, units="samples"))
        onsets_diff  = np.diff(onsets)
        onsets_diff_long =  np.where(onsets_diff > 0.2 * sr)  #本当は<にしてインデックスを＋1したい
        onsets = onsets[onsets_diff_long]

        segments = [yt_mono[onsets[idx]:onsets[idx+1]] for idx in range(len(onsets)-1)]

        return segments


    def onset(self, y, sr):
        yt = y
        if len(yt.shape) == 2:
            yt_mono = (yt[0]+yt[1])/2
        else:
            yt_mono = yt
        onsets = librosa.onset.onset_detect(y=yt_mono, sr=sr, backtrack=False, units="samples")


        if len(yt.shape) == 2:
            yt = yt[:, onsets[0]:len(yt)]
        else:
            yt = yt[onsets[0]:len(yt)]
        return yt

    def trim_s(self, y, sr, backtrack):
        """
        Segments according to onsets, then returns the loudest segment
        Cuts very sharply, for a rougher cut use trim_audio
        """
        yt = y
        if len(yt.shape) == 2:
            yt_mono = (yt[0]+yt[1])/2
        else:
            yt_mono = yt
        onsets = librosa.onset.onset_detect(y=yt_mono, sr=sr, backtrack=backtrack, units="samples")
        onsets = np.insert(onsets, 0, 0)
        #find the loudest segment (maybe rmse should be used instead of energy)
        segments = [yt_mono[onsets[idx]:onsets[idx+1]] for idx in range(len(onsets)-1)]
        powers = [np.sum(segment**2) for segment in segments]
        max_idx = np.argmax(powers)

        #append subsequent segments in case output is too short (<0.1sec)
        dur = (onsets[max_idx+1] - onsets[max_idx])/sr
        idx = max_idx
        while dur < 0.1 and idx+1 < len(onsets)-1:
            idx += 1
            dur += (onsets[idx+1] - onsets[idx])/sr

        if len(yt.shape) == 2:
            yt = yt[:, onsets[max_idx]:onsets[idx+1]]
        else:
            yt = yt[onsets[max_idx]:onsets[idx+1]]
        return yt

if __name__ == '__main__' :
    #proc = Processing('C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/test/')
    #proc.execute('C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/vowel_normal.wav', 'onset', False, False)
    proc = Processing('C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/20180728/')
    proc.execute('C:/Users/hikari.kubota/Documents/GitHub/auto_music/SongGenerator/mikakunin/wav/sample/20180728/8266436665974_tired.m4a', 'onset', False, False)
