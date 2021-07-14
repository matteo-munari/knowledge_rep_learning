from formulas import t, f


def count_models_from_ddnnf(ddnnf):
    return count_models(ddnnf & t)


def count_models(ddnnf):
    count = 1
    for clause in ddnnf.args:
        if clause.is_Atom or clause.is_Not:
            if clause == f:
                return count*0
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
