from typing import Set, List

from datalog.dlexpr import Bool, Expr
from datalog.pred import EmitFact


def extractEMITFacts(sentence, ct, fn) -> (List[str], Set[EmitFact]):
    sentence_facts = []
    dl_facts: Set[EmitFact] = set()
    if 'Emits a ' in sentence:  # T1
        event_fqn = sentence.split('Emits a ')[-1].split(' event')[0].strip('{').strip('}').replace(
            '-', '.')
        if '.' in event_fqn:
            event_fqn = event_fqn.split('.')[-1]
        fact = 'FUNCTION,PLACEHOLDER,EMIT,' + event_fqn
        sentence_facts.append(fact)
        dl_facts.add(EmitFact(ct, fn, event_fqn, Bool(True)))
    elif 'Emits an ' in sentence:  # T1
        event_fqn = sentence.split('Emits an ')[-1].split(' event')[0].strip('{').strip(
            '}').replace('-', '.')
        if '.' in event_fqn:
            event_fqn = event_fqn.split('.')[-1]
        fact = 'FUNCTION,PLACEHOLDER,EMIT,' + event_fqn
        sentence_facts.append(fact)
        dl_facts.add(EmitFact(ct, fn, event_fqn, Bool(True)))
    elif 'emits a' in sentence:  # T2
        event_fqn = sentence.split('emits a ')[-1].split(' event')[0].strip('{').strip('}').replace(
            '-', '.')
        if '.' in event_fqn:
            event_fqn = event_fqn.split('.')[-1]
        fact = 'FUNCTION,PLACEHOLDER,EMIT,' + event_fqn
        sentence_facts.append(fact)
        dl_facts.add(EmitFact(ct, fn, event_fqn, Bool(True)))
    elif 'emits an' in sentence:  # T2
        event_fqn = sentence.split('emits an ')[-1].split(' event')[0].strip('{').strip('}').replace('-', '.')
        if '.' in event_fqn:
            event_fqn = event_fqn.split('.')[-1]
        fact = 'FUNCTION,PLACEHOLDER,EMIT,' + event_fqn
        sentence_facts.append(fact)
        dl_facts.add(EmitFact(ct, fn, event_fqn, Bool(True)))
    elif 'Emits ' in sentence and ' and ' in sentence and 'events' in sentence:  # T3
        words = [word.strip().strip('.').strip(',') for word in sentence.split()]
        event_fqns = [word[1:-1].replace('-', '.') for word in words if
                      word[0] == '{' and word[-1] == '}']
        for event_fqn in event_fqns:
            if '.' in event_fqn:
                event_fqn = event_fqn.split('.')[-1]
            fact = 'FUNCTION,PLACEHOLDER,EMIT,' + event_fqn
            sentence_facts.append(fact)
            dl_facts.add(EmitFact(ct, fn, event_fqn, Bool(True)))
    return sentence_facts, dl_facts


def extractEMITIFFacts(sentence, ct, fn) -> (List[str], Set[EmitFact]):
    sentence_facts = []
    dl_facts: Set[EmitFact] = set()
    if 'Might emit a ' in sentence:  # T4
        event_fqn = sentence.split('Might emit a ')[-1].split(' event')[0].strip('{').strip(
            '}').replace('-', '.')
    elif 'Might emit an ' in sentence:  # T4
        event_fqn = sentence.split('Might emit an ')[-1].split(' event')[0].strip('{').strip(
            '}').replace('-', '.')
    if '.' in event_fqn:
        event_fqn = event_fqn.split('.')[-1]
    fact = 'FUNCTION,PLACEHOLDER,EMITIF,' + event_fqn
    dl_facts.add(EmitFact(ct, fn, event_fqn, Expr("")))
    sentence_facts.append(fact)
    return sentence_facts, dl_facts
