import collections
import json
import os

from macros import DOC_FACTS_OUTPUT_DIR


def isCommentLine(line):
    return True if line.strip().startswith('*') else False


def findFQNInDoc(line):
    for word in line.strip().split():
        if '.' in word:
            if 'since v' in line:
                return False
            if 'i.e.' in word:
                return False
            if 'e.g.' in word:
                return False
            if '5.05' in word:
                return False
            if 'https:' in line or 'xref:' in line:
                return False
            return True
    return False


def isSeeDoc(lines):
    if lines[1].strip().startswith('* @dev See {'):  # T37
        return True
    return False


def getLoadTarget(lines, current_contract_fqn) -> (str, str):
    """
    Get "@dev See" target.
    E.g., "@dev See {IERC165-supportsInterface}" will return
        (IERC165, supportsInterface)
    :param lines: The docstring lines
    :param current_contract_fqn: the contract which contains the docstring
    :return: a 2-tuple, (the target contract name, target func name)
    """
    if '-' in lines[1].strip().split('{')[-1].split('}')[0]:
        load_contract_fqn = lines[1].strip().split('{')[-1].split('}')[0].split('-')[0]
    else:
        load_contract_fqn = current_contract_fqn
    load_func_name = lines[1].strip().split('{')[-1].split('}')[0].split('-')[-1]
    return load_contract_fqn, load_func_name


def loadFacts(lib, version, load_contract_fqn, load_func_name, current_contract_fqn,
              current_func_name):
    func_facts = []
    contract_facts_file = DOC_FACTS_OUTPUT_DIR + '/' + lib + '/' + version + '/' + load_contract_fqn + '.json'
    if not os.path.isfile(contract_facts_file):
        return func_facts
    with open(contract_facts_file, 'r') as fr:
        contract_facts = json.load(fr, object_pairs_hook=collections.OrderedDict)
    for f in contract_facts:
        if f.split(',')[0] == 'FUNCTION' and f.split(',')[
            1] == load_contract_fqn + '.' + load_func_name:
            func_facts.append(f.replace(load_contract_fqn + '.' + load_func_name,
                                        current_contract_fqn + '.' + current_func_name))
    return func_facts
