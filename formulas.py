from sympy import *
from sympy.logic.boolalg import conjuncts

f, t = symbols('⊥, ⊤')


def count_prop_variables(str_formula):
    symbols = {'&', '|', '>', '<', '(', ')', 'True', 'False', '~', 'false', 'true'}
    for symb in symbols:
        str_formula = str_formula.replace(symb, ' ')
    symbols = str_formula.split()
    return len(set(symbols))


def split_independent(cnf_formula):
    atoms = cnf_formula.atoms() - {f, t, true, false}
    print(atoms)
    clauses = conjuncts(cnf_formula)
    components = []
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
    return most_frequent, count


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
        atom, count = most_frequent_atom(component)
        if count < 2 and (component.is_Atom or len(component.atoms() - {f, t}) <= 1):
            result = And(result, component)
        else:
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

    subst_dict = {'&': '*',
                  '|': '+',
                  '~': '',
                  '⊥': '0'}
    for atom in ddnnf.atoms() - {f}:
        subst_dict[atom.__str__()] = '1'

    sorted_keys = sorted(subst_dict.keys(), reverse=True)

    for key in sorted_keys:
        str_ddnnf = str_ddnnf.replace(key, subst_dict[key])

    return str_ddnnf


def list_notation(cnf):
    if cnf == f or cnf == false:
        return [[]]
    if cnf == t or cnf == true:
        return []

    dict = {}
    id = 1
    formula = []

    for clause in conjuncts(cnf):
        if clause.is_Atom:
            if clause not in dict:
                dict[clause] = id
                id += 1
            formula.append([dict[clause]])
        elif clause.is_Not:
            if Not(clause) not in dict:
                dict[Not(clause)] = id
                id += 1
            formula.append([-dict[Not(clause)]])
        else:
            list_clause = []
            for element in clause.args:
                if element.is_Atom:
                    if element not in dict:
                        dict[element] = id
                        id += 1
                    list_clause.append(dict[element])
                else:
                    if Not(element) not in dict:
                        dict[Not(element)] = id
                        id += 1
                    list_clause.append(-dict[Not(element)])
            formula.append(list_clause)

    """if isinstance(cnf, Or):
        list_clause = []
        for element in cnf.args:
            if element.is_Atom:
                if element not in dict:
                    dict[element] = id
                    id += 1
                list_clause.append(dict[element])
            else:
                if Not(element) not in dict:
                    dict[Not(element)] = id
                    id += 1
                list_clause.append(-dict[Not(element)])
        formula.append(list_clause)
    else:
        for clause in cnf.args:
            if clause.is_Atom:
                if clause not in dict:
                    dict[clause] = id
                    id += 1
                formula.append([dict[clause]])
            elif clause.is_Not:
                if Not(clause) not in dict:
                    dict[Not(clause)] = id
                    id += 1
                formula.append([-dict[Not(clause)]])
            else:
                list_clause = []
                for element in clause.args:
                    if element.is_Atom:
                        if element not in dict:
                            dict[element] = id
                            id += 1
                        list_clause.append(dict[element])
                    else:
                        if Not(element) not in dict:
                            dict[Not(element)] = id
                            id += 1
                        list_clause.append(-dict[Not(element)])
                formula.append(list_clause)"""
    return formula
