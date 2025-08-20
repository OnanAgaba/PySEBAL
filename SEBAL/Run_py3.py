# -*- coding: utf-8 -*-
"""
Created on 03 Dec 2019
Author: tih, sajid pareeth

Modified on: 20 Aug 2025
Author: Onan Agaba
"""
import pysebal_py3
import traceback
##### USER INPUTS

##### SET THE PATH TO INPUT CSV FILE #####
inputCSV = r"sample_input_timeseries.csv"
st = 2 # starting row number
en = 2 # ending row number

####### USER INPUTS FINISH HERE

for number in range(st, en + 1):
    try:
        print ('starting line num: %d' % number)
        pysebal_py3.SEBALcode(number,inputCSV)
        print ('line num: %d done' % number)   
    except:  # amir
        print ('--------------------\n')
        print ('SEBAL did not run line %d fully' % number)
        print ('\n******* ERROR *******\n')
        traceback.print_exc()
        
        print ('\n--------------------\n')
