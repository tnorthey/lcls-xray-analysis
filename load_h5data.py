import h5py

# Load the "key" array from a h5 file
def load_h5data(fname,key):
 try:
  f = h5py.File(fname, 'r')
 except Exception as e:
  print('Error: %s' % e)
  return False
 print(f.keys())
 try:
  dset = f[key]
 except Exception as e:
  print('%s error: %s' % (key, e))
  return False
 print(dset.shape)
 return dset