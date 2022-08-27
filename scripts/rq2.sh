#!/usr/bin/env bash
set -ueET
shopt -s expand_aliases
alias grep='grep --color'

BASE_PATH="/opt/doccon"
RESULT_PATH="$BASE_PATH/exp/dl/out"

OZ450="openzeppelin/v4.5.0"
ERC0018="erc721-extensions/v0.0.18"

RED='\033[0;31m'
NC='\033[0m' # No Color
failure() {
        local lineno=$1
        local msg=$2
        printf "${RED}Failed at $lineno ${NC}: $msg\n"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

echo "All Reported Cases (RQ2 in the paper)"
echo "==================================================================================";
echo "Reported issue 1: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3359";
echo "Contain 2 inconsistencies    Confirmed Fixed"
grep -PH '^ERC20\t_transfer\trecipient' "$RESULT_PATH/$OZ450/L1HasParam.csv"
grep -PH '^ERC20\t_transfer\tsender'    "$RESULT_PATH/$OZ450/L1HasParam.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 2: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3360";
echo "Contain 2 inconsistencies    Confirmed Fixed"
grep -PH '^ERC777\t_mint\tdata' "$RESULT_PATH/$OZ450/L1HasParam.csv"
grep -PH '^ERC777\t_mint\toperator' "$RESULT_PATH/$OZ450/L1HasParam.csv"


echo "----------------------------------------------------------------------------------";
echo "Reported issue 3: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3361";
echo "Contain 2 inconsistencies    NotConfirmed NotFixed"
grep -PH '^IERC777\tsend\toperatorData' "$RESULT_PATH/$OZ450/L1HasParam.csv"
grep -PH '^IERC777\tburn\toperatorData' "$RESULT_PATH/$OZ450/L1HasParam.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 4: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3362";
echo "Contain 3 inconsistencies    Confirmed NotFixed"
grep -PH '^ERC721\tsafeTransferFrom\t\$Cmp\(\$Literal\(from\), \$Literal\(address\(0\)\), NEQ\)' \
	 "$RESULT_PATH/$OZ450/L1Require.csv"
grep -PH '^ERC721\ttransferFrom\t\$Cmp\(\$Literal\(from\), \$Literal\(address\(0\)\), NEQ\)' \
	 "$RESULT_PATH/$OZ450/L1Require.csv"
grep -PH '^ERC721\t_safeTransfer\t\$Cmp\(\$Literal\(from\), \$Literal\(address\(0\)\), NEQ\)' \
	 "$RESULT_PATH/$OZ450/L1Require.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 5: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3363";
echo "Contain 1 inconsistencies    Confirmed Fixed"
grep -PH 'ERC721\t_safeMint\tdata'  "$RESULT_PATH/$OZ450/L1HasParam.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 6: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3366";
echo "Contain 4 inconsistencies    Confirmed NotFixed"
grep -PH '^EnumerableMap\t_at\t\$Cmp\(\$Literal\(index\), \$Literal\({length}\), LT\)'\
	 "$RESULT_PATH/$OZ450/L1Require.csv"
grep -PH '^EnumerableMap\tat\t\$Cmp\(\$Literal\(index\), \$Literal\({length}\), LT\)'\
	 "$RESULT_PATH/$OZ450/L1Require.csv"
grep -PH '^EnumerableSet\t_at\t\$Cmp\(\$Literal\(index\), \$Literal\({length}\), LT\)'\
	 "$RESULT_PATH/$OZ450/L1Require.csv"
grep -PH '^EnumerableSet\tat\t\$Cmp\(\$Literal\(index\), \$Literal\({length}\), LT\)'\
	 "$RESULT_PATH/$OZ450/L1Require.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 7: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3367";
echo "Contain 2 inconsistencies    Confirmed Fixed"
grep -PH '^ERC1155\t_beforeTokenTransfer\tamount' "$RESULT_PATH/$OZ450/L1HasParam.csv"
grep -PH '^ERC1155\t_beforeTokenTransfer\tid'     "$RESULT_PATH/$OZ450/L1HasParam.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 8: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3368";
echo "Contain 2 inconsistencies    Confirmed Fixed"
echo "(The 2 inconsistencies involves overloaded methods, thus only 1 fact here)"
grep -PH '^VestingWallet\trelease\tTokensReleased\t\$Bool\(True\)' "$RESULT_PATH/$OZ450/L1Emit.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 9: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3369";
echo "Contain 3 inconsistencies    Confirmed Fixed"
grep -PH '^Escrow\tdeposit\tDeposited\t\$Bool\(True\)' "$RESULT_PATH/$OZ450/L2Emit.csv"
grep -PH '^Escrow\twithdraw\tWithdrawn\t\$Bool\(True\)' "$RESULT_PATH/$OZ450/L2Emit.csv"
grep -PH '^PullPayment\t_asyncTransfer\tDeposited\t\$Bool\(True\)' "$RESULT_PATH/$OZ450/L2Emit.csv"
#grep -PH '^PullPayment\twithdrawPayments\tWithdrawn\t\$Bool\(True\)' "$RESULT_PATH/$OZ450/L2Emit.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 10: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3376";
echo "Contain 1 inconsistency    Confirmed Fixed"
grep -PH '^AccessControl\t_grantRole\tRoleGranted\t\$Bool\(True\)'  "$RESULT_PATH/$OZ450/L2Emit.csv"
#grep -PH '^AccessControl\t_revokeRole\tRoleRevoked\t\$Bool\(True\)' "$RESULT_PATH/$OZ450/L2Emit.csv"

# 3370 is ignored, 4.6.0 only
# echo "----------------------------------------------------------------------------------";
# echo "Reported issue 11: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3370";
# echo "Contain 1 inconsistency    Confirmed Fixed"
# grep -PH '^Governor\t_castVote\tVoteCastWithParams\t\$Bool\(True\)'  "$RESULT_PATH/$OZ450/L2Emit.csv"
 
# 3365 is ignored, 4.6.0 only, and is lv 3
# echo "----------------------------------------------------------------------------------";
# echo "Reported issue 12: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3375";
# echo "Contain 1 inconsistency    Confirmed Fixed"
# grep -PH '^Governor\t_countVote\tparams'  "$RESULT_PATH/$OZ450/L3HasParam.csv"


echo "----------------------------------------------------------------------------------";
echo "Reported issue 11: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3377";
echo "Contain 1 inconsistency    Confirmed Fixed"
grep -PH '^ERC3156FlashBorrower\tonFlashLoan' "$RESULT_PATH/$OZ450/L1HasFn.csv"


echo "----------------------------------------------------------------------------------";
echo "Reported issue 12: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3374";
echo "Contain 1 inconsistency    Confirmed Fixed"
grep -PH '^ERC1155\t_mintBatch\tTransferBatch\t\$Bool\(True\)' "$RESULT_PATH/$OZ450/L2Emit.csv"


echo "----------------------------------------------------------------------------------";
echo "Reported issue 13: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3378";
echo "Contain 2 inconsistencies    NotConfirmed NotFixed"
grep -PH 'IERC1820Registry\tsetInterfaceImplementer\tinterfaceHash' "$RESULT_PATH/$OZ450/L1HasParam.csv"
grep -PH 'IERC1820Registry\tgetInterfaceImplementer\tinterfaceHash' "$RESULT_PATH/$OZ450/L1HasParam.csv"


## erc721-ext.
echo "----------------------------------------------------------------------------------";
echo "Reported issue 14: https://github.com/1001-digital/erc721-extensions/issues/12";
echo "Contain 2 inconsistencies    Confirmed Fixed"
grep -PH 'HasSecondarySalesFees\tgetFeeRecipients\tWithFees\tgetFeeRecipients' "$RESULT_PATH/$ERC0018/L1Override.csv"
grep -PH 'HasSecondarySalesFees\tgetFeeBps\tWithFees\tgetFeeBps'               "$RESULT_PATH/$ERC0018/L1Override.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 15: https://github.com/1001-digital/erc721-extensions/issues/13";
echo "Contain 5 inconsistencies    Confirmed Fixed"
grep -PH 'WithMarketOffers\t_cancelOffer\tOfferWithdrawn\t\$Bool\(True\)'         "$RESULT_PATH/$ERC0018/L2Emit.csv"
grep -PH 'WithMarketOffers\t_beforeTokenTransfer\tOfferWithdrawn\t\$Bool\(True\)' "$RESULT_PATH/$ERC0018/L2Emit.csv"
grep -PH 'WithMarketOffers\tcancelOffer\tOfferWithdrawn\t\$Bool\(True\)'          "$RESULT_PATH/$ERC0018/L2Emit.csv"
grep -PH 'WithMarketOffers\t_makeOffer\tOfferCreated\t\$Bool\(True\)'             "$RESULT_PATH/$ERC0018/L2Emit.csv"
grep -PH 'WithMarketOffers\tmakeOfferTo\tOfferCreated\t\$Bool\(True\)'            "$RESULT_PATH/$ERC0018/L2Emit.csv"

## dapphub
echo "----------------------------------------------------------------------------------";
echo "Reported issue 16: https://github.com/dapphub/ds-chief/issues/14";
echo "Contain 2 inconsistencies    NotConfirmed NotFixed"
grep -PH 'DSChiefApprovals\tlock\tLogLockFree\t\$Bool\(True\)' "$RESULT_PATH/dapphub/ds-chief/L1Emit.csv"
grep -PH 'DSChiefApprovals\tfree\tLogLockFree\t\$Bool\(True\)' "$RESULT_PATH/dapphub/ds-chief/L1Emit.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 17: https://github.com/dapphub/ds-chief/issues/16";
echo "Contain 2 inconsistencies    NotConfirmed NotFixed"
grep -PH 'DSChiefApprovals\tvote\tEtch\t\$Bool\(True\)' "$RESULT_PATH/dapphub/ds-chief/L2Emit.csv"
grep -PH 'DSChiefApprovals\tetch\tEtch\t\$Bool\(True\)' "$RESULT_PATH/dapphub/ds-chief/L2Emit.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 18: https://github.com/dapphub/ds-auth/issues/14";
echo "Contain 1 inconsistency    NotConfirmed NotFixed"
grep -PH 'DSAuth\tsetOwner\tLogSetOwner\t\$Bool\(True\)' "$RESULT_PATH/dapphub/ds-auth/L2Emit.csv"

echo "----------------------------------------------------------------------------------";
echo "Reported issue 19: https://github.com/dapphub/ds-token/issues/39";
echo "Contain 2 inconsistencies    NotConfirmed NotFixed"
grep -PH 'DSToken\ttransferFrom\tTransfer\t\$Bool\(True\)' "$RESULT_PATH/dapphub/ds-token/L2Emit.csv"
grep -PH 'DSToken\ttransfer\tTransfer\t\$Bool\(True\)' "$RESULT_PATH/dapphub/ds-token/L2Emit.csv"

## conclusion
echo "==================================================================================";
echo "In total: 40 reported inconsistencies, 25 level-1, 15 level-2, 29 confirmed, 22 fixed."
