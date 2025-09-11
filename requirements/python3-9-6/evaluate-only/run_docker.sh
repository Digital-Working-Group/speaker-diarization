#!/bin/bash

if [ $# -eq 1 ];
then
    container_name=$1
else
    container_name="py3-9-6-pyannote-diarize-eval-only-ctr"
fi

if [ $# -eq 2 ];
then
    docker_name=$1
else
    docker_name="py3-9-6-pyannote-diarize-eval-only"
fi
dir_up=$(realpath "../../../")
docker run -v $dir_up:/scripts -it --rm --name $container_name $docker_name bash