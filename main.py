import argparse
import gc
import itertools
import operator
import sys
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
from utils import load, save_tree

from pysat.solvers import Solver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--source-type', type=str, default='formula')
    parser.add_argument('--no-reduction', action='store_true')
    parser.add_argument('--save-tree', action='store_true')
    parser.add_argument('--show-tree', action='store_true')
    parser.add_argument('--output-path', type=str, default='output')

    args = parser.parse_args()

    if args.source_type == 'formula':
        cnf = to_cnf(parse_expr(args.source))
    else:
        cnf = load(args.source, type=args.source_type)

    print(f"CNF formula:\n {cnf}")

    if args.no_reduction:
        ddnnf = to_d_dnnf(cnf, reduction=False)
    else:
        ddnnf = to_d_dnnf(cnf, reduction=True)
    print(f"d-DNNF formula:\n {ddnnf}")

    print("---------------------------")
    print("Ground Truth - Model Counting enumerating models")
    pysat_cnf = list_notation(cnf)
    s = Solver(bootstrap_with=pysat_cnf)
    gt_count = 0
    gc.disable()
    st = perf_counter_ns()
    for m in s.enum_models():
        gt_count += 1
    end = perf_counter_ns()
    gc.enable()
    print(f"N° models: {gt_count}")
    print(f"Time: {(end - st)//1e3} ms")

    print("---------------------------")
    print("Model counting via Knowledge Compilation")
    print(f"Replaced expression: {replace(ddnnf)}")
    gc.disable()
    st = perf_counter_ns()
    count2 = count_models_from_ddnnf(ddnnf)
    end = perf_counter_ns()
    gc.enable()
    print(f"N° models: {count2}")
    print(f"Time: {(end - st)//1e3} ms")

    """print("---------------------------")
    print("Model counting parsing replaced d-DNNF")
    gc.disable()
    st = perf_counter_ns()
    replaced = replace(ddnnf)
    count1 = parse_expr(replaced)
    end = perf_counter_ns()
    gc.enable()
    print("Replaced expression:", replaced)
    print(f"N° models: {count1}")
    print(f"Time: {(end - st)//1e3} ms")"""

    if args.show_tree:
        save_tree(ddnnf, show=True, path=args.output_path)
    elif args.save_tree:
        save_tree(ddnnf, show=False, path=args.output_path)