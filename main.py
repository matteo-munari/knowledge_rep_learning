import argparse
import gc
import os
from time import perf_counter_ns, time

from sympy import *
from sympy.abc import *
from sympy.logic.boolalg import conjuncts

from formulas import to_d_dnnf, replace, list_notation, count_prop_variables
from model_counting import *
from utils import load, save_tree

from pysat.solvers import Solver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=None, help='input source, if not specified read from standard input')
    parser.add_argument('--source-type', type=str, default=None, help='supported file type: sympy, minisat')
    parser.add_argument('--no-reduction', action='store_true', help='do not apply reductions to d-DNNF formula')
    parser.add_argument('--save-tree', action='store_true', help='save d-DNNF tree image')
    parser.add_argument('--show-tree', action='store_true', help='show d-DNNF tree image')
    parser.add_argument('--output-path', type=str, default='output', help='output folder path')
    parser.add_argument('--output-format', type=str, default='svg', help='output file format: svg, png, pdf...')

    args = parser.parse_args()

    if args.source and not args.source_type:
        parser.error("--source argument requires --source-type")

    "SEE IF USING CONJUNCTS AND DISJUNCTS FUNCTIONS THE COMPUTATIONS ARE SIMPLER"
    #print(conjuncts((A | B) & B))

    if not args.source:
        print("Insert formula:", end=" ")
        original_formula = input()
        n_variables = count_prop_variables(original_formula)
        cnf = to_cnf(parse_expr(original_formula))
    else:
        cnf, original_formula, n_variables = load(args.source, type=args.source_type)

    if original_formula:
        print(f"Original formula:\n  {original_formula}")
    print(f"Reduced CNF formula:\n  {cnf}")
    n_var_in_cnf = len(cnf.atoms() - {false, true, f, t})
    ignored_vars = n_variables - n_var_in_cnf
    print("Variables")
    print(f"  Total:{n_variables}\n  In reduced CFN:{n_var_in_cnf}\n  Ignored:{ignored_vars}")

    if args.no_reduction:
        ddnnf = to_d_dnnf(cnf, reduction=False)
    else:
        ddnnf = to_d_dnnf(cnf, reduction=True)
    print(f"d-DNNF formula:\n  {ddnnf}")

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
    print(f"N° of models of CNF formula: {gt_count}")
    print(f"N° of ignored variables: {ignored_vars}")
    print(f"Total N° of models: {gt_count} * 2^({ignored_vars}) = {gt_count * 2 ** ignored_vars}")
    print(f"Time: {(end - st)//1e3} ms")

    print("---------------------------")
    print("Model counting via Knowledge Compilation")
    gc.disable()
    st = perf_counter_ns()
    count2 = count_models_from_ddnnf(ddnnf)
    end = perf_counter_ns()
    gc.enable()
    print(f"N° of models of CNF formula: {count2}")
    print(f"N° of ignored variables: {ignored_vars}")
    print(f"Total N° of models: {count2} * 2^({ignored_vars}) = {count2 * 2**ignored_vars}")
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

    if not args.source:
        filename = str(time())
    else:
        basename = os.path.split(args.source)[1]
        filename = os.path.splitext(basename)[0]

    if args.show_tree:
        save_tree(ddnnf, show=True, path=args.output_path, filename=filename, format=args.output_format)
    elif args.save_tree:
        save_tree(ddnnf, show=False, path=args.output_path, filename=filename, format=args.output_format)