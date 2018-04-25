# -*- coding: utf-8 -*-
import numpy as np
import createLeadSheet as ls
import common_function as func
#import chord_voices as cv
#import harmonize_tf as hm
import createSequencer as seq
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
    articuration = leadSheet.articuration[0:rehA_length]

    # parse section
    melody = leadSheet.leadLine[0:rehA_length]
    chords = leadSheet.chordProgress[0:rehA_length]
    counterMelody = leadSheet.counterMelody[0:rehA_length]
    #chordObj = hm.Dataset()

    ba = leadSheet.ba[0:rehA_length]
    v1 = leadSheet.v1[0:rehA_length]
    v2 = leadSheet.v2 [0:rehA_length]

    bDr = leadSheet.baDrum[0:rehA_length]
    sDr = leadSheet.snare[0:rehA_length]
    cHH = leadSheet.hiHat[0:rehA_length]

    #Make Each Channel
    melody = np.stack([melody], axis = -1)
    mel_articulation = np.stack([articuration *100], axis = -1)

    ba = np.stack([ba], axis = -1)
    ba_articulation  = np.stack([articuration *80], axis = -1)

    vc = np.stack([v1, v2 ], axis = -1)
    vc_articuration = np.stack([articuration*80 ,articuration*80], axis = -1)

    dr = np.stack([cHH, sDr ,bDr], axis = -1)
    dr_articuration = np.stack([articuration*90, articuration*80 ,articuration*80], axis = -1)

    #For Shared Memory
    pointer_Perc = mltPrcss.Value('i', 0)
    pointer_Harm = mltPrcss.Value('i', 0)
    currentBeat = mltPrcss.Value('i', 0)
    playFlg_Perc = mltPrcss.Value('i', 1)
    playFlg_Harm = mltPrcss.Value('i', 1)
    rythm_seq = np.array([0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1 \
                                ,16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1 \
                                ,16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1,  16,-1,-1,-1 \
                                ])

    harmony_seq = np.array([0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ,0,-1,-1,-1,  0,-1,-1,-1,  0,-1,-1,-1,  16,-1,-1,-1 \
                                ])
    seq = mltPrcss.StepSequencer( [pointer_Perc, pointer_Harm], np.stack([rythm_seq, harmony_seq], axis = -1), [playFlg_Perc, playFlg_Harm])


    # multiprocessing setting
    timeSeriesObj = mltPrcss.TimeSeries()
    timeSeriesObj.setBpm(140)
    print("SET START TIME")
    timeSeriesObj.setStartTime(time.time())
    device = 0    #device = 3 #microX
    sp_melody =  mltPrcss.ChildProcess(device, 0, 1, pointer_Harm, currentBeat, melody, mel_articulation, timeSeriesObj, playFlg_Harm)
    sp_ba =  mltPrcss.ChildProcess(device, 1, 5, pointer_Harm, currentBeat, ba, ba_articulation, timeSeriesObj, playFlg_Harm)
    sp_vc =  mltPrcss.ChildProcess(device, 2, 5, pointer_Harm, currentBeat, vc, vc_articuration, timeSeriesObj, playFlg_Harm)
    sp_dr = mltPrcss.ChildProcess(device, 9, 0, pointer_Perc, currentBeat, dr, dr_articuration, timeSeriesObj, playFlg_Perc)

    #execute
    p_seq =  mltPrcss.Process(target = seq.execute, args=(timeSeriesObj, currentBeat) )
    p1 = mltPrcss.Process(target = sp_melody.execute)
    p2 = mltPrcss.Process(target = sp_ba.execute)
    p3 = mltPrcss.Process(target = sp_vc.execute)
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
    """
    p4.start()
    print("p5 START")
    p5.start()
    print("p6 START")
    p6.start()
    """
    print("p8 START")
    p8.start()

    p_seq.join()
    p1.join()
    p2.join()
    p3.join()
    """
    p4.join()
    p5.join()
    p6.join()
    """
    p8.join()
