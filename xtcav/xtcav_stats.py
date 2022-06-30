"""
xtcav_stats; T. Northey, June 2022
read xtcav data and save
for "run" and "experiment"
"""
# python base modules
import sys
sys.path.append('../')
import time
START = time.time()  # initialise timer
import numpy as np
from scipy.signal import argrelextrema
# SLAC modules: psana, xtcav2
from psana import MPIDataSource
from xtcav2.LasingOnCharacterization import LasingOnCharacterization
# import my functions
from checks import checks
from define_experiment_run import experiment, run, scratch_dir, Nevents

print('Start of script.')
print('Run: %d' % run)

ds = MPIDataSource('exp=%s:run=%d:smd'% (experiment, run))  # data source
smldata = ds.small_data('%sxtcav_stats_run%d.h5' % (scratch_dir, run), gather_interval=100)

XTCAVRetrieval = LasingOnCharacterization()

def squeeze(t, p):
    """remove single dimensions from t, p arrays"""
    return np.squeeze(t), np.squeeze(p)

def peak_maxima(t, p):
    """uses scipy argrelextrema to return the index positions of the 2 largest peak maxima.
    t, p must have same length; also returns delta_t between the peaks"""
    imax = argrelextrema(p, np.greater)
    imax = np.squeeze(imax)
    try:
        len(imax)
    except TypeError:
        return False   # if there's no len, exit
    if len(imax) < 2:  # if there's 0 or 1 local maximum, exit
        return False
    ipeaks = np.zeros(2, dtype=int)
    for _i in range(2):
        p_local_maxima = p[imax]  # absolute values of local maxima
        tmp = np.argmax(p_local_maxima)  # tmp index value of global max
        ipeaks[_i] = imax[tmp]  # true index of global max
        imax = np.delete(imax, tmp) # delete global max
    ipeak1 = ipeaks[0]  # index of largest local maximum
    ipeak2 = ipeaks[1]  # index of second largest local max
    dt = abs(t[ipeak2] - t[ipeak1]) # delta t between two peaks
    return ipeak1, ipeak2, dt

print('start of loop...')
for i, evt in enumerate(ds.events()):
    print('iteration %i' % i)
    # Add: stop after N events
    if i > Nevents:
        break
    XTCAVRetrieval.processEvent(evt)
    # method 1: center-of-mass
    tCOM, powerCOM = XTCAVRetrieval.xRayPower(method='COM')
    if (tCOM is None) or (powerCOM is None):
        print('tCOM or powerCOM is None')
        continue
    tCOM, powerCOM = squeeze(tCOM, powerCOM)
    # method 2: RMS
    tRMS, powerRMS = XTCAVRetrieval.xRayPower(method='RMS')
    if (tRMS is None) or (powerRMS is None):
        print('tRMS or powerRMS is None')
        continue
    tRMS, powerRMS = squeeze(tRMS, powerRMS)
    # peak maxima and delta_t
    if not peak_maxima(tCOM, powerCOM):
        continue
    imax1_COM, imax2_COM, dt_COM = peak_maxima(tCOM, powerCOM)
    if not peak_maxima(tRMS, powerRMS):
        continue
    imax1_RMS, imax2_RMS, dt_RMS = peak_maxima(tRMS, powerRMS)
    # agreement between two methods
    agreement = XTCAVRetrieval.reconstructionAgreement()
    # save to file
    smldata.event(tCOM=tCOM, tRMS=tRMS, powerCOM=powerCOM, powerRMS=powerRMS,
                  dt_COM=dt_COM, dt_RMS=dt_RMS,
                  imax1_COM=imax1_COM, imax2_COM=imax2_COM,
                  imax1_RMS=imax1_RMS, imax2_RMS=imax2_RMS,
                  agreement=agreement)

# END for loop
# final write to file
print('Final save to file..')
smldata.save()

END = time.time()
print('Total time: ' + str(END - START))
