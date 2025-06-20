#!/bin/bash

if [ $# -eq 1 ];
then
    container_name=$1
else
    container_name="pyannote-diarize-ctr"
fi

if [ $# -eq 2 ];
then
    docker_name=$1
else
    docker_name="pyannote-diarize"
fi
# osm="/mnt/neuropsych_mnt/opensmile_16k"
# dvrs="/mnt/neuropsych_mnt/downsampled_dvrs"
# js_fp="/mnt/scripts_mnt/ckarjadi-dev/dvoice_measures/"
docker run -v $(pwd):/scripts -it --rm --gpus all --name $container_name $docker_name bash