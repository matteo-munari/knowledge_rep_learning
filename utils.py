#Copyright 2021 by Matteo Munari

from sympy import And, Or, symbols, false, true, parse_expr, to_cnf, Not
import graphviz

from formulas import count_prop_variables, f, t


def load(path, type='sympy'):
    if type == 'sympy':
        with open(path) as f:
            formula = f.readline()
            return to_cnf(parse_expr(formula)), formula, count_prop_variables(formula)

    if type == 'minisat':
        with open(path) as f:
            n_var = 0
            data = f.readlines()
            expr = true
            for line in data:
                line = line.rstrip().split(" ")

                if line[0] == 'c':
                    continue

                if line[0] == 'p':
                    n_var = int(line[2])
                    continue

                clause = false
                for value in line[:-1]:
                    if int(value) > 0:
                        clause = Or(clause, symbols('x'+value))
                    else:
                        clause = Or(clause, ~symbols('x'+value[1:]))
                expr = And(expr, clause)
            return expr, None, n_var

    raise Exception("Type not supported")


def save_tree(ddnnf, show=False, path='output', filename='graph', format='svg'):
    graph = graphviz.Graph(format=format, node_attr={'shape':'circle'})

    if format == 'svg':
        labels = {'not':'¬', 'and':'∧', 'or':'∨', 'true':'⊤', 'false':'⊥'}
    else:
        labels = {'not':'¬', 'and': 'And', 'or':'Or', 'true':'T', 'false':'F'}

    add_to_graph(graph, 0, 1, ddnnf, labels)

    graph.render(path+'/'+filename+'.gv', view=show)


def add_to_graph(g, root, new_id, formula, labels):
    nodes = 1

    if formula.is_Atom:
        if formula == f:
            g.node(str(new_id), label=labels['false'])
        elif formula == t:
            g.node(str(new_id), label=labels['true'])
        else:
            g.node(str(new_id), label=formula.__str__())

        if root != 0:
            g.edge(str(root), str(new_id))
        return nodes

    if formula.is_Not:
        g.node(str(new_id), label=labels['not'], style='filled', fillcolor='lightgreen')
        if root != 0:
            g.edge(str(root), str(new_id))
        nodes += add_to_graph(g, new_id, new_id + nodes, Not(formula), labels)

    if isinstance(formula, And):
        g.node(str(new_id), label=labels['and'], style='filled', fillcolor='lightblue')
        if root != 0:
            g.edge(str(root), str(new_id))
        for clause in formula.args:
            nodes += add_to_graph(g, new_id, new_id + nodes, clause, labels)

    if isinstance(formula, Or):
        g.node(str(new_id), label=labels['or'], style='filled', fillcolor='lightcoral')
        if root != 0:
            g.edge(str(root), str(new_id))
        for clause in formula.args:
            nodes += add_to_graph(g, new_id, new_id + nodes, clause, labels)

    return nodes
