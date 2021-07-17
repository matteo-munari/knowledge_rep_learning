from sympy.logic.boolalg import conjuncts, disjuncts, false

from formulas import f


def count_models(ddnnf):
    count = 1
    for conjunct in conjuncts(ddnnf):
        if conjunct is f or conjunct is false:
            return 0
        if not conjunct.is_Atom and not conjunct.is_Not:
            count1 = 0
            for disjunct in disjuncts(conjunct):
                if disjunct.is_Atom or disjunct.is_Not:
                    if disjunct is not f and disjunct is not false:
                        count1 += 1
                else:
                    count1 += count_models(disjunct)
            count *= count1
    return count
