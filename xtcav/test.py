import psana
from xtcav2.LasingOnCharacterization import LasingOnCharacterization
import numpy as np
print('imports done.')

run = 43
ds = psana.DataSource('exp=cxilv0418:run='+str(run)+':smd')
  
XTCAVRetrieval = LasingOnCharacterization()
Nevents = 800
agreement = np.zeros(Nevents)
c = 0
print('start of loop...')
for i, evt in enumerate(ds.events()):
    # Add: stop after N events
    if i > Nevents:
        break
    XTCAVRetrieval.processEvent(evt)
    # method 1: center-of-mass
    t, powerCOM = XTCAVRetrieval.xRayPower(method='COM')
    if (t is None) or (powerCOM is None):
        print('t1 or powerCOM is None')
        continue
    # method 2: RMS
    t, powerRMS = XTCAVRetrieval.xRayPower(method='RMS')
    if (t is None) or (powerRMS is None): 
        print('t2 or powerRMS is None')
        continue
    agreement[c] = XTCAVRetrieval.reconstructionAgreement()
    print(agreement[c])
    c += 1

print('Iterations done: %d' % c)
print('Equal 0:')
print(np.sum(agreement == 0))
print('Agreement > 0.9:')
print(np.sum(agreement > 0.9) / c)
print('Agreement > 0.8:')
print(np.sum(agreement > 0.8) / c)
print('Agreement > 0.7:')
print(np.sum(agreement > 0.7) / c)

