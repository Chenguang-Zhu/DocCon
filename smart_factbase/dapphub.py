from typing import Set, List, Optional

from datalog.dlexpr import Expr, Bool
from datalog.pred import HasFnFact, RequireFact, EmitFact, OverrideFact, FnModFact


def extractContractContainFacts_DappHub(lib, version, src_file, doc_facts) \
        -> (List[str], Set[HasFnFact]):
    dl_has_fn_set: Set[HasFnFact] = set()
    with open(src_file, 'r') as fr:
        lines = fr.readlines()
    for i in range(len(lines)):
        contract_fqn = None
        if lines[i].strip().startswith('<h2>'):
            contract_fqn = lines[i].strip().split('<h2>')[-1]
        if lines[i].strip().startswith('#### `'):
            func_name = lines[i].strip().split('`')[1].split('(')[0]
            if contract_fqn:
                dl_has_fn_set.add(HasFnFact(contract_fqn, func_name))
            contract_fact = 'CONTRACT,' + contract_fqn + ',HASFUNCTION,' + func_name
            if contract_fact not in doc_facts:
                doc_facts.append(contract_fact)
    return doc_facts, dl_has_fn_set


def extractDocFactsFromOneFunc_DappHub(lib, version, lines, contract_fqn, func_name, doc_facts) -> (List[str], Set[RequireFact], Set[EmitFact], Set[OverrideFact], Set[FnModFact]):
    dl_require_set: Set[RequireFact] = set()
    dl_emit_set: Set[EmitFact] = set()
    dl_override_set: Set[OverrideFact] = set()
    dl_fn_mod_set: Set[FnModFact] = set()
    func_facts = []
    for i in range(len(lines)):
        if 'requires ' in lines[i]:
            require_fact, dl_require, dl_fn_mod = extractRequireFacts(lib, version, lines[i], contract_fqn, func_name)
            func_facts += require_fact
            if dl_require:
                dl_require_set.add(dl_require)
            if dl_fn_mod:
                dl_fn_mod_set.add(dl_fn_mod)
        if 'Fires a ' in lines[i] and 'event' in lines[i]:  # T5
            emit_fact, dl_emit = extractEmitFacts(lib, version, lines[i], contract_fqn, func_name)
            func_facts += emit_fact
            dl_emit_set.add(dl_emit)
        if 'Overridden from ' in lines[i]:  # T34
            override_fact, dl_override = extractOverrideFacts(lib, version, lines[i], contract_fqn, func_name)
            func_facts += override_fact
            dl_override_set.add(dl_override)
    for fact in func_facts:
        if fact not in doc_facts:
            doc_facts.append(fact)
    return doc_facts, dl_require_set, dl_emit_set, dl_override_set, dl_fn_mod_set


def extractRequireFacts(lib, version, sentence, contract_fqn, func_name) \
        -> (List[str], Optional[RequireFact], Optional[FnModFact]):
    sentence_facts = []
    right = sentence.split('requires ')[-1].split(')')[0]
    right = right.replace('`', '')
    if ' ' in right:
        right = right.replace(' ', '_')
    right = right.rstrip('\n')
    dl_fn_has_mod = None
    dl_require = None
    if right == 'auth':  # T33
        fact = 'FUNCTION,' + contract_fqn + '.' + func_name + ',HASMODIFER,' + right
        dl_fn_has_mod: Optional[FnModFact] = FnModFact(contract_fqn, func_name, right)
    else:  # T18
        fact = 'FUNCTION,' + contract_fqn + '.' + func_name + ',REQUIRE,' + right
        dl_require: Optional[RequireFact] = RequireFact(contract_fqn, func_name, Expr(right))
    if fact not in sentence_facts:
        sentence_facts.append(fact)
    return sentence_facts, dl_require, dl_fn_has_mod


def extractEmitFacts(lib, version, sentence, contract_fqn, func_name) \
        -> (List[str], EmitFact):
    sentence_facts = []
    right = sentence.split('Fires a ')[-1].split(' event')[0]
    right = right.strip().strip('.').strip(',')
    right = right.replace('`', '')
    if ' ' in right:
        right = right.replace(' ', '_')
    fact = 'FUNCTION,' + contract_fqn + '.' + func_name + ',EMIT,' + right
    if fact not in sentence_facts:
        sentence_facts.append(fact)
    dl_emit: EmitFact = EmitFact(contract_fqn, func_name, right, Bool(True))
    return sentence_facts, dl_emit


def extractOverrideFacts(lib, version, sentence, contract_fqn, func_name):
    sentence_facts = []
    right = sentence.split('Overridden from ')[-1]
    right = right.strip().strip('.').strip(',')
    right = right.replace('`', '')
    if ' ' in right:
        right = right.replace(' ', '_')
    right_full = right + '.' + func_name
    fact = 'FUNCTION,' + contract_fqn + '.' + func_name + ',OVERRIDE,' + right_full
    if fact not in sentence_facts:
        sentence_facts.append(fact)
    dl_override: OverrideFact = OverrideFact(right, func_name, contract_fqn, func_name)
    return sentence_facts, dl_override
