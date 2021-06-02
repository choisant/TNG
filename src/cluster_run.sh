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

if [ $file_number -gt 0 ]
then
    list_path="./data/$tng_run/cutdata/id_file_1/central_id_$file_number.txt"
    #list_path="./data/$tng_run/cutdata/missed/missed_$file_number.txt"
else
    list_path="./data/$tng_run/cutdata/central_id_1.txt"
fi
echo "$list_path"

readarray index_list < $list_path

for index in ${index_list[@]}; do
    python ./src/cluster_run.py -tng $tng_run -id $job_id -n $test_name -sub $index
    done
