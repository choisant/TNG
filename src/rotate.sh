#!/bin/bash
while getopts t:i:n: flag
do
    case "${flag}" in
        t) tng_run=${OPTARG};;
        i) job_id=${OPTARG};;
        n) test_name=${OPTARG};;
    esac
done


list_path="./data/$tng_run/cutdata/rotate.txt"

readarray index_list < $list_path

for index in ${index_list[@]}; do
    python ./src/check_rotation.py -tng $tng_run -n $test_name -sub $index
    done
