#!/usr/bin/env bash
pip3 uninstall -y slither-analyzer crytic-compile
pip3 install slither-analyzer==0.8.3 crytic-compile==0.2.3


workdir=$(pwd)
cd $workdir/library-src/openzeppelin && git checkout v4.5.0
cd $workdir/Code2Schema && python3 __main__0_8_3.py  ../library-src/openzeppelin --factsdir ../library-facts/openzeppelin/v4.5.0/

cd $workdir/library-src/openzeppelin && git checkout v4.6.0-rc.0
cd $workdir/Code2Schema && python3 __main__0_8_3.py  ../library-src/openzeppelin --factsdir ../library-facts/openzeppelin/v4.6.0-rc.0/
