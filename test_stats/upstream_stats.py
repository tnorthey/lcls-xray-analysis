from psana import *
import numpy as np
import time
from upstream_stats_vars import *

print('Start of script.')

start = time.time()  # initialise timer

# TN: initialise variables 
dark_shots = 0

# TN: what is this?
def safe_get(det, evt):
  try:
    return det.get(evt)
  except Exception:
    return None

# TN: enumerate makes the events iteratable by assigning indices to them (I think?)
# In python you can have 2 iterators "n" and "evt"
print('Begin loop')
for n, evt in enumerate(ds.events()):
  print('n:' + str(n) + ' evt:' + str(evt)) 
    
  ds.break_after(Nevents)

  ############################################################
  ### BEGIN CHECKS (I don't save any of this data to file)
  if evt is None: continue
  evrcodes = evr(evt)
  if evrcodes is None:continue

  # determine uvon, uvoff, dark
  dark = XRAYOFF in evrcodes
  if dark:
    print('DARK')
    dark_shots += 1
    continue

  # electron pull?
  evt_electron_pull = safe_get(electron, evt)
  if evt_electron_pull is None: continue
  #evt_electron = evt_electron_pull.ebeamCharge()
  #print('evt_electron: ' + str(evt_electron))

  # position in space of Jungfrau (distance from cell)
  evt_det_z = det_z(evt)
  if evt_det_z is None: continue
  #print('evt_det_z: ' + str(evt_det_z))
  ### END CHECKS
  ############################################################

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

