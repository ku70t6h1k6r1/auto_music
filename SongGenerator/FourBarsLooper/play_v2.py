# -*- coding: utf-8 -*-
import numpy as np
import createLeadSheet as ls
import common_function as func
#import chord_voices as cv
#import harmonize_tf as hm
import createSequencer as stepSeqs
import pygame.midi
from time import sleep
import time
from multiprocessing import Process, Queue, Value, Array
import multiprocess_function as mltPrcss

if __name__ == '__main__':
    #for TEST
    """
    pygame.init()
    pygame.midi.init()
    o = pygame.midi.Output(3)
    print(pygame.midi.get_count())
    print(pygame.midi.get_device_info(0))
    print(pygame.midi.get_device_info(1))
    print(pygame.midi.get_device_info(2))
    print(pygame.midi.get_device_info(3))
    for i in range(30):
        print("IN 60")
        o.note_on(60, 100 ,0)
        sleep(1)
    o.close()
    pygame.midi.quit()
    pygame.quit()
    exit()
    """

    #load lead sheet
    leadSheet = ls.SampleComposition()
    rehA_length = leadSheet.a_onePhrase_bars * leadSheet.a_loop * leadSheet.notePerBar_n
    rehB_length = leadSheet.b_onePhrase_bars * leadSheet.b_loop * leadSheet.notePerBar_n
    rehC_length = leadSheet.vamp_onePhrase_bars * leadSheet.vamp_loop * leadSheet.notePerBar_n
    start_rehC = rehA_length + rehB_length
    end_rehC = rehA_length + rehB_length + rehC_length + 1

    # articulation
    articuration = leadSheet.articuration #[0:rehA_length]

    # parse section
    melody = leadSheet.leadLine #[0:rehA_length]
    print(melody)
    chords = leadSheet.chordProgress #[0:rehA_length]
    counterMelody = leadSheet.counterMelody #[0:rehA_length]
    print(counterMelody)
    #chordObj = hm.Dataset()

    ba = leadSheet.ba #[0:rehA_length]
    v1 = leadSheet.v1 #[0:rehA_length]
    v2 = leadSheet.v2  #[0:rehA_length]

    bDr = leadSheet.baDrum #[0:rehA_length]
    sDr = leadSheet.snare #[0:rehA_length]
    cHH = leadSheet.hiHat #[0:rehA_length]

    #Make Each Channel
    melody = np.stack([melody], axis = -1)
    mel_articulation = np.stack([articuration *100], axis = -1)

    ba = np.stack([ba], axis = -1)
    ba_articulation  = np.stack([articuration *80], axis = -1)

    vc = np.stack([v1, v2 ], axis = -1)
    vc_articuration = np.stack([articuration*80 ,articuration*80], axis = -1)

    dr = np.stack([cHH, sDr ,bDr], axis = -1)
    dr_articuration = np.stack([articuration*90, articuration*80 ,articuration*80], axis = -1)

    cMelody = np.stack([counterMelody], axis = -1)
    cMel_articuration = np.stack([articuration*70], axis = -1)

    #For Shared Memory
    pointer_Perc = mltPrcss.Value('i', 0)
    pointer_Harm = mltPrcss.Value('i', 0)
    currentBeat = mltPrcss.Value('i', 0)

    playFlg_mel = mltPrcss.Value('i', 1)
    playFlg_cMel = mltPrcss.Value('i', 1)
    playFlg_ba = mltPrcss.Value('i', 1)
    playFlg_vc = mltPrcss.Value('i', 1)
    playFlg_dr = mltPrcss.Value('i', 1)

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

    #SecB
    stepSeqObj2 = stepSeqs.Sequencer(4*16)
    stepSeqObj2.create_stepSequencer(1,2)

    rythm_seq_B = stepSeqObj2.rythm_seq
    harmony_seq_B = stepSeqObj2.harmony_seq
    mel_seq_onoff_B = stepSeqObj2.harmony_seq_OnOff
    cMel_seq_onoff_B = stepSeqObj2.etc1_seq_OnOff
    ba_seq_onoff_B = stepSeqObj2.harmony_seq_OnOff
    vc_seq_onoff_B = stepSeqObj2.harmony_seq_OnOff
    dr_seq_onoff_B = stepSeqObj2.rythm_seq_OnOff

    rythm_seq = np.r_[rythm_seq, rythm_seq_B]
    harmony_seq = np.r_[harmony_seq, harmony_seq_B]
    mel_seq_onoff = np.r_[mel_seq_onoff, mel_seq_onoff_B]
    cMel_seq_onoff = np.r_[cMel_seq_onoff, cMel_seq_onoff_B]
    ba_seq_onoff = np.r_[ba_seq_onoff, ba_seq_onoff_B]
    vc_seq_onoff = np.r_[vc_seq_onoff, vc_seq_onoff_B]
    dr_seq_onoff = np.r_[dr_seq_onoff, dr_seq_onoff_B]



    seq = mltPrcss.StepSequencer( [pointer_Harm, pointer_Perc], \
                                    np.stack([harmony_seq, rythm_seq], axis = -1), \
                                    [playFlg_dr, playFlg_mel, playFlg_ba, playFlg_vc, playFlg_cMel], \
                                    np.stack([dr_seq_onoff, mel_seq_onoff, ba_seq_onoff, vc_seq_onoff, cMel_seq_onoff], axis = -1) \
                                )

    # multiprocessing setting
    timeSeriesObj = mltPrcss.TimeSeries()
    timeSeriesObj.setBpm(105)
    print("SET START TIME")
    timeSeriesObj.setStartTime(time.time())
    device = 0    #device = 3 #microX
    sp_melody =  mltPrcss.ChildProcess(device, 0, 1, pointer_Harm, currentBeat, melody, mel_articulation, timeSeriesObj, playFlg_mel)
    sp_cMelody =  mltPrcss.ChildProcess(device, 3, 5, pointer_Harm, currentBeat, cMelody, cMel_articuration, timeSeriesObj, playFlg_cMel)
    sp_ba =  mltPrcss.ChildProcess(device, 1, 5, pointer_Harm, currentBeat, ba, ba_articulation, timeSeriesObj, playFlg_ba)
    sp_vc =  mltPrcss.ChildProcess(device, 2, 5, pointer_Harm, currentBeat, vc, vc_articuration, timeSeriesObj, playFlg_vc)
    sp_dr = mltPrcss.ChildProcess(device, 9, 0, pointer_Perc, currentBeat, dr, dr_articuration, timeSeriesObj, playFlg_dr)

    #execute
    p_seq =  mltPrcss.Process(target = seq.execute, args=(timeSeriesObj, currentBeat) )
    p1 = mltPrcss.Process(target = sp_melody.execute)
    p2 = mltPrcss.Process(target = sp_ba.execute)
    p3 = mltPrcss.Process(target = sp_vc.execute)
    p4 = mltPrcss.Process(target = sp_cMelody.execute)
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
    """
    print("p5 START")
    p5.start()
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
    """
    p5.join()
    p6.join()
    """
    p8.terminate()
