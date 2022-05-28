# print basic stats for numpy array
def print_npstats(dset):
  print('length:  %d' % len(dset))
  print('mean:    %f' % np.mean(dset))
  print('median:  %f' % np.median(dset))
  print('minimum: %f' % np.min(dset))
  print('maximum: %f' % np.max(dset))
  print('st. dev: %f' % np.std(dset))