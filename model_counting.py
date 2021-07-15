from sympy import Or

from formulas import t, f


def count_models_from_ddnnf(ddnnf):
    if isinstance(ddnnf, Or):
        return count_models(ddnnf & t)
    return count_models(ddnnf)


def count_models(ddnnf):
    if ddnnf is f:
        return 0

    count = 1
    for clause in ddnnf.args:
        if clause.is_Atom or clause.is_Not:
            if clause is f:
                return 0  # False in conjunction causes the product to be zero
        else:
            count1 = 0
            for sub_clause in clause.args:
                if sub_clause.is_Atom or sub_clause.is_Not:
                    if sub_clause is not f:
                        count1 += 1
                else:
                    count1 += count_models(sub_clause)
            count *= count1
    return count
