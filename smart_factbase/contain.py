import collections
import json
from typing import Set, List

from datalog.pred import HasFnFact, HasParamFact, FnModFact, StateVarFact, CallFact, SouffleList, \
    CtModFact
from macros import CODE_FACTS_OUTPUT_DIR


def extractHASFUNCTIONFacts(lib, version, sentence) -> (List[str], Set[HasFnFact]):
    all_contracts, all_functions, _ = getAllContractsAndFunctionsAndParams(lib, version)
    sentence_facts: List[str] = []
    sentence_facts_dl: Set[HasFnFact] = set()
    for word in sentence.strip().split():
        word = word.replace('`', '')
        word = word.strip().strip('.').strip(',').strip('{').strip('}')
        if '.' in word:  # T28
            # print(word)
            contract_name = word.split('.')[0].strip('"').strip('\'')
            func_name = word.split('.')[1].strip('.').strip(',').strip(';').strip('"').strip('\'')
            # if contract_name not in all_contracts or func_name not in all_functions:
            if func_name not in all_functions:
                print(f"{func_name} is not in functions set")
                continue
            fact = 'CONTRACT,' + contract_name + ',HASFUNCTION,' + func_name
            if fact not in sentence_facts:
                sentence_facts.append(fact)
            # add HasFn/2 fact
            sentence_facts_dl.add(HasFnFact(contract_name, func_name))
    return sentence_facts, sentence_facts_dl


def extractHASPARAMFacts(lib, version, sentence, ct, fn) -> (List[str], Set[HasParamFact]):
    _, all_functions, all_params = getAllContractsAndFunctionsAndParams(lib, version)
    dl_facts = set()
    sentence_facts = list()
    words = [word.strip('.').strip(',') for word in sentence.strip().split()]
    keywords = []
    for i in range(len(words)):
        if words[i][0] == words[i][-1] == '`':  # T30
            if i > 0 and words[i - 1] == "member":  # member var of class, not param
                continue
            keywords.append(words[i].strip('`'))
    for kw in keywords:
        # print(kw)
        if kw not in all_params:
            continue
        fact = 'FUNCTION,PLACEHOLDER,HASPARAM,' + kw
        dl_facts.add(HasParamFact(ct, fn, kw))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractCALLFacts(lib, version, sentence, contract_fqn, func_name) -> (List[str], Set[CallFact]):
    _, all_functions, all_params = getAllContractsAndFunctionsAndParams(lib, version)
    sentence_facts = []
    dl_facts: Set[CallFact] = set()
    if ' call the ' in sentence and ' function' in sentence.split(' call the ')[-1]:  # T32
        callee_name = \
        sentence.strip().split(' call the ')[-1].split('function')[0].split('{')[-1].split('}')[0]
        callee_name = callee_name.strip().replace('`', '')
        fact = 'FUNCTION,PLACEHOLDER,CALL,' + callee_name
        callee_contract = contract_fqn
        callee_fn = callee_name
        if "." in callee_name:
            callee_contract = callee_name.split(".")[0]
            callee_fn = callee_name.split(".")[1]
        dl_facts.add(CallFact(contract_fqn, func_name, SouffleList([]), callee_contract, callee_fn,
                              SouffleList([])))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractUSEMODIFIERFacts(lib, version, sentence, contract_fqn, func_name) -> (
        List[str], Set[FnModFact]):
    _, all_functions, all_params = getAllContractsAndFunctionsAndParams(lib, version)
    dl_facts = set()
    sentence_facts = []
    if ' guaranteed by the ' in sentence and 'modifier' in sentence.split(' guaranteed by the ')[
        -1]:  # T25
        modifier_name = sentence.strip().split(' guaranteed by the ')[-1].split('modifier')[0]
        modifier_name = modifier_name.strip().replace('`', '')
        fact = 'FUNCTION,PLACEHOLDER,USEMODIFIER,' + modifier_name
        dl_facts.add(FnModFact(contract_fqn, func_name, modifier_name))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractHASSTATEVARIABLEFacts(lib, version, sentence, next_sentence, contract_fqn) -> (
List[str], Set[StateVarFact]):
    _, all_functions, all_params = getAllContractsAndFunctionsAndParams(lib, version)
    sentence_facts = []
    dl_facts = set()
    if ' Declare a' in sentence and 'state variable' in sentence.split(' Declare a')[-1]:  # T31
        state_var_name = next_sentence.strip().split()[-1].replace(';', '').strip()
        fact = 'CONTRACT,' + contract_fqn + ',HASSTATEVARIABLE,' + state_var_name
        dl_facts.add(StateVarFact(contract_fqn, state_var_name))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractContractHASMODIFIERFacts(lib, version, sentences, contract_fqn) -> (List[str], Set[CtModFact]):
    _, all_functions, all_params = getAllContractsAndFunctionsAndParams(lib, version)
    sentence_facts = []
    dl_facts = set()
    for i in range(len(sentences)):
        if ' @dev Modifier ' in sentences[i]:  # T27
            for j in range(i+1, len(sentences)):
                if ' modifier ' in sentences[j]:
                    modifier_name = sentences[j].strip().split('modifier ')[-1].split('(')[0]
                    fact = 'CONTRACT,' + contract_fqn + ',HASMODIFIER,' + modifier_name
                    dl_facts.add(CtModFact(contract_fqn, modifier_name))
                    if fact not in sentence_facts:
                        sentence_facts.append(fact)
    return sentence_facts, dl_facts


def getAllContractsAndFunctionsAndParams(lib, version):
    all_contracts, all_functions, all_params = [], [], []
    function_params_info_json = CODE_FACTS_OUTPUT_DIR + '/' + lib + '/' + version + '/contracts.json'
    with open(function_params_info_json, 'r') as fr:
        function_params_info = json.load(fr, object_pairs_hook=collections.OrderedDict)
    for fqn in function_params_info:
        contract_name = fqn.split('.')[0]
        function_name = fqn.split('.')[-1]
        if contract_name not in all_contracts:
            all_contracts.append(contract_name)
        if function_name not in all_functions:
            all_functions.append(function_name)
        for param in function_params_info[fqn]:
            if param not in all_params:
                all_params.append(param)
    return all_contracts, all_functions, all_params
