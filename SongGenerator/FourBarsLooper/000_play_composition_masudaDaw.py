# -*- coding: utf-8 -*-
import numpy as np
import createLeadSheet as ls
import common_function as func
import createSequencer as stepSeqs
import pygame.midi
from time import sleep
import time
from multiprocessing import Process, Queue, Value, Array
import multiprocess_function as mltPrcss


if __name__ == '__main__':
    #load lead sheet
    leadSheet = ls.composition_MasudaDaw()
    rehA_length = leadSheet.a_onePhrase_bars * leadSheet.a_loop * leadSheet.notePerBar_n

    # articulation
    articuration = leadSheet.articuration

    # parse section
    melody = leadSheet.leadLine
    melody_wav = leadSheet.leadLine_wav
    melody_dur = leadSheet.leadLine_dur
    print(melody)
    chords = leadSheet.chordProgress
    counterMelody = leadSheet.counterMelody
    print(counterMelody)

    ba = leadSheet.ba
    v1 = leadSheet.v1
    v2 = leadSheet.v2

    bDr = leadSheet.baDrum
    sDr = leadSheet.snare
    cHH = leadSheet.hiHat

    #ADD MASUDA
    mHH = leadSheet.mHH
    mSn = leadSheet.mSn
    mBD = leadSheet.mBD

    #Make Each Channel
    melody = np.stack([melody], axis = -1)
    mel_articulation = np.stack([articuration *100], axis = -1)

    melody_wav = np.stack([melody_wav], axis = -1)

    ba = np.stack([ba], axis = -1)
    ba_articulation  = np.stack([articuration *80], axis = -1)

    vc = np.stack([v1, v2 ], axis = -1)
    vc_articuration = np.stack([articuration*80 ,articuration*80], axis = -1)

    dr = np.stack([cHH, sDr ,bDr], axis = -1)
    dr_articuration = np.stack([articuration*90, articuration*80 ,articuration*80], axis = -1)

    mDr = np.stack([mHH, mSn ,mBD], axis = -1)
    dr_articuration = np.stack([articuration*90, articuration*80 ,articuration*80], axis = -1)

    cMelody = np.stack([counterMelody], axis = -1)
    cMel_articuration = np.stack([articuration*70], axis = -1)

    #For Shared Memory
    pointer_Perc = mltPrcss.Value('i', 0)
    pointer_Harm = mltPrcss.Value('i', 0)
    currentBeat = mltPrcss.Value('i', 0)

    playFlg_mel = mltPrcss.Value('i', 0)
    playFlg_cMel = mltPrcss.Value('i', 0)
    playFlg_ba = mltPrcss.Value('i', 0)
    playFlg_vc = mltPrcss.Value('i', 0)
    playFlg_dr = mltPrcss.Value('i', 0)
    playFlg_mDr = mltPrcss.Value('i', 0)

    #SecA
    stepSeqObj = stepSeqs.Sequencer(0)
    stepSeqObj.create_stepSequencer(1,2)

    rythm_seq = stepSeqObj.rythm_seq
    harmony_seq = stepSeqObj.harmony_seq
    mel_seq_onoff = stepSeqObj.harmony_seq_OnOff
    cMel_seq_onoff = stepSeqObj.etc1_seq_OnOff
    ba_seq_onoff = stepSeqObj.harmony_seq_OnOff
    vc_seq_onoff = stepSeqObj.harmony_seq_OnOff
    dr_seq_onoff = stepSeqObj.rythm_seq_OnOff
    mDr_seq_onoff = stepSeqObj.rythm_seq_OnOff

    seq = mltPrcss.StepSequencer( [pointer_Harm, pointer_Perc], \
                                    np.stack([harmony_seq, rythm_seq], axis = -1), \
                                    [playFlg_mDr, playFlg_dr, playFlg_mel, playFlg_ba, playFlg_vc, playFlg_cMel], \
                                    np.stack([mDr_seq_onoff, dr_seq_onoff, mel_seq_onoff, ba_seq_onoff, vc_seq_onoff, cMel_seq_onoff], axis = -1) \
                                )

    # multiprocessing setting
    timeSeriesObj = mltPrcss.TimeSeries()
    timeSeriesObj.setBpm(leadSheet.bpm)
    print(leadSheet.bpm)
    print("SET START TIME")
    timeSeriesObj.setStartTime(time.time())
    device = 0    #device = 3 #microX
    port = 3001 # For Masuda Daw

    sp_melody_wav =  mltPrcss.ChildProcessWave(leadSheet.wav_dir, melody_dur, pointer_Harm , currentBeat, melody_wav, mel_articulation, timeSeriesObj, playFlg_mel)
    sp_cMelody =  mltPrcss.ChildProcess(device, 3, 5, pointer_Harm, currentBeat, cMelody, cMel_articuration, timeSeriesObj, playFlg_cMel)
    sp_ba =  mltPrcss.ChildProcess(device, 1, 5, pointer_Harm, currentBeat, ba, ba_articulation, timeSeriesObj, playFlg_ba)
    sp_vc =  mltPrcss.ChildProcess(device, 2, 5, pointer_Harm, currentBeat, vc, vc_articuration, timeSeriesObj, playFlg_vc)
    sp_dr = mltPrcss.ChildProcess(device, 9, 0, pointer_Perc, currentBeat, dr, dr_articuration, timeSeriesObj, playFlg_dr)
    sp_mDr = mltPrcss.ChildProcessMasudaDaw(port, 9, 0, pointer_Perc, currentBeat, dr, dr_articuration, timeSeriesObj, playFlg_dr)


    #execute
    p_seq =  mltPrcss.Process(target = seq.execute, args=(timeSeriesObj, currentBeat) )
    p1 = mltPrcss.Process(target = sp_melody_wav .execute)
    p2 = mltPrcss.Process(target = sp_ba.execute)
    p3 = mltPrcss.Process(target = sp_vc.execute)
    p4 = mltPrcss.Process(target = sp_cMelody.execute)
    p5 = mltPrcss.Process(target = sp_mDr.execute)
    p8 = mltPrcss.Process(target = sp_dr.execute)

    #MAX 4process

    print("p_seq START")
    p_seq.start()
    print("p1 START")
    p1.start()
    print("p2 START")
    p2.start()
    print("p3 START")
    p3.start()
    print("p4 START")
    p4.start()
    print("p5 START")
    p5.start()
    """
    print("p6 START")
    p6.start()
    """
    print("p8 START")
    p8.start()

    p_seq.join()
    sleep(2)
    p1.terminate()
    p2.terminate()
    p3.terminate()
    p4.terminate()
    p5.terminate()
    """
    p6.join()
    """
    p8.terminate()
