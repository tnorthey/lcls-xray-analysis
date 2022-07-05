#runs=(43 44 45 46 47 48 56 57 61 62 63 64 68 70 71 72 73 74 79 80 81 82 83)
runs=(45 46 47 48 56 57 61 62 63 64 68 70 71 72 73 74 79 80 81 82 83)

echo "total runs:"
len=${#runs[@]}
echo $len

submit_script=submit_xtcav_stats.sh

for (( i=0; i<$len; i++ ))
do
 run=${runs[i]}
 echo "Run $run"
 dir=stats_run$run
 cd $dir
 xtcavDark cxilv0418 39 --max_shots 400
 xtcavLasingOff cxilv0418 40 --max_shots 400
 cd -
done

