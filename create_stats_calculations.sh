runs=(43 44 45 46 47 48 56 57 61 62 63 64 68 70 71 72 73 74 79 80 81 82 83)
echo "total runs:"
len=${#runs[@]}
echo $len

for (( i=0; i<$len; i++ ))
do
 run=${runs[i]}
 echo "Run $run"
 mkdir "stats_run$run"
 cp tmp_stats/* stats_run$run
 cd stats_run$run
 sed -i "s/RUN_NUMBER/$run/g" upstream_stats_vars.py
 sbatch submit_upstream_stats.sh
 cd -
done

