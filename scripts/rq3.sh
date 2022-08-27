#!/usr/bin/env bash
# RQ3: categorization of errors (lv1 all true positive, lv2 sampled true positive)
set -u

BASE_PATH=/opt/doccon
OUT=$BASE_PATH/exp/dl/out
SAMPLES=$BASE_PATH/exp/dl/labelled
OZ450=openzeppelin/v4.5.0
ERC=erc721-extensions/v0.0.18

RED='\033[0;31m'
NC='\033[0m' # No Color
function assert_num_equal() {
    local lineno=$3
    if [[ "$1" -ne "$2" ]]; then
        printf "${RED}Assertion failed: at $lineno ${NC}: $1 not equal to $2.\n"
    fi
}

printf "Categorization of Errors (RQ3 in the paper)\n"
printf "##############################################################\n"
printf "#                          Level-1                           #\n"
printf "##############################################################\n"
ALL_LV1_TP=$SAMPLES/lv1-tp.csv
cat "$SAMPLES/OZ-lv1/tp.csv" "$SAMPLES/ERC-lv1/tp.csv" "$SAMPLES/Dapp-lv1/tp.csv" > "$ALL_LV1_TP"

L1EE=$(while IFS= read -r line; do
rg -Fw "$line" $OUT/$OZ450/L1Emit.csv \
    $OUT/$ERC/L1Emit.csv  $OUT/dapphub/ds-*/L1Emit.csv;
done < "$ALL_LV1_TP" | wc -l)
assert_num_equal "$L1EE" 3 ${LINENO}
printf "Event Emission: %d\n" "$L1EE"
#printf "(grep '%s/*/L1Emit.csv' against '%s')\n\n" "$OUT" "$ALL_LV1_TP"

L1TR=$(while IFS= read -r line; do
rg -Fw "$line" $OUT/$OZ450/L1Re*.csv \
    $OUT/$ERC/L1Re*.csv  $OUT/dapphub/ds-*/L1Re*.csv;
done < "$ALL_LV1_TP" | wc -l)
assert_num_equal "$L1TR" 17 ${LINENO}
printf "Transaction Requirement and Reversion: %d\n" "$L1TR"
#printf "(grep '%s/*/L1Re*.csv' against '%s')\n\n" "$OUT" "$ALL_LV1_TP"

L1EC=$(while IFS= read -r line; do
rg -Fw "$line" \
    $OUT/$OZ450/L1Has*.csv $OUT/$ERC/L1Has*.csv  $OUT/dapphub/ds-*/L1Has*.csv \
    $OUT/$OZ450/L1CtHasMod.csv $OUT/$ERC/L1CtHasMod.csv  $OUT/dapphub/ds-*/L1CtHasMod.csv;
done < "$ALL_LV1_TP" | wc -l)
assert_num_equal "$L1EC" 20 ${LINENO}
printf "Element Containment: %d\n" "$L1EC"
#printf "(grep '%s/*/L1Has*.csv' against '%s')\n\n" "$OUT" "$ALL_LV1_TP"

L1ER=$(while IFS= read -r line; do
rg -Fw "$line" \
    $OUT/$OZ450/L1Override.csv $OUT/$ERC/L1Override.csv  $OUT/dapphub/ds-*/L1Override.csv \
    $OUT/$OZ450/L1Inherit.csv $OUT/$ERC/L1Inherit.csv  $OUT/dapphub/ds-*/L1Inherit.csv \
    $OUT/$OZ450/L1FnHasMod.csv $OUT/$ERC/L1FnHasMod.csv  $OUT/dapphub/ds-*/L1FnHasMod.csv;
done < "$ALL_LV1_TP" | wc -l)
assert_num_equal "$L1ER" 3 ${LINENO}
printf "Element Reference: %d\n" "$L1ER"
#printf "(grep '%s/*/L1Override.csv' against '%s')\n\n" "$OUT" "$ALL_LV1_TP"


printf "##############################################################\n"
printf "#                          Level-2                           #\n"
printf "##############################################################\n"
ALL_LV2_TP=$SAMPLES/lv2-tp.csv
cat "$SAMPLES/OZ-lv2/tp.csv" "$SAMPLES/ERC-lv2/tp.csv" "$SAMPLES/Dapp-lv2/tp.csv" > "$ALL_LV2_TP"

L2EE=$(while IFS= read -r line; do
rg -Fw "$line" $OUT/$OZ450/L2Emit.csv \
    $OUT/$ERC/L2Emit.csv  $OUT/dapphub/ds-*/L2Emit.csv;
done < "$ALL_LV2_TP" | wc -l)
assert_num_equal $L2EE 106 ${LINENO}
printf "Event Emission: %d\n" "$L2EE"
#printf "(grep '%s/*/L2Emit.csv' against '%s')\n\n" "$OUT" "$ALL_LV2_TP"

L2TR=$(while IFS= read -r line; do
rg -Fw "$line" $OUT/$OZ450/L2Re*.csv \
    $OUT/$ERC/L2Re*.csv  $OUT/dapphub/ds-*/L2Re*.csv;
done < "$ALL_LV2_TP" | wc -l)
assert_num_equal $L2TR 191 ${LINENO}
printf "Transaction Requirement and Reversion: %d\n" "$L2TR"
#printf "(grep '%s/*/L2Re*.csv' against '%s')\n" "$OUT" "$ALL_LV2_TP"
