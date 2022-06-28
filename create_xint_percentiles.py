import h5py
from analysis_functions import print_np_stats

"""
### From h5py:
An HDF5 file is a container for two kinds of objects: datasets, which are array-like collections of data, and groups, which are folder-like containers that hold datasets and other groups. The most fundamental thing to remember when using h5py is:

    Groups work like dictionaries, and datasets work like NumPy arrays

"""

# load h5 file
fname = 'upstream_stats_run43.h5'
f = h5py.File(fname, 'r')

# print database keys
print(f.keys())
# keys I care about: upstream, downstream, evt_xray

up = f['upstream']
down = f['downstream']
mJ = f['evt_xray']

print('Upstream intensity info:')
print_np_stats(up)
print('Downstream intensity info:')
print_np_stats(down)
print('mJ intensity info:')
print_np_stats(mJ)