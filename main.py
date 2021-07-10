import itertools
import operator

from sympy.abc import *
from sympy.core.symbol import Symbol
from sympy import true, false
from sympy.logic.inference import satisfiable
from sympy.logic.boolalg import And
from sympy import *
import sympy
from sympy.parsing.sympy_parser import split_symbols


def get_atoms(formula):
    atoms = set()
    for disjunct in formula:
        atoms = atoms.union(disjunct.atoms())
        atoms = atoms.difference([true, false])
    return atoms


def split_cnf_formula(formula): #can be made more efficient using graphs
    ind_components = []
    update = True
    while formula:
        atoms = set()
        first = formula.pop()
        component = [first]
        atoms = atoms.union(get_atoms(first))

        while update:
            update = False

            for f in formula:
                f_atoms = get_atoms(f)
                if atoms.intersection(f_atoms):
                    atoms = atoms.union(f_atoms)
                    formula.remove(f)
                    component.append(f)
                    update = True

        ind_components.append(component)

    return ind_components


def substitute(formula, atom):
    """
    Substitute every occurence of atom with True and of ~atom with False

    :param formula: disjunction of propositions
    :param atom: an atom, can be in the form A or ~A
    :return: the formula with the substitutions applied
    """
    f = []
    for elem in formula:
        if elem == atom:
            f.append(true)
        elif elem == ~atom:
            f.append(false)
        else:
            f.append(elem)

    return f


def reduce(cnf_formula):
    reduced_f = []
    for conjunct in cnf_formula:
        reduced_clause = []
        for disjunct in conjunct:
            if disjunct is not false:
                if not isinstance(disjunct, list) or disjunct is true:
                    if disjunct not in reduced_clause:
                        reduced_clause.append(disjunct)
                else:
                    reduced_clause.append(reduce(disjunct))

        reduced_f.append(reduced_clause) if reduced_clause else reduced_f.append([false])

    return reduced_f


def shannons_expansion(formula):

    # find the atom with highest number of occurences
    occurences = {}
    for conjunct in formula:
        conj_atoms = get_atoms(conjunct)
        for atom in conj_atoms:
            if atom not in occurences:
                occurences[atom] = 1
            else:
                occurences[atom] += 1

    # check if the formula contains only one propositional variable
    if len(occurences) > 1:
        most_frequent = max(occurences.items(), key=operator.itemgetter(1))[0]

        f0 = [[~most_frequent]]
        f1 = [[most_frequent]]

        for conjunct in formula:
            f0.append(substitute(conjunct, ~most_frequent))
            f1.append(substitute(conjunct, most_frequent))

        return [[make_d_dnnf(f0), make_d_dnnf(f1)]]

    return formula


def make_d_dnnf(cnf_formula):
    components = split_cnf_formula(cnf_formula)

    expanded_formula = [shannons_expansion(component) for component in components]

    return [f for formulas in expanded_formula for f in formulas]


def count_models(ddnnf_formula):
    if not isinstance(ddnnf_formula, list):
        return 0 if ddnnf_formula is false else 1

    counts = 1
    for conjunct in ddnnf_formula:
        conj_count = 0
        for disjunct in conjunct:
            disj_count = count_models(disjunct)
            conj_count += disj_count

        counts *= conj_count

    return counts


def cnf_to_list(cnf_formula):
    f = []
    for clause in cnf_formula.args:
        f_i = []
        for atom in clause.args:
            f_i.append(atom)
        f.append(f_i)

    return f


if __name__ == "__main__":
    at = ~A
    #t = [at, true]
    #print(get_atoms(t))

    #expr = input()

    expr = (A >> B | C) & (C >> ~A)
    cnf = to_cnf(expr)

    print(cnf)
    list_cnf = cnf_to_list(cnf)
    print(list_cnf)
    ddnnf = make_d_dnnf(list_cnf)
    print(ddnnf)
    mc = count_models(ddnnf)
    print(mc)

    """expr = '(A | B) & ~C & A'
    pexp = parse_expr(expr)
    atoms = pexp.atoms()
    print(pexp)"""


    """#formula = [[A, B], [C, D], [~D, F]] # COUNT = 12
    formula = [[~A, B, C], [~C, ~A]] # COUNT = 5
    #formula = [[~A, A]]

    ddnnf = make_d_dnnf(formula)

    print(ddnnf)
    print("START REDUCTION")
    #isatom = {true, false, A, B, C, D, F, ~A, ~B, ~C, ~D, ~F}
    reduced = reduce(ddnnf)
    print(reduced)

    mc = count_models(reduced)
    print(mc)

    #print(srepr(expr))"""

    #cnf = [[false, false, A, true, A], [[[C, false], [D]], D], [false]]
    #print(reduce(cnf))"""

