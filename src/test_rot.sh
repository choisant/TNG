#!/bin/bash
while getopts t:i:n:g: flag
do
    case "${flag}" in
        t) tng_run=${OPTARG};;
        i) job_id=${OPTARG};;
        n) test_name=${OPTARG};;
        g) file_number=${OPTARG};;
    esac
done

late_list=(518774 518810 518854 518896 519091 583208)

for index in ${late_list[@]}; do
    python ./src/check_rotation.py -tng $tng_run -id $job_id -n $test_name -sub  $index
    done
