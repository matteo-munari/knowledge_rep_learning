import itertools
import operator
from time import perf_counter_ns

from sympy.abc import *
from sympy.core.symbol import Symbol
from sympy import true, false
from sympy.logic.inference import satisfiable
from sympy.logic.boolalg import And, Or
from sympy import *
import sympy
from sympy.parsing.sympy_parser import split_symbols

from formulas import *


def replace(ddnnf):
    str_ddnnf = ddnnf.__str__()
    str_ddnnf = str_ddnnf.replace("&","*")
    str_ddnnf = str_ddnnf.replace("|","+")
    str_ddnnf = str_ddnnf.replace("~","")
    str_ddnnf = str_ddnnf.replace(f.__str__(), "0")

    for atom in ddnnf.atoms() - {f}:
        str_ddnnf = str_ddnnf.replace(atom.__str__(), "1")

    return str_ddnnf


def count_models_from_ddnnf(ddnnf):
    """WRONG because the ddnnf could start with a AND or with a OR?"""
    count = 1
    for clause in ddnnf.args:
        if clause.is_Atom:
            if clause == f:
                count *= 0
        else:
            count1 = 0
            for sub_clause in clause.args:
                if sub_clause.is_Atom:
                    count1 += 1
                else:
                    count1 += count_models_from_ddnnf(sub_clause)
            count *= count1
    return count


def count_models_from_cnf(cnf_formula):
    if cnf_formula.is_Atom:
        if cnf_formula == f:
            return 0
        else:
            return 1

    components = split_independent(cnf_formula)
    return


if __name__ == "__main__":
    """
    PIPELINE:
        - load/insert formula
        - convert to cnf
        - do recursively:
            ° split in independent components
            ° apply shannon's expansion
        - substitute and count models
    """
    expr = (A >> B | C) & (C >> ~A)
    #expr = (A | B) & (C | D) & (F | ~D)

    cnf = to_cnf(expr)

    ddnnf = to_d_dnnf(cnf, reduction=True)
    print(ddnnf)
    print(replace(ddnnf))

    st = perf_counter_ns()
    print("Parsing replaced string:", parse_expr(replace(ddnnf)))
    end = perf_counter_ns()
    print("Time:", end-st)

    st = perf_counter_ns()
    print("Counting recursively:", count_models_from_ddnnf(ddnnf))
    end = perf_counter_ns()
    print("Time:", end-st)


