# DocCon: Solidity API documentation error checker

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7034128.svg)](https://doi.org/10.5281/zenodo.7034128)

The latest version of this repo can be found at: https://github.com/uxhg/doccon-artifact

DocCon is a tool for detecting inconsistencies between documentations and the corresponding code for
Solidity smart contract libraries.

This repo provides a docker to replicate evaluation done in the
[ASE 2022 paper](https://wuxh.info/static/pub/doccon.pdf).


## Prerequisites
+ Linux OS (tested on Debian/sid, Ubuntu/16.04)
+ Docker (tested with 20.10.14, should work on newer versions)
+ At least 3GB space for the docker image

## Installation
Clone this repo and build Docker image:
```sh
git clone https://github.com/Chenguang-Zhu/DocCon_Artifact.git
cd DocCon_Artifact
sudo docker build -t doccon .
```
Time estimation: 20–30 minutes (on modern hardware with good network condition)

If successful, at the end of the command line output should look similar to the following:
```sh
Successfully built 778036834c4e
Successfully tagged doccon:latest
```

## Run End-to-End Evaluation and Interprete the Results
After building the Docker image, you can start the Docker container:

```sh
sudo docker run --name doccon --rm -it doccon
```
Once started, the container will start the end-to-end evaluation process automatically, which consist of three parts.
+ Code facts extraction
+ Documentation fact extraction
+ Inconsistency discovery

The process may take about three minutes.

When it finishs the three steps, it will show results corresponding to the results presented in the
paper. It is recommended that your terminal window has at least 100 columns to easily read the results
on screen.

### Subjects
All the following evaluation are done for the three smart contract libraries.
+ [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts)
+ [ERC721-Extensions](https://github.com/1001-digital/erc721-extensions/)
+ [Dappsys](https://github.com/dapphub/dappsys)

### RQ1: Detected Errors of Different Levels for Three Libraries
DocCon defines three levels according to the severity of the doc-code inconsistency (errors).

+ For level-1 (most severe) errors, we inspect every case and label true positive cases and false
  positive ones to calculate the precision.

+ For level-2 errors, we only inspect and label some sampled cases. Numbers of all detected errors
  as well as precision calculated according to labelled cases are shown.

+ For level-3 (least severe) errors, we only list the total reported errors.

We also list file locations if you want to inspect the Datalog output and the labeled data.

Note that `L1*.csv` means there are a series of CSV files (actually TSV, tab-separated) beginning
with `L1`, containing errors detected by different rules.

You should see the following table, presenting data in Table.4 of the paper.

```
##############################################################
#                      OpenZeppelin                          #
##############################################################
[OpenZeppelin] Load All (labelled) Level-1 Errors
Level-1 Total: 49 (files: /opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1*.csv)
True Positive:  38 (file: /opt/doccon/exp/dl/labelled/OZ-lv1/tp.csv)
False Positive: 11 (file: /opt/doccon/exp/dl/labelled/OZ-lv1/fp.csv)
OpenZeppelin Level-1 Precision: 0.78
=================================================
[OpenZeppelin] Load All and Sampled (labelled) Level-2 Errors
Level-2 Total: 567 (files: /opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L2*.csv)
Sample size:    229
True Positive:  164 (file: /opt/doccon/exp/dl/labelled/OZ-lv2/tp.csv)
False Positive: 65 (file: /opt/doccon/exp/dl/labelled/OZ-lv2/fp.csv)
OpenZeppelin Level-2 Precision (sampled): 0.72
=================================================
[OpenZeppelin] Load All (not-labelled) Level-3 Errors
Level-3 Total: 3741 (files: /opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L3*.csv)
##############################################################
#                        ERC721-Ext.                         #
##############################################################
[ERC721-Ext.] Load All (labelled) Level-1 Errors
Level-1 Total: 3 (files: /opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L1*.csv)
True Positive: 3  (file: /opt/doccon/exp/dl/labelled/ERC-lv1/tp.csv)
False Positive: 0 (file: /opt/doccon/exp/dl/labelled/ERC-lv1/fp.csv)
ERC721-Ext. Level-1 precision: 1.00
=================================================
[ERC721-Ext.] Load All (labelled) Level-2 Errors
Level-2 Total: 79 (files: /opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L2*.csv)
True Positive: 58  (file: /opt/doccon/exp/dl/labelled/ERC-lv1/tp.csv)
False Positive: 21 (file: /opt/doccon/exp/dl/labelled/ERC-lv1/fp.csv)
ERC721-Ext. Level-2 precision: 0.73
=================================================
[ERC721-Ext.] Load All (not-labelled) Level-3 Errors
Level-3 Total: 377 (files: /opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L3*.csv)
##############################################################
#                          Dappsys                           #
##############################################################
[Dappsys] Load All (labelled) Level-1 Errors
Level-1 Total: 4
(files: /opt/doccon/exp/dl/out/dapphub/l1-total.csv)
True Positive: 2  (file: /opt/doccon/exp/dl/labelled/Dapp-lv1/tp.csv)
False Positive: 2 (file: /opt/doccon/exp/dl/labelled/Dapp-lv1/fp.csv)
Dappsys Level-1 precision: 0.50
=================================================
[Dappsys] Load All (labelled) Level-2 Errors
Level-2 Total: 141
(files: /opt/doccon/exp/dl/out/dapphub/l2-total.csv)
True Positive: 75  (file: /opt/doccon/exp/dl/labelled/Dapp-lv2/tp.csv)
False Positive: 66 (file: /opt/doccon/exp/dl/labelled/Dapp-lv2/fp.csv)
Dappsys Level-2 precision: 0.53
=================================================
[Dappsys] Load All (not-labelled) Level-3 Errors
Level-3 Total: 448
(files: /opt/doccon/exp/dl/out/dapphub/l3-total.csv)
```

### RQ2: Errors Reported to the Developers

We show all facts revealing inconsistency cases reported to the developers in the following format.
In total, there are 19 issues, containing 40 inconsistencies.

For each issue, we list the URL, the number of inconsistencies reported, whether the issue have been
confirmed or fixed, and the revealing facts.

```
All Reported Cases
==================================================================================
Reported issue 1: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3359
Contain 2 inconsistencies    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:ERC20 _transfer       recipient
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:ERC20 _transfer       sender
----------------------------------------------------------------------------------
Reported issue 2: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3360
Contain 2 inconsistencies    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:ERC777        _mint   data
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:ERC777        _mint   operator
----------------------------------------------------------------------------------
Reported issue 3: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3361
Contain 2 inconsistencies    NotConfirmed NotFixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:IERC777       send    operatorData
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:IERC777       burn    operatorData
----------------------------------------------------------------------------------
Reported issue 4: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3362
Contain 3 inconsistencies    Confirmed NotFixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv:ERC721 safeTransferFrom        $Cmp($Literal(from), $Literal(address(0)), NEQ)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv:ERC721 transferFrom    $Cmp($Literal(from), $Literal(address(0)), NEQ)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv:ERC721 _safeTransfer   $Cmp($Literal(from), $Literal(address(0)), NEQ)
----------------------------------------------------------------------------------
Reported issue 5: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3363
Contain 1 inconsistencies    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:ERC721        _safeMint       data
----------------------------------------------------------------------------------
Reported issue 6: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3366
Contain 4 inconsistencies    Confirmed NotFixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv:EnumerableMap  _at     $Cmp($Literal(index), $Literal({length}), LT)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv:EnumerableMap  at      $Cmp($Literal(index), $Literal({length}), LT)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv:EnumerableSet  _at     $Cmp($Literal(index), $Literal({length}), LT)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv:EnumerableSet  at      $Cmp($Literal(index), $Literal({length}), LT)
----------------------------------------------------------------------------------
Reported issue 7: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3367
Contain 4 inconsistencies    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:ERC1155       _beforeTokenTransfer    amount
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:ERC1155       _beforeTokenTransfer    id
----------------------------------------------------------------------------------
Reported issue 8: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3368
Contain 2 inconsistencies    Confirmed Fixed
(The 2 inconsistencies involves overloaded methods, thus only 1 fact here)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Emit.csv:VestingWallet     release TokensReleased  $Bool(True)
----------------------------------------------------------------------------------
Reported issue 9: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3369
Contain 3 inconsistencies    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L2Emit.csv:Escrow    deposit Deposited       $Bool(True)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L2Emit.csv:Escrow    withdraw        Withdrawn       $Bool(True)
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L2Emit.csv:PullPayment       _asyncTransfer  Deposited       $Bool(True)
----------------------------------------------------------------------------------
Reported issue 10: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3376
Contain 1 inconsistency    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L2Emit.csv:AccessControl     _grantRole      RoleGranted     $Bool(True)
----------------------------------------------------------------------------------
Reported issue 11: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3377
Contain 1 inconsistency    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasFn.csv:ERC3156FlashBorrower     onFlashLoan
----------------------------------------------------------------------------------
Reported issue 12: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3374
Contain 1 inconsistency    Confirmed Fixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L2Emit.csv:ERC1155   _mintBatch      TransferBatch   $Bool(True)
----------------------------------------------------------------------------------
Reported issue 13: https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3378
Contain 2 inconsistencies    NotConfirmed NotFixed
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:IERC1820Registry      setInterfaceImplementer interfaceHash
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv:IERC1820Registry      getInterfaceImplementer interfaceHash
----------------------------------------------------------------------------------
Reported issue 14: https://github.com/1001-digital/erc721-extensions/issues/12
Contain 2 inconsistencies    Confirmed Fixed
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L1Override.csv:HasSecondarySalesFees   getFeeRecipients        WithFees        getFeeRecipients
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L1Override.csv:HasSecondarySalesFees   getFeeBps       WithFees        getFeeBps
----------------------------------------------------------------------------------
Reported issue 15: https://github.com/1001-digital/erc721-extensions/issues/13
Contain 5 inconsistencies    Confirmed Fixed
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L2Emit.csv:WithMarketOffers    _cancelOffer    OfferWithdrawn  $Bool(True)
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L2Emit.csv:WithMarketOffers    _beforeTokenTransfer    OfferWithdrawn  $Bool(True)
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L2Emit.csv:WithMarketOffers    cancelOffer     OfferWithdrawn  $Bool(True)
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L2Emit.csv:WithMarketOffers    _makeOffer      OfferCreated    $Bool(True)
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/L2Emit.csv:WithMarketOffers    makeOfferTo     OfferCreated    $Bool(True)
----------------------------------------------------------------------------------
Reported issue 16: https://github.com/dapphub/ds-chief/issues/14
Contain 2 inconsistencies    NotConfirmed NotFixed
/opt/doccon/exp/dl/out/dapphub/ds-chief/L1Emit.csv:DSChiefApprovals     lock    LogLockFree     $Bool(True)
/opt/doccon/exp/dl/out/dapphub/ds-chief/L1Emit.csv:DSChiefApprovals     free    LogLockFree     $Bool(True)
----------------------------------------------------------------------------------
Reported issue 17: https://github.com/dapphub/ds-chief/issues/16
Contain 2 inconsistencies    NotConfirmed NotFixed
/opt/doccon/exp/dl/out/dapphub/ds-chief/L2Emit.csv:DSChiefApprovals     vote    Etch    $Bool(True)
/opt/doccon/exp/dl/out/dapphub/ds-chief/L2Emit.csv:DSChiefApprovals     etch    Etch    $Bool(True)
----------------------------------------------------------------------------------
Reported issue 18: https://github.com/dapphub/ds-auth/issues/14
Contain 1 inconsistency    NotConfirmed NotFixed
/opt/doccon/exp/dl/out/dapphub/ds-auth/L2Emit.csv:DSAuth        setOwner        LogSetOwner     $Bool(True)
----------------------------------------------------------------------------------
Reported issue 19: https://github.com/dapphub/ds-token/issues/39
Contain 2 inconsistencies    NotConfirmed NotFixed
/opt/doccon/exp/dl/out/dapphub/ds-token/L2Emit.csv:DSToken      transferFrom    Transfer        $Bool(True)
/opt/doccon/exp/dl/out/dapphub/ds-token/L2Emit.csv:DSToken      transfer        Transfer        $Bool(True)
==================================================================================
In total: 40 reported inconsistencies, 25 level-1, 15 level-2, 29 confirmed, 22 fixed.
```

### RQ3 Categorization of Errors

To study the errors in smart contract API documentations in depth, we categorized all the manually
validated true-positive cases.

The categorization can be determined according to which Datalog facts reveal the error. E.g., `ERC20
_transfer recipient` reveals an error and is a fact of predicate `L1HasParam`. Because `L*HasParam`
describes the containment relation between functions and parameters, we categorize it as "Element
Containment".

| Category                              | Files                                                               |
| -----------                           | -----------                                                         |
| Event Emission                        | `L*Emit.csv`                                                        |
| Transaction Requirement and Reversion | `L*Require.csv`, `L*Revert.csv `                                    |
| Element Containment                   | `L*HasFn.csv`, `L*HasParam.csv`, `L*CtHasMod`, `L*HasStateVar.csv`, |
| Element Reference                     | `L*Override.csv`, `L*FnHasMod.csv`, `L*Inherit.csv`                 |

We use labelled data to search in respective files (e.g., `L1Emit.csv` for level-1 Event Emission
errors) to print the number of errors in each category for level-1 errors.

You should see the following output. This should match the left side of Fig.10 in the paper.
We do not show level-2 results here since level-2 involves usages of manually sampled data.
```
Categorization of Errors (RQ3 in the paper)
##############################################################
#                          Level-1                           #
##############################################################
Event Emission: 3
Transaction Requirement and Reversion: 17
Element Containment: 20
Element Reference: 3

##############################################################
#                          Level-2                           #
##############################################################
Event Emission: 106
Transaction Requirement and Reversion: 191
```


## More Details
### Files and Directories
Inside docker everything we use resides inside `/opt/doccon`.
You can inspect:
+ `Code2Schema`, `smart_factbase`: the extractors we build to extract facts.
+ `datalog`: Datalog rules we used to query.
+ `exp/dl/in`: facts generated by extractors.
+ `exp/dl/out`: queried results, all our results above can be found in files under it.

```
├──📂 Code2Schema        # code facts extractor
├──📂 smart_factbase     # doc facts extractor
├──📂 datalog            # datalog definitions, inference rules
├──📂 library-src        # source of generated
├──📂 library-facts      # generated code facts, will be linked to exp/dl/in dir
├──📂 exp                # storing generated data and pre-installed data
|  ├─📂 dl               # datalog related
|  | ├─📂  in            # inference input, will link to generated codefacts and docfacts
|  | └─📂  out           # inference output
|  └─📂doc_facts         # generated doc facts, will be linked to exp/dl/in dir
|     ├─📂  dapphub
|     ├─📂  erc721-extensions
|     └─📂  openzeppelin
├──📄 entry.sh           # bash script which automatically run after the container starts
```

In all RQ1-RQ3 above, we also give file locations and you can inspect those files if interested in
details.


### All Detected Errors
We report the total level-1/2/3 numbers of detected errors in the Table.4 of the paper.
Those numbers can be verified by counting the numbers of lines of those files as below.
You can also inspect those files to see the corresponding facts.
```
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/all-L1.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/all-L2.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/all-L3.csv

/opt/doccon/exp/dl/out/dapphub/l1-total.csv
/opt/doccon/exp/dl/out/dapphub/l2-total.csv
/opt/doccon/exp/dl/out/dapphub/l3-total.csv

/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/all-L1.csv
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/all-L2.csv
/opt/doccon/exp/dl/out/erc721-extensions/v0.0.18/all-L3.csv
```

### Interpretation of Files
Files mentioned in the previous section (e.g., `all-L1.csv`, `all-L2.csv`) are concatenation of
standalone files residing in the same directories. For example, under
`/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/`, there are: 
```
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1CtHasMod.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Revert.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Require.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Override.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Inherit.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasStateVar.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasParam.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1HasFn.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1FnHasMod.csv
/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/L1Emit.csv 
``` 

`/opt/doccon/exp/dl/out/openzeppelin/v4.5.0/all-L1.csv` are concatenation of those files, all of
which are tab-separated value files. Each file contains errors of a specific type of one of the
three levels and each line corresponds to a detected error.

For example, `L1HasParam.csv` contains Level-1 errors, related to existence of function parameters.
In that file, `ERC1155 _beforeTokenTransfer amount` indicates that documentation of contract
`ERC1155` indicates function `_beforeTokenTransfer` has a parameter named `amount` but not in the
code.

You can find out how to interpret other CSV files by checking Datalog files in
`datalog/err-detect/` and related descriptions in the paper.

---

If you would like to use DocCon in your research, please cite our ASE'22 paper.

```latex
@inproceedings{ZhuETAL2022DocCon,
  author = {Zhu, Chenguang and Liu, Ye and Wu, Xiuheng and Li, Yi},
  booktitle = {Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering},
  title = {Identifying Solidity Smart Contract API Documentation Errors},
  year = {2022}
}
```
