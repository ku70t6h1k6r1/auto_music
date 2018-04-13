# -*- coding: utf-8 -*-

import pyaudio
import wave
import threading
from time import sleep
#for test
import calculateBpm as bpm
import sys

CHUNK = 512


class AudioPlayer(object):
    """ A Class For Playing Audio """

    def __init__(self, audio_file, start_frame_idx): #setPosあるからいらんかも
        self.audio_file = audio_file
        self.s_f_idx = start_frame_idx
        self.playing = threading.Event()    # 再生中フラグ

    def callback(self, in_data, frame_count, time_info, status):
        print(frame_count)
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def run(self):
        """ Play audio in a sub-thread """
        audio = pyaudio.PyAudio()
        input = wave.open(self.audio_file, "rb")
        output = audio.open(format=audio.get_format_from_width(input.getsampwidth()),
                            channels=input.getnchannels(),
                            rate=input.getframerate(),
                            #stream_callback=self.callback, #test
                            output=True)

        input.setpos(self.s_f_idx)
        while self.playing.is_set():
            data = input.readframes(CHUNK)
            if len(data) > 0:
                # play audio
                output.write(data)
            else:
                # end playing audio
                self.playing.clear()

        # stop and close the output stream
        output.stop_stream()
        output.close()
        # close the input file
        input.close()
        # close the PyAudio
        audio.terminate()

    def play(self):
        """ Play audio. """
        if not self.playing.is_set():
            self.playing.set()
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def wait(self):
        if self.playing.is_set():
            self.thread.join()

    def stop(self):
        """ Stop playing audio and wait until the sub-thread terminates. """
        if self.playing.is_set():
            self.playing.clear()
            self.thread.join()

    def setPos(self, start_frame_idx):
        self.s_f_idx = start_frame_idx

if __name__ == "__main__":
    #for test part
    bpmObj =  bpm.calBpm(r'C:\\work\\ai_music\\freesound\\yukio_mishima_l.wav')
    player1 = AudioPlayer(r'C:\\work\\ai_music\\freesound\\yukio_mishima_l.wav',0)

    temp = 0
    pos = bpmObj[2][0]
    try:
        for i in pos:
            player1.stop()
            player1.setPos(i)
            player1.play()
            sleep(1)
            print(i - temp)
            temp = i
        player1.stop()
    except KeyboardInterrupt:
        player1.stop()
        sys.exit
