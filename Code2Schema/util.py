from shutil import ReadError
from datalog.dlexpr import Expr, Cmp, NegExpr, BinOp, UnaryOp, BinLogicOp, MathBinOp, BinLogExpr, \
    MathExpr

binOpStrs = {
    BinOp.EQ: "EQ",
    BinOp.GEQ: "GEQ",
    BinOp.GT: "GT",
    BinOp.LEQ: "LEQ",
    BinOp.LT: "LT",
    BinOp.NEQ: "NEQ",
    UnaryOp.NEG: "NOT",
    BinLogicOp.AND: "AND",
    BinLogicOp.OR: "OR",
    MathBinOp.ADD: "ADD",
    MathBinOp.SUB: "SUB",
    MathBinOp.MUL: "MUL",
    MathBinOp.DIV: "DIV"
}
def conds2Expr(conds):
    expr, end_index = translateCondArray2Expr(conds, 0, len(conds))
    assert end_index == len(conds), "invalid conds: "+ ",".join(conds)
    return expr 

def translateCondArray2Expr(conds, i, n):
    if i==n:
        assert False, "out of the bounds of conds"
    if binOpStrs[BinOp.EQ] != conds[i] \
        and binOpStrs[BinOp.GEQ] != conds[i] \
        and binOpStrs[BinOp.GT] != conds[i] \
        and binOpStrs[BinOp.LEQ] != conds[i] \
        and binOpStrs[BinOp.LT] != conds[i]\
        and binOpStrs[BinOp.NEQ] != conds[i] \
        and binOpStrs[MathBinOp.ADD] != conds[i] \
        and binOpStrs[MathBinOp.SUB] != conds[i] \
        and binOpStrs[MathBinOp.MUL] != conds[i] \
        and binOpStrs[MathBinOp.DIV] != conds[i]\
        and binOpStrs[UnaryOp.NEG] != conds[i] \
        and binOpStrs[BinLogicOp.OR] != conds[i]\
        and binOpStrs[BinLogicOp.AND] != conds[i]:

        return Expr(conds[i]), i+1
    if binOpStrs[BinOp.EQ] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return Cmp(BinOp.EQ, left, right), end_index
    elif binOpStrs[BinOp.GEQ] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return Cmp(BinOp.GEQ, left, right), end_index
    elif binOpStrs[BinOp.GT] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return Cmp(BinOp.GT, left, right), end_index
    elif binOpStrs[BinOp.LEQ] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return Cmp(BinOp.LEQ, left, right), end_index
    elif binOpStrs[BinOp.LT] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return Cmp(BinOp.LT, left, right), end_index
    elif binOpStrs[BinOp.NEQ] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return Cmp(BinOp.NEQ, left, right), end_index
    elif binOpStrs[MathBinOp.ADD] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return MathExpr(MathBinOp.ADD, left, right), end_index
    elif binOpStrs[MathBinOp.SUB] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return MathExpr(MathBinOp.SUB, left, right), end_index
    elif binOpStrs[MathBinOp.MUL] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return MathExpr(MathBinOp.MUL, left, right), end_index
    elif binOpStrs[MathBinOp.DIV] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return MathExpr(MathBinOp.DIV, left, right), end_index
    elif binOpStrs[BinOp.LT] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        return Cmp(BinOp.LT, left, right), end_index
    elif binOpStrs[BinLogicOp.AND] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        # return ANDExpr(left, right), end_index
        return BinLogExpr(left, right, BinLogicOp.AND), end_index
    elif binOpStrs[BinLogicOp.OR] == conds[i]:
        left, end_index = translateCondArray2Expr(conds, i+1, n)
        right, end_index = translateCondArray2Expr(conds, end_index, n)
        # return ORExpr(left, right), end_index
        return BinLogExpr(left, right, BinLogicOp.OR), end_index
    elif binOpStrs[UnaryOp.NEG] == conds[i]:
        right, end_index = translateCondArray2Expr(conds, i+1, n)
        return NegExpr(right), end_index
 

def test():
    conds = "GEQ,currentAllowance,amount".split(",")
    conds = "OR;NEQ;value;0;_contains(map,key)".split(";")
    expr, end_index = translateCondArray2Expr(conds, 0, len(conds))
    assert end_index == len(conds), "invalid conds"
    print(expr)

if __name__ == "__main__":
    test()