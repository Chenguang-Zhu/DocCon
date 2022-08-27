#!/usr/bin/env bash

pip3 uninstall -y slither-analyzer crytic-compile
pip3 install slither-analyzer==0.8.3 crytic-compile==0.2.3

workdir=$(pwd)
cd $workdir/library-src/erc721-extensions && git checkout v0.0.18
cp $workdir/legacy/erc721-extensions.hardhat.config.js $workdir/library-src/erc721-extensions/hardhat.config.js
cd $workdir/Code2Schema && python3 __main__0_8_3.py  ../library-src/erc721-extensions --factsdir ../library-facts/erc721-extensions/v0.0.18/

