from sympy import *


f, t = symbols('⊥, ⊤')


def split_independent(cnf_formula):
    atoms = cnf_formula.atoms() - {f, t}
    clauses = list(cnf_formula.args)
    components = []
    "POP first atom, save all formulas that present it, then iteratively do the same for all new atoms inserted"
    "When this first step stop in the first element of the list append the and of all clauses"
    "Continue popping and checking until all atoms are checked"
    while atoms:
        atom = atoms.pop()
        to_check = {atom}
        conj = And()

        while to_check:
            check_atom = to_check.pop()
            remaining = []
            for clause in clauses:
                if check_atom in clause.atoms():
                    conj = And(conj, clause)
                    to_check = to_check.union(conj.atoms()) - {f, t, check_atom}
                    atoms = atoms.difference(conj.atoms())
                else:
                    remaining.append(clause)
            clauses = remaining

        components.append(conj)

    for clause in clauses:
        components.append(clause)
    return components


def most_frequent_atom(cnf_formula):
    most_frequent = None
    count = 0
    for atom in cnf_formula.atoms():
        occurences = cnf_formula.count(atom)
        if atom != f and atom != t and occurences > count:
            most_frequent = atom
            count = occurences
    return most_frequent


def shannon_exp(cnf_formula, atom):
    f0 = And(~atom, cnf_formula.replace(~atom, t).replace(atom, f))
    f1 = And(atom, cnf_formula.replace(~atom, f).replace(atom, t))

    return Or(f0, f1)


def reduce(cnf_formula):
    reduced = And()
    for clause in cnf_formula.args:
        if not clause.is_Atom:
            clause = clause.replace(f, false)
        reduced = And(reduced, clause)
    return reduced


def to_d_dnnf(cnf_formula, reduction=True):
    components = split_independent(cnf_formula)
    result = And()
    for component in components:
        if component.is_Atom or len(component.atoms() - {f, t}) <= 1:
            result = And(result, component)
        else:
            atom = most_frequent_atom(component)
            expansion = shannon_exp(component, atom)

            f0, f1 = expansion.args
            if reduction:
                f0 = reduce(f0)
                f1 = reduce(f1)

            f0 = to_d_dnnf(f0, reduction)
            f1 = to_d_dnnf(f1, reduction)

            result = And(result, Or(f0, f1))
    return result


def replace(ddnnf):
    str_ddnnf = ddnnf.__str__()

    subst_dict = {'&':'*',
                  '|':'+',
                  '~':'',
                  '⊥':'0'}
    for atom in ddnnf.atoms() - {f}:
        subst_dict[atom.__str__()] = '1'

    for key, item in subst_dict.items():
        str_ddnnf = str_ddnnf.replace(key, item)

    return str_ddnnf
