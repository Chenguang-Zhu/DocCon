
def fuzzyMatch(doc_fact, all_code_facts):
    for code_fact in all_code_facts:
        if doc_fact == code_fact:
            return True
        if fuzzyMatchOneFact(doc_fact, code_fact):
            return True
    return False

def fuzzyMatchOneFact(doc_fact, code_fact):
    #if len(doc_fact.split(',')) != len(code_fact.split(',')):
    #    return False
    if doc_fact.split(',')[2] == 'EMITIF' and code_fact.split(',')[2] == 'EMIT':
        if doc_fact.split(',')[:2] == code_fact.split(',')[:2] and doc_fact.split(',')[-1] == code_fact.split(',')[-1]:
            return True
    if doc_fact.split(',')[:3] != code_fact.split(',')[:3]:
        # function name require
        return False
    if doc_fact.split(',')[2] == 'REQUIRE':
        if len(doc_fact.split(',')) >= 4 and doc_fact.split(',')[3] in ['LT', 'LEQ', 'GT', 'GEQ', 'EQ', 'NEQ']:
            if doc_fact.split(',')[3] != code_fact.split(',')[3]:
                # op not same
                return False
            doc_left_expr = doc_fact.split(',')[4]
            code_left_expr = code_fact.split(',')[4]
            doc_right_expr = doc_fact.split(',')[5]
            code_right_expr = code_fact.split(',')[5]
            if fuzzyMatchExpr(doc_left_expr, code_left_expr) and fuzzyMatchExpr(doc_right_expr, code_right_expr):
                return True
            if doc_fact.split(',')[3] in ['EQ', 'NEQ']:
                if fuzzyMatchExpr(doc_left_expr, code_right_expr) and fuzzyMatchExpr(doc_right_expr, code_left_expr):
                    return True
        else:
            # require single expr
            doc_expr = doc_fact.split(',')[3]
            code_expr = code_fact.split(',')[3]
            if fuzzyMatchExpr(doc_expr, code_expr):
                return True
    return False

def fuzzyMatchExpr(doc_expr, code_expr):
    if doc_expr == code_expr:
        return True
    if doc_expr.lower() == code_expr.lower():
        return True
    if doc_expr.endswith('_balance'):
        if doc_expr.split('_')[0] + doc_expr.split('_')[-1].title() == code_expr:  # code in camel case
            # xxx_balance -> xxxBalance
            return True
    if doc_expr == 'the caller':  # ERC1155
        if code_expr == 'owner':
            return True
    if '(' in doc_expr and ')' in doc_expr:
        # function call, check function name
        return fuzzyMatchExpr(doc_expr.split('(')[0], code_expr.split('(')[0])
    return False
