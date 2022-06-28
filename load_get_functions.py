"""Define thresholds, EVR codes, safe_get, Detector, load h5 data"""

import h5py
from define_experiment_run import experiment, run
from psana import MPIDataSource, Detector

def load_diode_adu_thresholds():
    """specify diode and pixel thresholds"""
    #These diode values are from the diode which measures the pulse by pulse X-ray pulse intensity.
    diode_avg = 25000
    lower_threshold = 10
    upper_threshold = 50000
    # Each pixel threshold; ADU or keV units
    lb = 2 # lower bound (ADU) for a hit
    ub = 80 # Upper bound (ADU) for a hit
    return diode_avg, lower_threshold, upper_threshold, lb, ub

def load_evrcodes():
    """Define EVR codes"""
    LASERON = 183
    LASEROFF = 184
    XRAYOFF = 162
    XRAYOFF1 = 163
    return LASERON, LASEROFF, XRAYOFF, XRAYOFF1

def safe_get(det, evt):
    """try to return the event"""
    try:
        return det.get(evt)
    except:
        print('safe_get: Error getting event, returning.')
        return None

def load_detector_vars(_experiment, _run):
    """loads detector variables"""
    ds = MPIDataSource('exp=%s:run=%d'% (_experiment, _run))
    front = Detector('jungfrau4M', ds.env())
    diode_upstream = Detector('CXI-DG2-BMMON', ds.env())
    diode_downstream = Detector('CXI-DG3-BMMON', ds.env())
    x_ray = Detector('FEEGasDetEnergy', ds.env())
    electron = Detector('EBeam', ds.env())
    uvint = Detector('Acqiris', ds.env())
    stageencoder = Detector('CXI:LAS:MMN:04.RBV', ds.env())
    ttfltpos = Detector('CXI:TIMETOOL:FLTPOS', ds.env())
    chamber_pressure = Detector('CXI:MKS670:READINGGET', ds.env())
    det_z = Detector('Jungfrau_z', ds.env())
    #This section is for choosing the correct evr detector, which occasionally switches
    # TN: Can rewrite shorter I think. Also why does this happen, what exactly is going on?
    evr = Detector('evr1')
    evt0 = ds.events().next()
    evrcodes = evr(evt0)
    if evrcodes is None:
        evr = Detector('evr2')
        evrcodes_otherdetector = evr(evt0)
        if evrcodes_otherdetector is None:
            print('evr error')
    return front, diode_upstream, diode_downstream, x_ray, electron,\
        uvint, stageencoder, ttfltpos, chamber_pressure, det_z, evr

def load_h5data(fname, key):
    """Load the "key" array from a h5 file"""
    try:
        f = h5py.File(fname, 'r')
    except IOError:
        print('load_h5data: Error loading h5file, returning.')
        return False
    print(f.keys())
    try:
        dset = f[key]
    except:
        print('load_h5data: Error reading dataset key, returning.')
        return False
    print(dset.shape)
    return dset
