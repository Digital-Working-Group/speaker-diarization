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

docker run -v $(pwd):/scripts -it --rm --gpus all --name $container_name $docker_name bash