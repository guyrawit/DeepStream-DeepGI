#!/bin/bash

docker run --gpus all -it --rm --net=host --privileged -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v /home/rawit/DeepGI-program:/app deepgi bash
