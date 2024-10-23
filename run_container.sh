#!/bin/bash

docker run --gpus all -it --rm --net=host --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -w /opt/nvidia/deepstream/deepstream-7.1 nvcr.io/nvidia/deepstream:7.1-gc-triton-devel
