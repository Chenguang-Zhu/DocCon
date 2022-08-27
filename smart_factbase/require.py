from typing import Set, List

from datalog.dlexpr import Cmp, BinOp, Expr, NegExpr
from datalog.pred import RequireFact


def extractREQEQFacts(sentence, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    sentence_facts = []
    dl_facts: Set[RequireFact] = set()
    operator = 'EQ'
    if ' must be owned by ' in sentence:  # T11
        right = sentence.split('must be owned by')[-1].strip().strip(',').strip('.')
        right = right.replace('`', '')
        left = sentence.split('- ')[-1].split('must be owned by')[0].strip().strip(',').strip('.')
        left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
        for lv in left_vars:
            lv = lv.replace('`', '')
            lv = 'ownerOf(' + lv + ')'
            dl_facts.add(RequireFact(contract_fqn, func_name, Cmp(BinOp.EQ, Expr(lv), Expr(right))))
            fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + operator + ',' + lv + ',' + right
            if fact not in sentence_facts:
                sentence_facts.append(fact)
    elif ' must have the same length' in sentence:  # T10
        right = sentence.split(' and ')[-1].split('must have the same length')[0].strip().strip(',').strip('.')
        right = right.replace('`', '') + ".length"
        left = sentence.split('- ')[-1].split(' and ')[0].strip().strip(',').strip('.')
        left = left.replace('`', '') + ".length"
        fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + operator + ',' + left + ',' + right
        dl_facts.add(RequireFact(contract_fqn, func_name, Cmp(BinOp.EQ, Expr(left), Expr(right))))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractREQNEQFacts(sentence, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    sentence_facts = []
    dl_facts: Set[RequireFact] = set()
    operator = 'NEQ'
    if ' cannot be ' in sentence:  # T9
        right = sentence.split('cannot be')[-1].strip().strip(',').strip('.')
        if '`' in right:
            right = right.split('`')[1]
        if right == 'the zero address':  # T12
            right = 'address(0)'
        if right == 'zero':
            right = '0'
        left = sentence.split('- ')[-1].split('cannot be')[0].strip().strip(',').strip('.')
        left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
        if not left_vars:
            left_vars = [left.split()[-1]]
        for lv in left_vars:
            lv = lv.replace('`', '')
            dl_facts.add(RequireFact(contract_fqn, func_name, Cmp(BinOp.NEQ, Expr(lv), Expr(right))))
            fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + operator + ',' + lv + ',' + right
            if fact not in sentence_facts:
                sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractREQLEQFacts(sentence, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    sentence_facts = []
    dl_facts: Set[RequireFact] = set()
    operator = 'LEQ'
    right = ""
    if 'at most ' in sentence:  # T8
        right = sentence.split(' at most ')[-1].strip().strip(',').strip('.')
        for word in right.split():
            if word[0] == word[-1] == '`':
                right = word
                break
        right = right.replace('`', '')
    elif ' cannot be greater than ' in sentence:  # T7
        right = sentence.split('cannot be greater than')[-1].strip().strip(',').strip('.')
        right = right.replace('`', '')
    if right == 'the fee denominator':
        right = '_feeDenominator()'
    left = sentence.split('- ')[-1].split('cannot be greater than')[0].strip().strip(',').strip('.')
    left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
    if right:
        for lv in left_vars:
            lv = lv.replace('`', '')
            dl_facts.add(RequireFact(contract_fqn, func_name, Cmp(BinOp.LEQ, Expr(lv), Expr(right))))
            fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + operator + ',' + lv + ',' + right
            if fact not in sentence_facts:
                sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractREQGEQFacts(sentence, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    sentence_facts = []
    dl_facts: Set[RequireFact] = set()
    operator = 'GEQ'
    if 'at least ' in sentence:  # T8
        right = sentence.split(' at least ')[-1].strip().strip(',').strip('.')
        for word in right.split():
            if word[0] == word[-1] == '`':
                right = word
                break
        right = right.replace('`', '')
    elif ' cannot be less than' in sentence:  # T7
        right = sentence.split(' cannot be less than ')[-1].strip().strip(',').strip('.')
        for word in right.split():
            if word[0] == word[-1] == '`':
                right = word
                break
        right = right.replace('`', '')
    left = sentence.split('- ')[-1].split(' at least')[0].strip().strip(',').strip('.')
    left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
    for lv in left_vars:
        lv = lv.replace('`', '')
        if 'have a balance of' in left:  # T13
            if '`' + lv + '`' not in left.split('have a balance of')[0]:
                continue
            lv += '_balance'
        elif 'have allowance for' in left:  # T14
            lv += '_allowance'
        elif 'tokens.' == sentence.strip().split()[-1]:
            lv = lv + 'Balance'
        dl_facts.add(RequireFact(contract_fqn, func_name, Cmp(BinOp.GEQ, Expr(lv), Expr(right))))
        fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + operator + ',' + lv + ',' + right
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractREQLTFacts(sentence, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    sentence_facts = []
    dl_facts: Set[RequireFact] = set()
    operator = 'LT'
    right = sentence.split('must be strictly less than')[-1].strip().strip(',').strip('.')  # T6
    right = right.replace('`', '')
    left = sentence.split('- ')[-1].split('must be strictly less than')[0].strip().strip(',').strip('.')
    left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
    for lv in left_vars:
        lv = lv.replace('`', '')
        fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + operator + ',' + lv + ',' + right
        dl_facts.add(RequireFact(contract_fqn, func_name, Cmp(BinOp.LT, Expr(lv), Expr(right))))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractREQGTFacts(sentence, contract_fqn, func_name) -> (List[str], Set[RequireFact]):
    sentence_facts = []
    dl_facts: Set[RequireFact] = set()
    operator = 'GT'
    right = sentence.split('must be strictly greater than')[-1].strip().strip(',').strip('.')  # T6
    right = right.replace('`', '')
    left = sentence.split('- ')[-1].split('must be strictly greater than')[0].strip().strip(',').strip('.')
    left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
    for lv in left_vars:
        lv = lv.replace('`', '')
        fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + operator + ',' + lv + ',' + right
        dl_facts.add(RequireFact(contract_fqn, func_name, Cmp(BinOp.GT, Expr(lv), Expr(right))))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts


def extractREQFacts(sentence, contract_fqn, func_name)-> (List[str], Set[RequireFact]):
    sentence_facts = []
    dl_facts: Set[RequireFact] = set()
    if ' must be already minted' in sentence:  # T15
        left = sentence.split('- ')[-1].split('must be already minted')[0].strip().strip(',').strip('.')
        left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
        for lv in left_vars:
            lv = lv.replace('`', '')
            lv = '_minted(' + lv + ')'
            dl_facts.add(RequireFact(contract_fqn, func_name, Expr(lv)))
            fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + lv
            if fact not in sentence_facts:
                sentence_facts.append(fact)
    if ' must exist' in sentence:  # T16
        left = sentence.split('- ')[-1].split('must exist')[0].strip().strip(',').strip('.')
        left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
        for lv in left_vars:
            lv = lv.replace('`', '')
            lv = '_exists(' + lv + ')'
            dl_facts.add(RequireFact(contract_fqn, func_name, Expr(lv)))
            fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + lv
            if fact not in sentence_facts:
                sentence_facts.append(fact)
    if ' must not exist' in sentence:  # T17
        left = sentence.split('- ')[-1].split('must not exist')[0].strip().strip(',').strip('.')
        left_vars = ([word for word in left.split() if word[0] == word[-1] == '`'])
        for lv in left_vars:
            lv = lv.replace('`', '')
            dl_facts.add(RequireFact(contract_fqn, func_name, NegExpr(Expr(f"_exists({lv})"))))
            lv = '!_exists(' + lv + ')'
            fact = 'FUNCTION,PLACEHOLDER,REQUIRE,' + lv
            if fact not in sentence_facts:
                sentence_facts.append(fact)
    if ' the contract must not be paused' in sentence:  # T36
        fact = 'FUNCTION,PLACEHOLDER,REQUIRE,!paused()'
        dl_facts.add(RequireFact(contract_fqn, func_name, NegExpr(Expr(f"paused()"))))
        if fact not in sentence_facts:
            sentence_facts.append(fact)
    return sentence_facts, dl_facts
