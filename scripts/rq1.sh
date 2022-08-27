#!/usr/bin/env bash
set -eu

BASE_PATH=/opt/doccon
SAMPLES_PATH="$BASE_PATH/exp/dl/labelled"
OUT_PATH="$BASE_PATH/exp/dl/out"


RED='\033[0;31m'
NC='\033[0m' # No Color
function assert_num_equal() {
    local lineno=$3
    if [[ "$1" -ne "$2" ]]; then
        printf "${RED}Assertion failed: at $lineno ${NC}: $1 not equal to $2.\n"
    fi
}

printf "Compute Precision by Sampling (RQ1 in the paper)\n"

printf "##############################################################\n"
printf "#                      OpenZeppelin                          #\n"
printf "##############################################################\n"

echo "[OpenZeppelin] Load All (labelled) Level-1 Errors"
OZ_450_DIR=$OUT_PATH/openzeppelin/v4.5.0
OZ_1_TOTAL=$(wc -l < $OZ_450_DIR/all-L1.csv)
OZ_1_TP=$(wc -l < $SAMPLES_PATH/OZ-lv1/tp.csv)
OZ_1_FP=$(wc -l < $SAMPLES_PATH/OZ-lv1/fp.csv)
assert_num_equal $OZ_1_TOTAL 49 ${LINENO}
printf "Level-1 Total: %d (files: %s)\n" "$OZ_1_TOTAL" "$OZ_450_DIR/L1*.csv"
printf "True Positive:  %d (file: %s)\n"  "$OZ_1_TP" "$SAMPLES_PATH/OZ-lv1/tp.csv"
printf "False Positive: %d (file: %s)\n"  "$OZ_1_FP" "$SAMPLES_PATH/OZ-lv1/fp.csv"
printf "OpenZeppelin Level-1 Precision: %.2f\n" "$(dc -e "4 k $OZ_1_TP  $OZ_1_TP  $OZ_1_FP + / p")" 

printf "=================================================\n"
printf "[OpenZeppelin] Load All and Sampled (labelled) Level-2 Errors\n"
OZ_2_TOTAL=$(wc -l < $OUT_PATH/openzeppelin/v4.5.0/all-L2.csv)
OZ_2_TP=$(wc -l < $SAMPLES_PATH/OZ-lv2/tp.csv)
OZ_2_FP=$(wc -l < $SAMPLES_PATH/OZ-lv2/fp.csv)
assert_num_equal $OZ_2_TOTAL 567 ${LINENO}
printf "Level-2 Total: %d (files: %s)\n" "$OZ_2_TOTAL" "$OZ_450_DIR/L2*.csv"
printf "Sample size:    %d\n"  "$(dc -e "$OZ_2_TP  $OZ_2_FP + p")"
printf "True Positive:  %d (file: %s)\n" "$OZ_2_TP"  "$SAMPLES_PATH/OZ-lv2/tp.csv"
printf "False Positive: %d (file: %s)\n" "$OZ_2_FP"  "$SAMPLES_PATH/OZ-lv2/fp.csv"
printf "OpenZeppelin Level-2 Precision (sampled): %.2f\n" "$(dc -e "4 k $OZ_2_TP  $OZ_2_TP  $OZ_2_FP + / p")" 

echo "================================================="
echo "[OpenZeppelin] Load All (not-labelled) Level-3 Errors"
OZ_3_TOTAL=$(wc -l < $OUT_PATH/openzeppelin/v4.5.0/all-L3.csv)
assert_num_equal $OZ_3_TOTAL 3741 ${LINENO}
printf "Level-3 Total: %d (files: %s)\n" "$OZ_3_TOTAL" "$OZ_450_DIR/L3*.csv"


printf "##############################################################\n"
printf "#                        ERC721-Ext.                         #\n"
printf "##############################################################\n"
printf "[ERC721-Ext.] Load All (labelled) Level-1 Errors\n"
ERC_DIR=$OUT_PATH/erc721-extensions/v0.0.18
ERC_1_TOTAL=$(wc -l < $ERC_DIR/all-L1.csv)
ERC_1_TP=$(wc -l < $SAMPLES_PATH/ERC-lv1/tp.csv)
ERC_1_FP=$(wc -l < $SAMPLES_PATH/ERC-lv1/fp.csv)
assert_num_equal $ERC_1_TOTAL 3 ${LINENO}
printf "Level-1 Total: %d (files: %s)\n" "$ERC_1_TOTAL" "$ERC_DIR/L1*.csv"
printf "True Positive: %d  (file: %s)\n" "$ERC_1_TP"    "$SAMPLES_PATH/ERC-lv1/tp.csv"
printf "False Positive: %d (file: %s)\n" "$ERC_1_FP"    "$SAMPLES_PATH/ERC-lv1/fp.csv"
printf "ERC721-Ext. Level-1 precision: %.2f\n" "$(dc -e "4 k $ERC_1_TP  $ERC_1_TP  $ERC_1_FP + / p")" 

printf "=================================================\n"
printf "[ERC721-Ext.] Load All (labelled) Level-2 Errors\n"
ERC_2_TOTAL=$(wc -l < $OUT_PATH/erc721-extensions/v0.0.18/all-L2.csv)
ERC_2_TP=$(wc -l < $SAMPLES_PATH/ERC-lv2/tp.csv)
ERC_2_FP=$(wc -l < $SAMPLES_PATH/ERC-lv2/fp.csv)
assert_num_equal $ERC_2_TOTAL 79 ${LINENO}
printf "Level-2 Total: %d (files: %s)\n" "$ERC_2_TOTAL" "$ERC_DIR/L2*.csv"
#printf "Sample size:    %d\n"  "$(dc -e "$ERC_2_TP  $ERC_2_FP + p")"
printf "True Positive: %d  (file: %s)\n" "$ERC_2_TP"    "$SAMPLES_PATH/ERC-lv1/tp.csv"
printf "False Positive: %d (file: %s)\n" "$ERC_2_FP"    "$SAMPLES_PATH/ERC-lv1/fp.csv"
printf "ERC721-Ext. Level-2 precision: %.2f\n" "$(dc -e "4 k $ERC_2_TP  $ERC_2_TP  $ERC_2_FP + / p")" 

printf "=================================================\n"
printf "[ERC721-Ext.] Load All (not-labelled) Level-3 Errors\n"
ERC_3_TOTAL=$(wc -l < $OUT_PATH/erc721-extensions/v0.0.18/all-L3.csv)
printf "Level-3 Total: %d (files: %s)\n" "$ERC_3_TOTAL" "$ERC_DIR/L3*.csv"
assert_num_equal $ERC_3_TOTAL 377 ${LINENO}


printf "##############################################################\n"
printf "#                          Dappsys                           #\n"
printf "##############################################################\n"

printf "[Dappsys] Load All (labelled) Level-1 Errors\n"
DAPP_1_TP=$(wc -l < $SAMPLES_PATH/Dapp-lv1/tp.csv)
DAPP_1_FP=$(wc -l < $SAMPLES_PATH/Dapp-lv1/fp.csv)
DAPP_1_TOTAL=$(sort -u "$OUT_PATH/dapphub/l1-total.csv" | wc -l)
assert_num_equal $DAPP_1_TOTAL 4 ${LINENO}
printf "Level-1 Total: %d\n" $DAPP_1_TOTAL
#awk '{count+=$1} END{print count}' <<< \
#	"$(for x in "$OUT_PATH"/dapphub/*; do  wc -l <  "$x/all-L1.csv"; done )"
printf "(files: %s)\n" "$OUT_PATH/dapphub/l1-total.csv"
printf "True Positive: %d  (file: %s)\n" "$DAPP_1_TP" "$SAMPLES_PATH/Dapp-lv1/tp.csv"
printf "False Positive: %d (file: %s)\n" "$DAPP_1_FP" "$SAMPLES_PATH/Dapp-lv1/fp.csv"
printf "Dappsys Level-1 precision: %.2f\n" "$(dc -e "4 k $DAPP_1_TP  $DAPP_1_TP  $DAPP_1_FP + / p")" 

printf "=================================================\n"
printf "[Dappsys] Load All (labelled) Level-2 Errors\n"
DAPP_2_TP=$(wc -l < $SAMPLES_PATH/Dapp-lv2/tp.csv)
DAPP_2_FP=$(wc -l < $SAMPLES_PATH/Dapp-lv2/fp.csv)
DAPP_2_TOTAL=$(sort -u "$OUT_PATH/dapphub/l2-total.csv" | wc -l)
assert_num_equal $DAPP_2_TOTAL 141 ${LINENO}
printf "Level-2 Total: %d\n" $DAPP_2_TOTAL
#awk '{count+=$1} END{print count}' <<< \
#"$(for x in "$OUT_PATH"/dapphub/*; do  wc -l <  "$x/all-L2.csv"; done )"
printf "(files: %s)\n" "$OUT_PATH/dapphub/l2-total.csv"
#printf "Sample size:    %d\n"  "$(dc -e "$DAPP_2_TP  $DAPP_2_FP + p")"
printf "True Positive: %d  (file: %s)\n" "$DAPP_2_TP"  "$SAMPLES_PATH/Dapp-lv2/tp.csv"
printf "False Positive: %d (file: %s)\n" "$DAPP_2_FP"  "$SAMPLES_PATH/Dapp-lv2/fp.csv"
printf "Dappsys Level-2 precision: %.2f\n" "$(dc -e "4 k $DAPP_2_TP  $DAPP_2_TP  $DAPP_2_FP + / p")" 

printf "=================================================\n"
printf "[Dappsys] Load All (not-labelled) Level-3 Errors\n"
DAPP_3_TOTAL=$(sort -u "$OUT_PATH/dapphub/l3-total.csv" | wc -l)
assert_num_equal $DAPP_3_TOTAL 448 ${LINENO}
printf "Level-3 Total: %d\n" $DAPP_3_TOTAL
#awk '{count+=$1} END{print count}' <<< \
#	"$(for x in "$OUT_PATH"/dapphub/*; do  wc -l <  "$x/all-L3.csv"; done )"
printf "(files: %s)\n" "$OUT_PATH/dapphub/l3-total.csv"
