from sympy import And, Or, symbols, false, true, parse_expr, to_cnf


def load(path, type='formula'):
    if type == 'formula':
        with open(path) as f:
            formula = f.readline()
            return to_cnf(parse_expr(formula))

    if type == 'minisat':
        with open(path) as f:
            data = f.readlines()
            expr = true
            for line in data:
                line = line.rstrip().split(" ")

                if line[0] == 'c' or line[0] == 'p':
                    continue

                clause = false
                for value in line[:-1]:
                    if int(value) > 0:
                        clause = Or(clause, symbols('x'+value))
                    else:
                        clause = Or(clause, ~symbols('x'+value[1:]))
                expr = And(expr, clause)
            return expr

    raise Exception("Type not supported")
