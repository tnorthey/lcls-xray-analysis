"""
xtcav_stats; T. Northey, June 2022
"""
# python base modules
import time
# psana, xtcav2
from psana import MPIDataSource
from xtcav2.LasingOnCharacterization import LasingOnCharacterization
# import my functions
import sys
sys.path.append('../')
from checks import checks
from load_get_functions import load_diode_adu_thresholds, load_evrcodes,\
        load_detector_vars, safe_get
from define_experiment_run import experiment, run, scratch_dir, Nevents

print('Start of script.')

START = time.time()  # initialise timer

_, lower_threshold, upper_threshold, _, _ = load_diode_adu_thresholds()
LASERON, LASEROFF, XRAYOFF, XRAYOFF1 = load_evrcodes()

ds = MPIDataSource('exp=%s:run=%d'% (experiment, run))  # data source
smldata = ds.small_data('%sxtcav_stats_run%d.h5' %(scratch_dir, run), gather_interval=100)
front, diode_upstream, diode_downstream, x_ray, electron, uvint, stageencoder, ttfltpos,\
chamber_pressure, det_z, evr = load_detector_vars(experiment, run)

XTCAVRetrieval = LasingOnCharacterization()

print('Begin loop')
c = 0
for n, evt in enumerate(ds.events()):
    print('n:' + str(n) + ' evt:' + str(evt))
    ds.break_after(Nevents)

    if not checks(evt, evr, x_ray, electron, diode_downstream, XRAYOFF, det_z):
        continue

    XTCAVRetrieval.processEvent(evt)
    # method 1: center-of-mass
    t1, powerCOM = XTCAVRetrieval.xRayPower(method='COM')
    if (t1 is None) or (powerCOM is None):
        continue
    # method 2: RMS
    t2, powerRMS = XTCAVRetrieval.xRayPower(method='RMS')
    if (t2 is None) or (powerRMS is None):
        continue
    # agreement between two methods
    agreement = XTCAVRetrieval.reconstructionAgreement()
    # saving to file
    smldata.event(t1=t1, t2=t2, powerCOM=powerCOM,\
            powerRMS=powerRMS, agreement=agreement)

# END for loop
# final write to file
print('Final save to file..')
smldata.save()

END = time.time()
print('Total time: ' + str(END - START))

