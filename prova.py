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

from formulas import to_d_dnnf, replace, list_notation
from model_counting import *
from utils import load

from pysat.solvers import Solver

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

    cnf = load('files/example_sympy_3.txt', 'formula')

    #expr = (A >> B | C) & (C >> ~A)
    #expr = (A | B) & (C | D) & (F | ~D)
    #expr = (A | B) >> C
    #expr = ((~A | B) >> C) | ((~B >> A) >> C)
    print("CNF formula:", cnf)

    ddnnf = to_d_dnnf(cnf, reduction=False)
    print("d-DNNF formula:", ddnnf)

    print("---------------------------")
    print("Ground Truth computed with pysat")
    pysat_cnf = list_notation(cnf)
    print(pysat_cnf)
    s = Solver(bootstrap_with=pysat_cnf)
    gt_count = 0
    gc.disable()
    st = perf_counter_ns()
    for m in s.enum_models():
        gt_count += 1
    end = perf_counter_ns()
    gc.enable()
    print("N° models:", gt_count)
    print("Time:", end - st)

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


