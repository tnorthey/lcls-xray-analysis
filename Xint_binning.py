from psana import *
import numpy as np
import time
# my functions (should be in same directory)
from run_sum_stats import *
from load_get_functions import *

"""
T. Northey, May 2022
xint_binning:
Bins Jungfrau pixel arrays of size (8,512,1024) according to x-ray shot intensity percentiles
For the run defined in vars script
"""

print('Start of script.')

start = time.time()  # initialise timer

# load diode and ADU detector thresholds
diode_avg,lower_threshold,upper_threshold,lb,ub = load_diode_adu_thresholds()
# load EVR codes
LASERON,LASEROFF,XRAYOFF,XRAYOFF1 = load_evrcodes()
# define experiment e.g. 'cxilv0418', scratch directory, and list of run numbers 
experiment,run,scratch_dir = load_exp_run_scratch()

ds = MPIDataSource('exp=%s:run=%d'% (experiment, run))  # idk what this does exactly..
#This creates a 'small-data file' in your scratch folder, which is later loaded into the i_ub script
smldata = ds.small_data('%s/Xray_stats_run%d.h5' %(scratch_dir, run), gather_interval=100)

# load detector
# this loading part is ~slow (2-3 secs), maybe do not use inside loop
front,diode_upstream,diode_downstream,x_ray,electron,uvint,stageencoder,ttfltpos,chamber_pressure,det_z,evr = load_detector_vars(experiment,run)

print('Binning detector pixel arrays into %d percentiles' % npercentiles)
print('percentiles:')
print(percentiles)
# TN: initialise variables 
nbins = npercentiles - 1
bins = np.zeros(nbins) # counts number of shots in each bin
zero_array = np.zeros((nbins, 8, 512, 1024))
data = zero_array

def checks():
  ############################################################
  ### BEGIN CHECKS (I don't save any of this data to file)
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

def get_xint():
  evt_xint_pull = safe_get(diode_upstream, evt)
  if evt_xint_pull is None: return False
  xint = evt_xint_pull.TotalIntensity() #; print('xint: ' + str(xint))
  if (xint < lower_threshold) or (xint >= upper_threshold): return False
  return xint

def get_img():
  img = np.copy(front.calib_data(evt)) 
  if img is None: return False
  # remove pixels outside of [lb,ub] threshold
  try: 
    img *= (img > lb)
  except TypeError:
    print('Error', img, lb)
    return False
  try:
    img *= (img < ub)
  except TypeError:
    print('Error', img, ub)
    return False
  return img

# TN: enumerate makes the events iteratable by assigning indices to them (I think?)
# In python you can have 2 iterators "n" and "evt"
Nevents = 100000
for n, evt in enumerate(ds.events()):
  print('n:' + str(n) + ' evt:' + str(evt)) 
    
  ds.break_after(Nevents)

  if not checks(): print('checks FAlse'); continue

  xint = get_xint()
  if not xint: print('xint False'); continue

  img = get_img()
  if img.any() == False: print('img false'); continue
 
  #print('Normalising by upstream events..')
  img /= xint

  # normalise x-ray intensity
  xint /= xint_max

  # categorise into xint bins
  for i in range(0,nbins):
    if xint >= percentiles[i] and xint <= percentiles[i+1]:
      bins[i] += 1
      data[i,:,:,:] += img
  
  # saving to file
  ### I need to understand this method of saving...
  smldata.event()

# END for loop
# final write to file
data = smldata.sum(data)  # NB sums data from each MPI process!
bins = smldata.sum(bins)
print('Final save to file..')
smldata.save(data=data,bins=bins)

end = time.time()
print('Total time: ' + str(end - start))

