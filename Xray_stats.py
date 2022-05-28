from psana import *
import numpy as np
import time
# import my functions
from define_evrcodes import load_evrcodes
from define_detector_vars import load_detector_vars
from define_exp_scratch_runs import load_exp_scratch_runs
from define_diode_adu_thresholds import load_diode_adu_thresholds
from safe_get import safe_get
#from checks import checks

print('Start of script.')

start = time.time()  # initialise timer

# load diode and ADU detector thresholds
diode_avg,lower_threshold,upper_threshold,lb,ub = load_diode_adu_thresholds()
# load EVR codes
LASERON,LASEROFF,XRAYOFF,XRAYOFF1 = load_evrcodes()
# define experiment e.g. 'cxilv0418', scratch directory, and list of run numbers 
experiment,scratch_dir,runs = load_exp_scratch_runs()
run = runs[0]
# FILENAME:
ds = MPIDataSource('exp=%s:run=%d'% (experiment, run))
smldata = ds.small_data('/reg/d/psdm/cxi/%s/scratch/northeyt/Xray_stats_run%d.h5' %(experiment, run), gather_interval=100)  #This creates a 'small-data file' in your scratch folder, which is later loaded into the i_ub script

# load detector
# this loading part is ~slow (2-3 secs), maybe do not use inside loop
front,diode_upstream,diode_downstream,x_ray,electron,uvint,stageencoder,ttfltpos,chamber_pressure,det_z,evr = load_detector_vars(experiment,run)

# TN: initialise variables 
dark_shots = 0

def checks():
  ############################################################
  ### BEGIN CHECKS
  if evt is None: return False
  evrcodes = evr(evt)
  if evrcodes is None: return False

  # determine uvon, uvoff, dark
  dark = XRAYOFF in evrcodes
  if dark: return False

  evt_xray_pull = safe_get(x_ray, evt)
  if evt_xray_pull is None: return False
  # x-ray intensity in mJ 
  #evt_xray = evt_xray_pull.f_21_ENRC()
  #print('evt_xray: ' + str(evt_xray))

  # electron pull?
  evt_electron_pull = safe_get(electron, evt)
  if evt_electron_pull is None: return False
  #evt_electron = evt_electron_pull.ebeamCharge()
  #print('evt_electron: ' + str(evt_electron))

  # position in space of Jungfrau (distance from cell)
  evt_det_z = det_z(evt)
  if evt_det_z is None: return False
  #print('evt_det_z: ' + str(evt_det_z))
    
  # upstream/downstream correlation if there are non-linear effect (?)
  evt_xint_pulldown = safe_get(diode_downstream, evt)
  if evt_xint_pulldown is None: return False
  #evt_diode_downstream = evt_xint_pulldown.TotalIntensity()
  #print('evt_diode_downstream: ' + str(evt_diode_downstream))
  return True
  ### END CHECKS
  ############################################################

# TN: enumerate makes the events iteratable by assigning indices to them (I think?)
# In python you can have 2 iterators "n" and "evt"
Nevents = 1e5
print('Begin loop')
for n, evt in enumerate(ds.events()):
  print('n:' + str(n) + ' evt:' + str(evt)) 
    
  ds.break_after(Nevents)

  checks()

  evt_xray_pull = safe_get(x_ray, evt)
  if evt_xray_pull is None: continue
  # x-ray intensity in mJ 
  evt_xray = evt_xray_pull.f_21_ENRC()
  #print('evt_xray: ' + str(evt_xray))

  # upstream/downstream correlation if there are non-linear effect (?)
  evt_xint_pulldown = safe_get(diode_downstream, evt)
  if evt_xint_pulldown is None: continue
  evt_diode_downstream = evt_xint_pulldown.TotalIntensity()
  #print('evt_diode_downstream: ' + str(evt_diode_downstream))

  # upstream x-ray intensity
  evt_xint_pull = safe_get(diode_upstream, evt)
  if evt_xint_pull is None: continue
  xint = evt_xint_pull.TotalIntensity() #; print('xint: ' + str(xint))
  if (xint < lower_threshold) or (xint >= upper_threshold): continue

  # saving to file
  ### I need to understand this method of saving...
  smldata.event(upstream=xint, downstream=evt_diode_downstream, evt_xray=evt_xray)

# END for loop
# final write to file
# bins = smldata.sum(bins)  # Don't need to do it for bins array (idk why though)
print('Final save to file..')
#smldata.save(bins=bins)
smldata.save()

end = time.time()
print('Total time: ' + str(end - start))

