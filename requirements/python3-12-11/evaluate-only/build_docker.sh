#!/bin/bash
if [ $# -eq 1 ];
then
    docker_name=$1
else
    docker_name="py3-12-11-pyannote-diarize-eval-only"
fi
docker build -t $docker_name .
