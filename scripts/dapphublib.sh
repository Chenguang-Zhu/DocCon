#!/usr/bin/env bash
# # install nix environment that dapp tools depend.
# # this is a interactive process
# sh <(curl -L https://nixos.org/nix/install) --daemon

# # may need to create another terminal to make nix effective

# # install dapp tool sets

# curl https://dapp.tools/install | sh

pip3 uninstall -y slither-analyzer crytic-compile

pip3 install slither-analyzer==0.8.0 crytic-compile==0.2.0

# sudo mv /home/liuye/.nix-profile/bin/solc /home/liuye/.nix-profile/bin/solc.0.8.6
# solc-select use 0.4.24
workdir=$(pwd)
dapplib_src_dir=$(pwd)/library-src/DappHub

if [ ! -e $dapplib_src_dir ]
then 
    echo "created $dapplib_src_dir"
    mkdir -p $dapplib_src_dir
fi 


dapplibs=( ds-auth ds-cache ds-chief ds-exec ds-guard ds-pause ds-proxy ds-roles ds-stop ds-test ds-thing ds-token ds-value ds-weth ds-math )
#dapplibs=( ds-auth ds-cache ds-chief ds-exec ds-guard ds-pause ds-proxy ds-roles ds-stop ds-test ds-thing ds-token ds-value ds-weth )

github_dapphub_prefix=git@github.com:dapphub

for dapplib in ${dapplibs[@]}
do 

    # if [ -d $dapplib_src_dir/$dapplib ]
    # then 
    #     cd  $dapplib_src_dir/$dapplib 
    #     git pull 
    # else
    #     cd $dapplib_src_dir
    #     git clone $github_dapphub_prefix/${dapplib}.git
    # fi 
    # # for sublib in $(ls $dapplib_src_dir/$dapplib/lib)
    # # do 
    # #     cd  $dapplib_src_dir/$dapplib/lib/$sublib && git pull 
    # # done 
    # cd $dapplib_src_dir/$dapplib/ && dapp update && dapp build 
    cd $workdir/Code2Schema 
    python3 __main__0_8_0.py $dapplib_src_dir/$dapplib/ --factsdir $workdir/library-facts/dapphub/$dapplib/  --ignore-compile
done 


