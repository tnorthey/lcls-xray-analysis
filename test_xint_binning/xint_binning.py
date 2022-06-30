"""
xint_binning:
Bins Jungfrau pixel arrays of size (8, 512, 1024) according to x-ray shot intensity percentiles.
T. Northey,  May 2022
"""

import time
import numpy as np
import sys
sys.path.append('../')
from psana import MPIDataSource
# my functions
from run_sum_stats import xint_max, percentiles
from checks import checks
from load_get_functions import load_diode_adu_thresholds, load_evrcodes,\
        load_detector_vars, safe_get
from define_experiment_run import experiment, run, scratch_dir, Nevents

print('Start of script.')

start = time.time()  # initialise timer

# load diode and ADU detector thresholds
diode_avg, lower_threshold, upper_threshold, lb, ub = load_diode_adu_thresholds()
# load EVR codes
LASERON, LASEROFF, XRAYOFF, XRAYOFF1 = load_evrcodes()

ds = MPIDataSource('exp=%s:run=%d'% (experiment, run))
smldata = ds.small_data('%sxint_binning_run%d.h5' %(scratch_dir, run), gather_interval=100)

# load detector
# this loading part is ~slow (2-3 secs),  maybe do not use inside loop
front, diode_upstream, diode_downstream, x_ray, electron, uvint, stageencoder,\
        ttfltpos, chamber_pressure, det_z, evr = load_detector_vars(ds)

npercentiles = len(percentiles)
print('Binning detector pixel arrays into %d percentiles' % npercentiles)
print('percentiles:')
print(percentiles)
nbins = npercentiles - 1
bins = np.zeros(nbins) # counts number of shots in each bin
zero_array = np.zeros((nbins, 8, 512, 1024))
data = zero_array

def get_xint(_evt):
    """get x-ray intensity from the upstream detector"""
    evt_xint_pull = safe_get(diode_upstream, _evt)
    _xint = evt_xint_pull.TotalIntensity()
    if (_xint < lower_threshold) or (_xint >= upper_threshold):
        return False
    return _xint

def get_img(_evt):
    """get Jungfrau pixel array"""
    _img = np.copy(front.calib_data(_evt))
    if _img is None:
        return False
    # remove pixels outside of [lb, ub] threshold
    try:
        _img *= (_img > lb)
    except TypeError:
        print('Error', _img, lb)
        return False
    try:
        _img *= (_img < ub)
    except TypeError:
        print('Error', _img, ub)
        return False
    return _img

for n, evt in enumerate(ds.events()):
    print('n:' + str(n) + ' evt:' + str(evt))

    ds.break_after(Nevents)

    if not checks(evt, evr, XRAYOFF, x_ray, electron, diode_downstream, det_z):
        print('checks False')
        continue
    xint = get_xint(evt)
    if not xint:
        print('xint False')
        continue
    img = get_img(evt)
    if not img.any():
        print('img false')
        continue
    #print('Normalising by upstream events..')
    img /= xint
    # normalise x-ray intensity
    xint /= xint_max
    # categorise into xint bins
    for i in range(0, nbins):
        if percentiles[i] <= xint <= percentiles[i+1]:
            bins[i] += 1
            data[i, :, :, :] += img
    # saving to file
    smldata.event()

# END for loop
# final write to file
data = smldata.sum(data)  # NB sums data from each MPI process!
bins = smldata.sum(bins)
print('Final save to file..')
smldata.save(data=data, bins=bins)

end = time.time()
print('Total time: ' + str(end - start))
