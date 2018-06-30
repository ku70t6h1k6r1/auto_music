        if instName == 'bass':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sine], [1.0, 0.5], [1.0, 2.0], aSynthe.FilterName.bandpass, [1,9000], [0.001, 0.02, 0.9, 0.01], 44100)
        if instName == 'lead':
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandpass, [1000,12000], [0.05, 0.01, 0.4, 0.01], 44100)
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.square], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandcut, [5000,12000], [0.03, 0.2, 0.1, 0.01], 44100)
        if instName == 'lead2':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.square], [1.0, 0.8], [1.02, 1.02], aSynthe.FilterName.bandpass, [10000, 12000], [0.05, 0.01, 0.4, 0.01], 44100)
            #self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sawtooth, aSynthe.Waveform.sine], [1.0, 0.8], [1.0, 1.02], aSynthe.FilterName.bandcut, [5000,12000], [0.03, 0.2, 0.1, 0.01], 44100)
        #elif instName == 'voice':
        #    self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.05], [1.0, 0.01], aSynthe.FilterName.bandpass, [10,10000], [0.001, 0.02, 0.6, 0.2], 44100)
        elif instName == 'voice':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.sine, aSynthe.Waveform.sawtooth], [1.0, 0.8], [1.0, 2.02], aSynthe.FilterName.bandpass, [50,1200], [0.0, 0.1, 0.8, 0.1], 44100)
        elif instName == 'kick':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0, 0.8], [1.0, 0.0], aSynthe.FilterName.lowpass, [200], [0.001, 0.02, 0.1 ,0.1], 44100)
        elif instName == 'snare':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.square], [1.0, 1.0], [1.0, 0.5], aSynthe.FilterName.bandcut, [5,100], [0.0, 0.02, 0.002, 0.1], 44100)
        elif instName == 'hihat':
            self.synthesizer = aSynthe.Synthesizer([aSynthe.Waveform.whitenoise, aSynthe.Waveform.sawtooth], [1.0,0.2], [1.0,0.0], aSynthe.FilterName.highpass, [7000], [0.0, 0.01, 0.001, 0.01], 44100)
