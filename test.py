from define_evrcodes import load_evrcodes
from define_detector_vars import load_detector_vars
from define_exp_run_scratch import load_exp_run_scratch
from define_diode_adu_thresholds import load_diode_adu_thresholds
import time

start = time.time()

# load diode and ADU detector thresholds
diode_avg,lower_threshold,upper_threshold,lb,ub = load_diode_adu_thresholds()

# load EVR codes
LASERON,LASEROFF,XRAYOFF,XRAYOFF1 = load_evrcodes()

# define experiment e.g. 'cxilv0418', scratch directory, and list of run numbers 
experiment,run,scratch_dir = load_exp_run_scratch()

# load detector
# this loading part is ~slow (2-3 secs), maybe do not use inside loop
front,diode_upstream,diode_downstream,x_ray,electron,uvint,stageencoder,ttfltpos,chamber_pressure,det_z,evr = load_detector_vars(experiment,run)

end = time.time()
print('Total time: ' + str(end - start))
