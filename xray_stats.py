"""
Xray_stats; T. Northey, May 2022
Save upstream and downstream diode readings, and mJ detector readings
to the defined scratch directory 'scratch_dir', for all shots in run number
'run', in experiment 'experiment'.
Variables defined in function load_exp_run_scratch in file define_exp_run_scratch.py
"""

import time
# psana
from psana import MPIDataSource
# import my functions
from checks import checks
from load_get_functions import load_diode_adu_thresholds,\
        load_evrcodes,\
        load_exp_run_scratch, load_detector_vars,\
        safe_get

print('Start of script.')

START = time.time()  # initialise timer

# load diode and ADU detector thresholds
_, lower_threshold, upper_threshold, _, _ = load_diode_adu_thresholds()
# load EVR codes
LASERON, LASEROFF, XRAYOFF, XRAYOFF1 = load_evrcodes()
# define experiment e.g. 'cxilv0418', scratch directory, and list of run numbers
experiment, run, scratch_dir = load_exp_run_scratch()

ds = MPIDataSource('exp=%s:run=%d'% (experiment, run))  # idk what this does exactly..
#This creates a 'small-data file' in your scratch folder, which is later loaded into the i_ub script
smldata = ds.small_data('%s/xray_stats_run%d.h5' %(scratch_dir, run), gather_interval=100)

# load detector
# this loading part is ~slow (2-3 secs), maybe do not use inside loop
front, diode_upstream, diode_downstream, x_ray, electron, uvint, stageencoder, ttfltpos,\
chamber_pressure, det_z, evr = load_detector_vars(experiment, run)

Nevents = 100000
print('Begin loop')
for n, evt in enumerate(ds.events()):
    print('n:' + str(n) + ' evt:' + str(evt))
    ds.break_after(Nevents)

    if not checks(evt):
        continue

    evt_xray_pull = safe_get(x_ray, evt)
    if evt_xray_pull is None:
        continue

    # x-ray intensity in mJ
    evt_xray = evt_xray_pull.f_21_ENRC()
    #print('evt_xray: ' + str(evt_xray))
    # downstream diode reading
    evt_xint_pulldown = safe_get(diode_downstream, evt)
    if evt_xint_pulldown is None:
        continue

    evt_diode_downstream = evt_xint_pulldown.TotalIntensity()
    #print('evt_diode_downstream: ' + str(evt_diode_downstream))
    # upstream diode reading
    evt_xint_pull = safe_get(diode_upstream, evt)
    if evt_xint_pull is None:
        continue

    xint = evt_xint_pull.TotalIntensity()
    if (xint < lower_threshold) or (xint >= upper_threshold):
        continue

    # saving to file
    smldata.event(upstream=xint, downstream=evt_diode_downstream, evt_xray=evt_xray)

# END for loop
# final write to file
print('Final save to file..')
smldata.save()

END = time.time()
print('Total time: ' + str(END - START))
