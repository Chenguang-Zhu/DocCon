from typing import Set, List, Optional

from contain import extractHASFUNCTIONFacts
from contain import getAllContractsAndFunctionsAndParams
from datalog.pred import HasFnFact, HasParamFact, OverrideFact, FnModFact, RequireFact, EmitFact, \
    RevertFact, InheritFact
from openzeppelin import extractRequireFacts, extractEmitFacts, extractRevertFacts
from util import findFQNInDoc


def extractDocFactsFromOneFunc_ERC721(lib, version, lines, contract_fqn, func_name, doc_facts) \
        -> (List[str], Set[FnModFact], Set[RequireFact], Set[EmitFact],
            Set[RevertFact], Set[HasParamFact], Set[OverrideFact]):
    # extract facts
    func_facts = []
    # solidity
    func_facts, fn_mod_facts = extractModifierFacts(lines, func_facts, contract_fqn, func_name)
    func_facts, inherit_facts = extractInheritFacts(lines, func_facts, contract_fqn)
    func_facts, require_facts = extractRequireFacts(lines, func_facts, contract_fqn, func_name)
    func_facts, emit_facts, = extractEmitFacts(lines, func_facts, contract_fqn, func_name)
    func_facts, revert_facts = extractRevertFacts(lines, func_facts, contract_fqn, func_name)
    func_facts, has_param_facts, override_facts = extractFunctionContainFacts(lib, version, lines,
                                                                              func_facts,
                                                                              contract_fqn,
                                                                              func_name)
    func_facts = [fact.replace(',PLACEHOLDER,', ',' + contract_fqn + '.' + func_name + ',')
                  for fact in func_facts]
    func_facts = [fact.replace(',CONT_PLACEHOLDER,', ',' + contract_fqn + ',') for fact in func_facts]
    for fact in func_facts:
        if fact not in doc_facts:
            doc_facts.append(fact)
    return doc_facts, fn_mod_facts, require_facts, emit_facts, revert_facts, has_param_facts, override_facts, inherit_facts


def extractContractContainFacts_ERC721(lib, version, src_file, doc_facts: List[str]) -> (
        List[str], List[HasFnFact]):
    with open(src_file, 'r') as fr:
        lines = fr.readlines()
    contract_facts = []
    contract_facts_dl: Set[HasFnFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('///'):
            if findFQNInDoc(lines[i]):
                sentence_facts, sentence_facts_dl = extractHASFUNCTIONFacts(lib, version, lines[i])
                contract_facts += sentence_facts
                contract_facts_dl = contract_facts_dl.union(sentence_facts_dl)
    for fact in contract_facts:
        if fact not in doc_facts:
            doc_facts.append(fact)
    return doc_facts, contract_facts_dl


def extractModifierFacts(lines, func_facts, ct, fn) -> (List[str], Set[FnModFact]):
    dl_fn_has_mod_set: Set[FnModFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('/// Only allow ') and ' if ' in lines[i]:
            sentence_facts, dl_fn_had_mod = extractUSEMODIFIERFacts(lines[i], ct, fn)
            func_facts += sentence_facts
            if dl_fn_had_mod:
                dl_fn_has_mod_set.add(dl_fn_had_mod)
    return func_facts, dl_fn_has_mod_set


def extractInheritFacts(lines, func_facts, contract_fqn) -> (List[str], Set[InheritFact]):
    dl_inherit_set: Set[InheritFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('/// Implement the ') and ' Contract' in lines[i]:  # T35
            parent_contract = lines[i].strip().split(' Implement the ')[-1].split(' Contract')[
                0].replace('`', '').strip()
            fact = 'CONTRACT,CONT_PLACEHOLDER,IS,' + parent_contract
            dl_inherit_set.add(InheritFact(parent_contract, contract_fqn))
            if fact not in func_facts:
                func_facts.append(fact)
    return func_facts, dl_inherit_set


def extractFunctionContainFacts(lib, version, lines, func_facts, contract_fqn, fn_name) \
        -> (List[str], Set[HasParamFact], Set[OverrideFact]):
    dl_has_param_set: Set[HasParamFact] = set()
    dl_override_set: Set[OverrideFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('/// @param '):
            sentence_facts, dl_has_param = extractHASPARAMFacts(lib, version, lines[i],
                                                                contract_fqn, fn_name)
            func_facts += sentence_facts
            if dl_has_param:
                dl_has_param_set.add(dl_has_param)
        if lines[i].strip().startswith('/// Implement ') and lines[i].strip().endswith('Contract'):
            sentence_facts, dl_override = extractOverrideFacts(lib, version, lines[i], contract_fqn,
                                                               fn_name)
            func_facts += sentence_facts
            if dl_override:
                dl_override_set.add(dl_override)
                print(dl_override_set)
    return func_facts, dl_has_param_set, dl_override_set


def extractUSEMODIFIERFacts(sentence, ct, fn) -> (List[str], Optional[FnModFact]):
    sentence_facts = []
    if 'Only allow ' in sentence:
        modifier_name = sentence.strip().split(' if ')[-1]
        if 'if within the allowed' in sentence:  # T26
            modifier_name = 'within' + ''.join(sentence.strip().split(' the allowed ')[-1].split())
    fact = 'FUNCTION,PLACEHOLDER,USEMODIFIER,' + modifier_name
    sentence_facts.append(fact)
    fn_mod_fact = None if modifier_name is None else FnModFact(ct, fn, modifier_name)
    return sentence_facts, fn_mod_fact


def extractHASPARAMFacts(lib, version, sentence, contract_fqn, fn_name) \
        -> (List[str], Optional[HasParamFact]):
    """
    Extract HasParam facts
    Returns:
        A tuple, .0 is a list of str, facts in original format;
        .1 is a HasParamFact or None
    """
    _, all_functions, all_params = getAllContractsAndFunctionsAndParams(lib, version)
    sentence_facts = []
    kw = sentence.split('/// @param ')[-1].strip().split()[0]  # T29
    if kw not in all_params:
        return sentence_facts, None
    fact = 'FUNCTION,PLACEHOLDER,HASPARAM,' + kw
    if fact not in sentence_facts:
        sentence_facts.append(fact)
    return sentence_facts, HasParamFact(contract_fqn, fn_name, kw)


def extractOverrideFacts(lib, version, sentence, contract_fqn, func_name) \
        -> (List[str], OverrideFact):
    _, all_functions, all_params = getAllContractsAndFunctionsAndParams(lib, version)
    sentence_facts = []
    parent_contract_name = sentence.split('`')[1]
    fact = 'FUNCTION,PLACEHOLDER,OVERRIDE,' + parent_contract_name + '.' + func_name
    print(f"find override {func_name}")
    if fact not in sentence_facts:
        sentence_facts.append(fact)
    return sentence_facts, OverrideFact(parent_contract_name, func_name, contract_fqn, func_name)
