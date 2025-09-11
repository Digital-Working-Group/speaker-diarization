#!/bin/bash
if [ $# -eq 1 ];
then
    docker_name=$1
else
    docker_name="py3-9-6-pyannote-diarize"
fi
docker build -t $docker_name .
