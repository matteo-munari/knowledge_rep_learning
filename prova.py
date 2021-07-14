import gc
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

from formulas import to_d_dnnf, replace
from model_counting import *
from utils import load

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
    cnf = load('files/example_sympy_1.txt', 'sympy')
    #cnf = parse_expr('(x1 | x2) & x3')
    print(cnf)


    #expr = (A >> B | C) & (C >> ~A)
    #expr = (A | B) & (C | D) & (F | ~D)
    #expr = (A | B) >> C
    #expr = ((~A | B) >> C) | ((~B >> A) >> C)

    print("CNF formula:", cnf)

    ddnnf = to_d_dnnf(cnf, reduction=False)
    print("d-DNNF formula:", ddnnf)

    print("---------------------------")
    print("First method")
    gc.disable()
    st = perf_counter_ns()
    replaced = replace(ddnnf)
    count1 = parse_expr(replaced)
    end = perf_counter_ns()
    gc.enable()
    print("Replaced expression:", replaced)
    print("Count:", count1)
    print("Time:", end - st)

    print("---------------------------")
    print("Second method")
    gc.disable()
    st = perf_counter_ns()
    count2 = count_models_from_ddnnf(ddnnf)
    end = perf_counter_ns()
    gc.enable()
    print("Count:", count2)
    print("Time:", end - st)

