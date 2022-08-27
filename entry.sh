#!/usr/bin/env bash
set -ux

#BASE_PATH="$HOME/Projects/smart_apidoc_inconsis"
BASE_PATH="/opt/doccon"
SCRIPT_PATH=$BASE_PATH/scripts

$SCRIPT_PATH/extract-facts.sh

### prepare facts for Datalog engine
DOC_FACTS_ROOT="$BASE_PATH/exp/doc_facts"
CODE_FACTS_ROOT="$BASE_PATH/library-facts"
DL_IN_PATH="$BASE_PATH/exp/dl/in"
DL_OUT_PATH="$BASE_PATH/exp/dl/out"

echo "Link extracted facts to datalog input directory"
name_vers=( "openzeppelin/v4.5.0" "erc721-extensions/v0.0.18" )
for nv in "${name_vers[@]}"; do
	mkdir -p "$DL_IN_PATH/$nv"
	mkdir -p "$DL_OUT_PATH/$nv"
	ln -sf "$DOC_FACTS_ROOT/$nv/docfacts"\
	   "$DL_IN_PATH/$nv/"
	ln -sf "$CODE_FACTS_ROOT/$nv/codefacts"\
	   "$DL_IN_PATH/$nv/"

	ln -sf "$DOC_FACTS_ROOT/$nv/docfacts"\
	   "$DL_IN_PATH/$nv/"
	ln -sf "$CODE_FACTS_ROOT/$nv/codefacts"\
	   "$DL_IN_PATH/$nv/"
done

## manually confirmed functions of erc721-ext. those from openzeppelins are excluded
## override HasFn/2
cp "$BASE_PATH/exp/resources/ERC721Exts.DefinedFunctions.facts" \
   "$CODE_FACTS_ROOT/erc721-extensions/v0.0.18/codefacts/HasFn.facts"

## Override IsContract/1 for dapphub projects
for x in "$BASE_PATH"/exp/resources/dapphub/*; do
    cp "$x"/IsContract.facts "$CODE_FACTS_ROOT/dapphub/${x##*/}/codefacts/IsContract.facts"
done
## Add ExcludeInterface/1 and ExcludeContract/1
## we do not need this anymore, because we override HasFn/2
## with a manually confirmed list of functions
ln -sf "$CODE_FACTS_ROOT/openzeppelin/v4.5.0/codefacts/IsInterface.facts"\
   "$CODE_FACTS_ROOT/erc721-extensions/v0.0.18/codefacts/ExcludeInterface.facts"
ln -sf "$CODE_FACTS_ROOT/openzeppelin/v4.5.0/codefacts/IsContract.facts"\
   "$CODE_FACTS_ROOT/erc721-extensions/v0.0.18/codefacts/ExcludeContract.facts"
touch "$CODE_FACTS_ROOT/openzeppelin/v4.5.0/codefacts/ExcludeContract.facts"
touch "$CODE_FACTS_ROOT/openzeppelin/v4.5.0/codefacts/ExcludeInterface.facts"


# dapplibs=( "ds-auth" "ds-cache" "ds-chief" "ds-exec" "ds-guard" "ds-pause" "ds-proxy" "ds-roles" "ds-stop" "ds-test" "ds-thing" "ds-token" "ds-value" "ds-weth" )
dapplibs=( "ds-stop" "ds-cache" "ds-chief" "ds-token" "ds-guard" "ds-roles" "ds-auth" "ds-math" )
for dapplib in "${dapplibs[@]}"; do
	mkdir -p "$DL_IN_PATH/dapphub/$dapplib"
	mkdir -p "$DL_OUT_PATH/dapphub/$dapplib"

	touch "$CODE_FACTS_ROOT/dapphub/$dapplib/codefacts/ExcludeContract.facts"
	touch "$CODE_FACTS_ROOT/dapphub/$dapplib/codefacts/ExcludeInterface.facts"

	ln -sf "$DOC_FACTS_ROOT/dapphub/$dapplib/docfacts"\
	   "$DL_IN_PATH/dapphub/$dapplib/"
	ln -sf "$CODE_FACTS_ROOT/dapphub/$dapplib/codefacts"\
	   "$BASE_PATH/exp/dl/in/dapphub/$dapplib/"
done

### Inconsistency Discovery
#RULE_PATH="$HOME/Projects/DocCon-Facts/datalog"
RULE_PATH="$BASE_PATH/datalog/"
SOUFFLE="souffle"
cd "$RULE_PATH/userdef-functors" && ./compile-functor.sh \
	&& export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}`pwd`
for nv in "${name_vers[@]}"; do
	$SOUFFLE -F "$DL_IN_PATH/$nv" -D "$DL_OUT_PATH/$nv" \
			"$RULE_PATH/err-detect/l1err.dl"
	echo "Concat $nv L1 results"
	cd "$DL_OUT_PATH/$nv" && cat L1*.csv > all-L1.csv

	$SOUFFLE -F "$DL_IN_PATH/$nv" -D "$DL_OUT_PATH/$nv" \
			"$RULE_PATH/err-detect/l2err.dl"
	echo "Concat $nv L2 results"
	cd "$DL_OUT_PATH/$nv" && cat L2*.csv > all-L2.csv

	$SOUFFLE -F "$DL_IN_PATH/$nv" -D "$DL_OUT_PATH/$nv" \
			"$RULE_PATH/err-detect/l3err.dl"
	echo "Concat $nv L3 results"
	cd "$DL_OUT_PATH/$nv" && cat L3*.csv > all-L3.csv
done

for dapplib in "${dapplibs[@]}"; do
	$SOUFFLE -F "$DL_IN_PATH/dapphub/$dapplib" \
			-D "$DL_OUT_PATH/dapphub/$dapplib" \
			"$RULE_PATH/err-detect/l1err.dl"
	echo "Concat $dapplib L1 results"
	cd "$DL_OUT_PATH/dapphub/$dapplib" && cat L1*.csv > all-L1.csv

	$SOUFFLE -F "$DL_IN_PATH/dapphub/$dapplib" \
			-D "$DL_OUT_PATH/dapphub/$dapplib" \
			"$RULE_PATH/err-detect/l2err.dl"
	echo "Concat $dapplib L2 results"
	cd "$DL_OUT_PATH/dapphub/$dapplib" && cat L2*.csv > all-L2.csv

	$SOUFFLE -F "$DL_IN_PATH/dapphub/$dapplib" \
			-D "$DL_OUT_PATH/dapphub/$dapplib" \
			"$RULE_PATH/err-detect/l3err.dl"
	echo "Concat $dapplib L3 results"
	cd "$DL_OUT_PATH/dapphub/$dapplib" && cat L3*.csv > all-L3.csv
done

cd "$DL_OUT_PATH/dapphub"
for x in ds-*; do cat "$x"/all-L1.csv ; done > l1-total.csv
for x in ds-*; do cat "$x"/all-L2.csv ; done > l2-total.csv
for x in ds-*; do cat "$x"/all-L3.csv ; done > l3-total.csv


set +x
printf "alias ll='ls -alh'\nalias l='ll -ctr'" >> /root/.bashrc
cd "$BASE_PATH"
printf "##############################################################\n"
printf "#            Reproducing Evaluation Starts Here              #\n"
printf "##############################################################\n"
$SCRIPT_PATH/rq1.sh
$SCRIPT_PATH/rq2.sh
$SCRIPT_PATH/rq3.sh

bash
