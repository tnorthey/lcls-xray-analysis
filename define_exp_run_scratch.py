def load_exp_run_scratch():
 experiment = 'cxilv0418'
 scratch_dir = '/reg/d/psdm/cxi/%s/scratch/northeyt/' % experiment
 runs=[43, 44, 45, 46, 47, 48, 56, 57, 61, 62, 63, 64, 68, 70, 71, 72, 73, 74, 79, 80, 81, 82, 83] # currently runs does nothing. Delete? Or move to another file?
 run = 43
 return experiment,run,scratch_dir
