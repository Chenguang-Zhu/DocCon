from typing import List, Optional

from condition import parseConditionSentence
from datalog.dlexpr import Expr
from datalog.pred import RevertFact


def extractREVERTIFFacts(sentence, ct, fn) -> (List[str], RevertFact):
    sentence_facts = []
    message_func_name = sentence.split('Reverts with ')[-1].split(' if')[0]
    message_func_name = message_func_name.replace('`', '')
    condition_sentence = sentence.split(' if ')[-1].strip().strip(',').strip('.')
    condition = parseConditionSentence(condition_sentence)
    fact = 'FUNCTION,PLACEHOLDER,REVERTIF,' + condition
    dl_fact = RevertFact(ct, fn, Expr(condition))
    if fact not in sentence_facts:
        sentence_facts.append(fact)
    # print(sentence_facts)
    return sentence_facts, dl_fact
