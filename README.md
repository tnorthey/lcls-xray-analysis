# lcls-xray-analysis

Reads data from LCLS X-ray, e.g. X-ray intensity diode readings (upstream/downstream), X-ray intensity (mJ detector), xtcav (temporal pulse structure), chamber pressure, Jungfrau detector pixel readings, plus more...

Requires psana python library (developed by SLAC personnel; [link] [name])
Aside from some post-analysis, you must be on the SLAC computers to run these scripts. I'm using git to version control / share with collaborators.

working on: xtcav (temporal pulse structure)

### To do
- define_exp_run_scratch.template & bash script to create many directories
- runs is defined in bash script (after all)
- write create_stats_h5 script
- write load_stats_h5
- use the load_stats_h5 in Xint_binning


### Files

```
define_detector_vars.py
define_diode_adu_thresholds.py
define_evrcodes.py
define_exp_scratch_runs.py
get_xint.py
load_h5data.py
print_npstats.py
radialavg.py
README.md
safe_get.py
test.py
Xray_stats.py
```

### Logic / code structure

#### 'define' scripts

Contain functions that define variables used often. May need to change diode_adu_thresholds, experiment name, scratch directory location, and list of runs (define_exp_scratch_runs)

#### Other non-capitalised functions

`get_xint.py`; gets the X-ray intensity readings
`load_h5data.py`; loads data with the key 'key' from a h5 file
`print_npstats.py`; print statistics about a numpy array (mean, median, percentiles, range, st. dev.)
`radialavg.py`; radial average of data into nbins radial q-bins.
  nbins must be an integer.
  data and q must be numpy arrays of the same size.
`safe_get.py`;
`test.py`;




