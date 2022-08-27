import collections
import json
import os
from typing import Set, List

from contain import extractHASFUNCTIONFacts, extractHASSTATEVARIABLEFacts, extractCALLFacts, \
    extractContractHASMODIFIERFacts
from contain import extractHASPARAMFacts
from contain import extractUSEMODIFIERFacts
from datalog.pred import SeeFnFact, HasFnFact, RequireFact, EmitFact, RevertFact, HasParamFact, \
    FnModFact, StateVarFact, CallFact, CtModFact
from event import extractEMITFacts
from event import extractEMITIFFacts
from macros import DOC_FACTS_OUTPUT_DIR
from require import extractREQEQFacts
from require import extractREQFacts
from require import extractREQGEQFacts
from require import extractREQGTFacts
from require import extractREQLEQFacts
from require import extractREQLTFacts
from require import extractREQNEQFacts
from revert import extractREVERTIFFacts
from util import findFQNInDoc
from util import getLoadTarget
from util import isSeeDoc
from util import loadFacts


def extractDocFactsFromOneFunc_OpenZeppelin(lib, version, lines, contract_fqn, func_name,
                                            doc_facts: List[str]) -> (
List[str], Set[SeeFnFact], Set[RequireFact], Set[EmitFact], Set[RevertFact], Set[HasParamFact], Set[FnModFact], Set[CallFact]):
    see_fn: Set[SeeFnFact] = set()
    if isSeeDoc(lines):
        # load target facts
        load_contract_fqn, load_func_name = getLoadTarget(lines, contract_fqn)
        # generate SeeFn/2 facts
        see_fn.add((SeeFnFact(contract_fqn, func_name, load_contract_fqn, load_func_name)))
        func_facts = loadFacts(lib, version, load_contract_fqn, load_func_name, contract_fqn,
                               func_name)
        for fact in func_facts:
            if fact not in doc_facts:
                doc_facts.append(fact)
    # extract facts
    func_facts: List[str] = []
    # solidity
    func_facts, require_facts = extractRequireFacts(lines, func_facts, contract_fqn, func_name)

    func_facts, emit_facts = extractEmitFacts(lines, func_facts, contract_fqn, func_name)
    func_facts, revert_facts = extractRevertFacts(lines, func_facts, contract_fqn, func_name)
    func_facts, has_param_facts, use_mod_facts, call_facts = extractFunctionContainFacts(lib, version, lines, func_facts,
                                                              contract_fqn, func_name)
    func_facts = [fact.replace(',PLACEHOLDER,', ',' + contract_fqn + '.' + func_name + ',') for fact
                  in func_facts]
    for fact in func_facts:
        if fact not in doc_facts:
            doc_facts.append(fact)
    return doc_facts, see_fn, require_facts, emit_facts, revert_facts, has_param_facts, use_mod_facts, call_facts


# --- Solidity Program Facts ---

def extractRequireFacts(lines, func_facts, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    dl_fact_req = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('* Requirements:'):
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == '*/':
                    break
                if lines[j].strip().startswith('* -'):
                    sentence = lines[j].strip()
                    k = j + 1
                    while not lines[k].strip().startswith('* -') and not lines[
                        k].strip().startswith('*/') and not lines[k].strip() == '*':
                        sentence += ' ' + lines[k].strip()[2:]
                        k += 1
                    if 'must be strictly less than' in sentence:  # template T5
                        sentence_facts, req_fact_dl = extractREQLTFacts(sentence, contract_fqn,
                                                                        func_name)
                        func_facts += sentence_facts
                    elif 'must be strictly greater than' in sentence:  # T6
                        sentence_facts, req_fact_dl = extractREQGTFacts(sentence, contract_fqn,
                                                                        func_name)
                        func_facts += sentence_facts
                    elif 'cannot be greater than ' in sentence:  # T7
                        sentence_facts, req_fact_dl = extractREQLEQFacts(sentence, contract_fqn,
                                                                         func_name)
                        func_facts += sentence_facts
                    elif 'cannot be less than ' in sentence:  # T7
                        sentence_facts, req_fact_dl = extractREQGEQFacts(sentence, contract_fqn,
                                                                         func_name)
                        func_facts += sentence_facts
                    elif ' must ' in sentence and 'at least' in sentence:  # T8
                        sentence_facts, req_fact_dl = extractREQGEQFacts(sentence, contract_fqn,
                                                                         func_name)
                        func_facts += sentence_facts
                    elif ' must ' in sentence and 'at most' in sentence:  # T8
                        sentence_facts, req_fact_dl = extractREQLEQFacts(sentence, contract_fqn,
                                                                         func_name)
                        func_facts += sentence_facts
                    elif ' cannot be ' in sentence:  # T9
                        sentence_facts, req_fact_dl = extractREQNEQFacts(sentence, contract_fqn,
                                                                         func_name)
                        func_facts += sentence_facts
                    elif ' must be owned by ' in sentence:  # T11
                        sentence_facts, req_fact_dl = extractREQEQFacts(sentence, contract_fqn,
                                                                        func_name)
                        func_facts += sentence_facts
                    elif ' must have the same length' in sentence:  # T10
                        sentence_facts, req_fact_dl = extractREQEQFacts(sentence, contract_fqn,
                                                                        func_name)
                        func_facts += sentence_facts
                    else:
                        sentence_facts, req_fact_dl = extractREQFacts(sentence, contract_fqn,
                                                                      func_name)
                        func_facts += sentence_facts
                    dl_fact_req = dl_fact_req.union(req_fact_dl)
    return func_facts, dl_fact_req


def extractEmitFacts(lines, func_facts, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    dl_fact_emit = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('/**'):
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == '*/':
                    break
                if lines[j].strip().startswith('* Emits '):
                    sentence_facts, dl_facts = extractEMITFacts(lines[j], contract_fqn, func_name)
                    func_facts += sentence_facts
                    dl_fact_emit = dl_fact_emit.union(dl_facts)
                elif lines[j].strip().startswith('* ') and ' emits a ' in lines[j] and 'event' in \
                        lines[j]:
                    sentence_facts, dl_facts = extractEMITFacts(lines[j], contract_fqn, func_name)
                    func_facts += sentence_facts
                    dl_fact_emit = dl_fact_emit.union(dl_facts)
                elif lines[j].strip().startswith('* Might emit '):
                    sentence_facts, dl_facts = extractEMITIFFacts(lines[j], contract_fqn, func_name)
                    func_facts += sentence_facts
                    dl_fact_emit = dl_fact_emit.union(dl_facts)
    return func_facts, dl_fact_emit


def extractRevertFacts(lines, func_facts, contract_fqn, func_name) -> (List[str], Set[RevertFact]):
    revert_facts: Set[RevertFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('/**'):
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == '*/':
                    break
                if lines[j].strip().startswith('* Reverts '):
                    sentence_facts, dl_fact = extractREVERTIFFacts(lines[j], contract_fqn,
                                                                   func_name)
                    func_facts += sentence_facts
                    revert_facts.add(dl_fact)
    return func_facts, revert_facts


def extractContractContainFacts_OpenZeppelin(lib, version, src_file, doc_facts: List[str], contract_fqn) -> (
List[str], Set[HasFnFact], Set[StateVarFact], Set[CtModFact]):
    with open(src_file, 'r') as fr:
        lines = fr.readlines()
    contract_facts = []
    dl_has_fn_facts = set()
    dl_state_var_facts = set()
    dl_mod_facts = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('* '):
            if findFQNInDoc(lines[i]):
                sentence_facts, contain_fact_dl = extractHASFUNCTIONFacts(lib, version, lines[i])
                contract_facts += sentence_facts
                dl_has_fn_facts = dl_has_fn_facts.union(contain_fact_dl)
            if i + 1 < len(lines):
                sentence_facts, state_var_dl = extractHASSTATEVARIABLEFacts(lib, version, lines[i], lines[i + 1],
                                                              contract_fqn)
                contract_facts += sentence_facts
                dl_state_var_facts = dl_state_var_facts.union(state_var_dl)
            if i + 5 < len(lines):
                sentence_facts, ct_has_mod_dl = extractContractHASMODIFIERFacts(lib, version, lines[i:i+5], contract_fqn)
                contract_facts += sentence_facts
                dl_mod_facts = dl_mod_facts.union(ct_has_mod_dl)

    for fact in contract_facts:
        if fact not in doc_facts:
            doc_facts.append(fact)
    return doc_facts, dl_has_fn_facts, dl_state_var_facts, dl_mod_facts


def extractFunctionContainFacts(lib, version, lines, func_facts, contract_fqn, func_name) -> (List[str], Set[HasParamFact], Set[FnModFact], Set[CallFact]):
    dl_param_facts: Set[HasParamFact] = set()
    dl_fn_mod_facts: Set[FnModFact] = set()
    dl_call_facts: Set[CallFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('/**'):
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == '*/':
                    break
                if lines[j].strip().startswith('* '):
                    sentence_facts, has_param_facts = extractHASPARAMFacts(lib, version, lines[j],
                                                                           contract_fqn, func_name)
                    func_facts += sentence_facts
                    dl_param_facts = dl_param_facts.union(has_param_facts)
                    sentence_facts, use_mod_facts = extractUSEMODIFIERFacts(lib, version, lines[j],
                                                                            contract_fqn, func_name)
                    func_facts += sentence_facts
                    dl_fn_mod_facts = dl_fn_mod_facts.union(use_mod_facts)
                    sentence_facts, call_facts = extractCALLFacts(lib, version, lines[j],
                                                                  contract_fqn, func_name)
                    func_facts += sentence_facts
                    dl_call_facts = dl_call_facts.union(call_facts)

    return func_facts, dl_param_facts, dl_fn_mod_facts, dl_call_facts


def copyOtherFactsToTheirOwnerFiles(lib, version, doc_facts, contract_fqn):
    for fact in doc_facts:
        target_contract_fqn = fact.split(',')[1].split('.')[0]
        if target_contract_fqn != contract_fqn:
            target_fact_file = DOC_FACTS_OUTPUT_DIR + '/' + lib + '/' + version + '/' + target_contract_fqn + '.json'
            if os.path.isfile(target_fact_file):
                with open(target_fact_file, 'r') as fr:
                    target_facts = json.load(fr, object_pairs_hook=collections.OrderedDict)
            else:
                target_facts = []
            if fact not in target_facts:
                target_facts.append(fact)
            with open(target_fact_file, 'w') as fw:
                json.dump(target_facts, fw, indent=2)
