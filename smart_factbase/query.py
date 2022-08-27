import json
import collections

from macros import CODE_FACTS_OUTPUT_DIR
from macros import DOC_FACTS_OUTPUT_DIR

from match import fuzzyMatch

def checkContractCodeDocInconsistency(lib, version, contract_name, level):
    print('=== Querying ' + contract_name)
    code_facts_file = CODE_FACTS_OUTPUT_DIR + '/' + lib + '/' + version + '/' + contract_name + '.facts'
    contract_code_facts = []
    with open(code_facts_file, 'r') as fr:
        lines = fr.readlines()
    for i in range(len(lines)):
        contract_code_facts.append(lines[i].strip())
    doc_facts_file = DOC_FACTS_OUTPUT_DIR + '/' + lib + '/' + version + '/' + contract_name + '.json'
    contract_doc_facts = []
    with open(doc_facts_file, 'r') as fr:
        doc_facts = json.load(fr, object_pairs_hook=collections.OrderedDict)
        for f in doc_facts:
            contract_doc_facts.append(f)
    if level == '1':
        # direct inclusion
        for df in contract_doc_facts:
            if isAnotherContract(df, contract_name):
                continue
            if df in contract_code_facts:
                pass
            elif fuzzyMatch(df, contract_code_facts):
                pass
            else:
                if isInterfaceDocFacts(df):
                    continue
                print('INCONSIS LV1: ', df, 'in the doc, but not in the code!')
        # call chain
        # inheritance
    elif level == '2':
        for cf in contract_code_facts:
            if cf not in contract_doc_facts:
                if ',REQUIRE,' in cf or ',REVERTIF,' in cf or ',EMIT,' in cf or ',EMITIF,' in cf:
                    print('INCONSIS LV2: ', cf, 'in the code, but not in the doc!')
                else:
                    pass
    else:
        for cf in contract_code_facts:
            if cf not in contract_doc_facts:
                if ',REQUIRE,' in cf or ',REVERTIF,' in cf or ',EMIT,' in cf or ',EMITIF,' in cf:
                    pass
                else:
                    print('INCONSIS LV3: ', cf, 'in the code, but not in the doc!')


def checkFuncCodeDocInconsistency(lib, version, contract_name, func_name, level):
    print('=== Querying ' + contract_name + '.' + func_name)
    code_facts_file = CODE_FACTS_OUTPUT_DIR + '/' + lib + '/' + version + '/' + contract_name + '.facts'
    func_code_facts = []
    with open(code_facts_file, 'r') as fr:
        lines = fr.readlines()
    for i in range(len(lines)):
        if lines[i].strip().split(',')[0] == 'FUNCTION' and lines[i].strip().split(',')[1] == contract_name + '.' + func_name:
            func_code_facts.append(lines[i].strip())
    doc_facts_file = DOC_FACTS_OUTPUT_DIR + '/' + lib + '/' + version + '/' + contract_name + '.json'
    func_doc_facts = []
    with open(doc_facts_file, 'r') as fr:
        doc_facts = json.load(fr, object_pairs_hook=collections.OrderedDict)
    for f in doc_facts:
        if f.split(',')[0] == 'FUNCTION' and f.split(',')[1] == contract_name + '.' + func_name:
            func_doc_facts.append(f)
    if level == '1':
        # direct inclusion
        for df in func_doc_facts:
            if df not in func_code_facts:
                if isInterfaceDocFacts(df):
                    continue
                print('INCONSIS LV1: ', df, 'in the doc, but not in the code!')
        # call chain
        # inheritance
    elif level == '2':
        for cf in func_code_facts:
            if cf not in func_doc_facts:
                if ',REQUIRE,' in cf or ',REVERTIF,' in cf or ',EMIT,' in cf or ',EMITIF,' in cf:
                    print('INCONSIS LV2: ', cf, 'in the code, but not in the doc!')
                else:
                    pass
    else:
        for cf in func_code_facts:
            if cf not in func_doc_facts:
                if ',REQUIRE,' in cf or ',REVERTIF,' in cf or ',EMIT,' in cf or ',EMITIF,' in cf:
                    pass
                else:
                    print('INCONSIS LV3: ', cf, 'in the code, but not in the doc!')

def isInterfaceDocFacts(df):
    if df.split(',')[0] == 'FUNCTION' and df.split(',')[1].startswith('I'):
        if df.split(',')[2] in ['EMIT', 'EMITIF', 'REQUIRE', 'REVERTIF']:
            return True
    return False

def isAnotherContract(df, contract_name):
    if df.split(',')[1].split('.')[0] != contract_name:
        return True
    return False
