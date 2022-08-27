#!/usr/bin/env bash

g++ userfunctors.cpp -c -fPIC -o functors.o 
g++ -shared -o libfunctors.so functors.o 
# export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}`pwd`
