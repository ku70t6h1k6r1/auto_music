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

    # parse section
    melody = leadSheet.leadLine #[0:rehA_length]
    chords = leadSheet.chordProgress #[0:rehA_length]
    counterMelody = leadSheet.counterMelody #[0:rehA_length]
    #chordObj = hm.Dataset()

    ba = leadSheet.ba #[0:rehA_length]
    v1 = leadSheet.v1 #[0:rehA_length]
    v2 = leadSheet.v2 #[0:rehA_length]

    bDr = leadSheet.baDrum #[0:rehA_length]
    print(bDr )
    sDr = leadSheet.snare #[0:rehA_length]
    print(sDr )
    cHH = leadSheet.hiHat #[0:rehA_length]
    print(cHH )

    articuration = leadSheet.articuration #[0:rehA_length]

    # multiprocessing setting
    timeSeriesObj = mltPrcss.TimeSeries()
    timeSeriesObj.setBpm(140)
    print("SET START TIME")
    timeSeriesObj.setStartTime(time.time())
    #device = 3 #microX
    device = 0
    sp_melody =  mltPrcss.ChildProcessHomo(device, 0, 1, np.stack([melody], axis = -1), np.stack([articuration *100], axis = -1), timeSeriesObj)
    sp_ba =  mltPrcss.ChildProcess(device, 1, 5, ba, articuration*80, timeSeriesObj)
    sp_v1 =  mltPrcss.ChildProcess(device, 2, 5, v1, articuration*80, timeSeriesObj)
    sp_v2 =  mltPrcss.ChildProcess(device, 2, 5, v2, articuration*80, timeSeriesObj)
    sp_bDr =  mltPrcss.ChildProcess(device, 9, 0, bDr, articuration*40, timeSeriesObj)
    sp_sDr =  mltPrcss.ChildProcess(device, 9, 0, sDr, articuration*30, timeSeriesObj)
    sp_cHH =  mltPrcss.ChildProcess(device, 9, 0, cHH, articuration*90, timeSeriesObj)

    dr_articuration = np.stack([articuration*90, articuration*80 ,articuration*80], axis = -1)
    dr = np.stack([cHH, sDr ,bDr], axis = -1)
    sp_dr = mltPrcss.ChildProcessHomo(device, 9, 0, dr, dr_articuration, timeSeriesObj)

    #execute
    p1 = mltPrcss.Process(target = sp_melody.execute)
    p2 = mltPrcss.Process(target = sp_ba.execute)
    p3 = mltPrcss.Process(target = sp_v1.execute)
    p4 = mltPrcss.Process(target = sp_v2.execute)
    p5 = mltPrcss.Process(target = sp_bDr.execute)
    p6 = mltPrcss.Process(target = sp_sDr.execute)
    p7 = mltPrcss.Process(target = sp_cHH.execute)

    p8 = mltPrcss.Process(target = sp_dr.execute)


    #MAX 4process
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

    p1.join()
    p2.join()
    p3.join()
    """
    p4.join()
    p5.join()
    p6.join()
    """
    p8.join()
