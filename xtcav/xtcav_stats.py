"""
xtcav_stats; T. Northey, June 2022
read xtcav data and save
for "run" and "experiment" 
"""
# python base modules
import time
START = time.time()  # initialise timer
# psana, xtcav2
from psana import MPIDataSource
#import psana
#from psana import *
from xtcav2.LasingOnCharacterization import LasingOnCharacterization
# import my functions
import sys
sys.path.append('../')
from checks import checks
from load_get_functions import load_diode_adu_thresholds, load_evrcodes,\
        load_detector_vars, safe_get
from define_experiment_run import experiment, run, scratch_dir, Nevents

print('Start of script.')
print('Run: %d' % run)

#run = 43
#ds = psana.DataSource('exp=cxilv0418:run='+str(run)+':smd')
ds = MPIDataSource('exp=%s:run=%d:smd'% (experiment, run))  # data source
smldata = ds.small_data('%sxtcav_stats_run%d.h5' % (scratch_dir, run), gather_interval=100)

XTCAVRetrieval = LasingOnCharacterization()
Nevents = 700
print('start of loop...')
for i, evt in enumerate(ds.events()):
    # Add: stop after N events
    if i > Nevents:
        break
    XTCAVRetrieval.processEvent(evt)
    # method 1: center-of-mass
    t1, powerCOM = XTCAVRetrieval.xRayPower(method='COM')
    if (t1 is None) or (powerCOM is None):
        print('t1 or powerCOM is None')
        continue
    # method 2: RMS
    t2, powerRMS = XTCAVRetrieval.xRayPower(method='RMS')
    if (t2 is None) or (powerRMS is None): 
        print('t2 or powerRMS is None')
        continue
    # agreement between two methods
    agreement = XTCAVRetrieval.reconstructionAgreement()
    print(agreement)
    smldata.event(t1=t1, t2=t2, powerCOM=powerCOM, powerRMS=powerRMS, agreement=agreement)

# END for loop
# final write to file
print('Final save to file..')
smldata.save()

END = time.time()
print('Total time: ' + str(END - START))
