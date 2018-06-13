# coding: UTF-8

def midiNoteToHz(midiNote):
    # ref:https://drumimicopy.com/audio-frequency/
    return 440 * 2**( (midiNote - 69)/12 )

def a16beatToSec( bpm):
    return 60/bpm/4
