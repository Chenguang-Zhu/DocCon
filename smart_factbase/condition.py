
def parseConditionSentence(sentence):
    res = ''
    if ' is greater than ' in sentence:  # T19
        left_var = sentence.split('is greater than')[0].split()[-1]
        right_var = sentence.split('is greater than')[-1].split()[0]
        res += 'GT,' + left_var + ',' + right_var + ')'
    elif ' is less than ' in sentence:  # T19
        left_var = sentence.split('is less than')[0].split()[-1]
        right_var = sentence.split('is less than')[-1].split()[0]
        res += 'LT,' + left_var + ',' + right_var + ')'
    elif ' is at least ' in sentence:  # T20
        left_var = sentence.split('is at least')[0].split()[-1]
        right_var = sentence.split('is at least')[-1].split()[0]
        res += 'GEQ,' + left_var + ',' + right_var + ')'
    elif ' is at most ' in sentence:  # T20
        left_var = sentence.split('is at most')[0].split()[-1]
        right_var = sentence.split('is at most')[-1].split()[0]
        res += 'LEQ,' + left_var + ',' + right_var + ')'
    elif ' is not ' in sentence:  # T21
        left_var = sentence.split('is not')[0].split()[-1]
        right_var = sentence.split('is not')[-1].split()[0]
        res += 'NEQ,' + left_var + ',' + right_var + ')'
    elif ' is the zero address' in sentence:  # T22
        left_var = sentence.split('is the zero address')[0].split()[-1]
        res += 'EQ,' + left_var + ',address(0))'
    elif ' does not exist' in sentence:  # T23
        left_var = sentence.split('does not exist')[0].split()[-1]
        res += '!exist(' + left_var + '))'
    elif 'is empty' in sentence:  # T24
        var = sentence.split('is empty')[0].split()[-1]
        res += 'empty(' + var + ')'
    else:
        res += sentence.replace(' ', '_')
    return res
