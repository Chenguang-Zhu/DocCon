#!/usr/bin/env bash

BASE_PATH="/opt/doccon"
SCRIPT_DIR=$BASE_PATH/scripts

### extract code facts
$SCRIPT_DIR/openzeppelin.sh
$SCRIPT_DIR/erc721-extensions.sh
$SCRIPT_DIR/dapphublib.sh


### extract doc facts
echo "Clean facts generated last time" && \
	rm -rf "$BASE_PATH/doc_facts" && \
	cd "$BASE_PATH/smart_factbase" && \
	./batch-450 && \
	./batch-erc721 && \
	./batch-dapp && cd "$BASE_PATH"
