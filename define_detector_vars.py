from psana import *

def load_detector_vars(experiment,run):
 #run = 43  # for initial detector setup; changes later when looping over runs
 ds = MPIDataSource('exp=%s:run=%d'% (experiment, run)) 
 
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
  else:
   print('evr detector found')
 
 return front,diode_upstream,diode_downstream,x_ray,electron,uvint,stageencoder,ttfltpos,chamber_pressure,det_z,evr