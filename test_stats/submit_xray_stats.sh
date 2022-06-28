#!/bin/bash

#SBATCH --partition=psanaq

# Request hours of runtime: (always enter time in minutes).  Max time for SLAC is 48 hours
#SBATCH --time=2880:00

# Setting nodes and tasks per node: (Modify this if you're planning to use multiple nodes in parallel to run a job)
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1

# Here's where the job name is defined (what shows up in the queue)
#SBATCH -J stats

#Here's where the memory is defined (setting to 0 should be maximum)
#SBATCH --mem=0 

#This creates an output file
#SBATCH -o xray_stats.log

# This runs the job
source /reg/g/psdm/etc/psconda.sh
mpirun python -u -m mpi4py.run xray_stats.py
#python xint_binning.py
