from sympy import And, Or, symbols, false, true, parse_expr, to_cnf, Not
import graphviz


def load(path, type='sympy'):
    if type == 'sympy':
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


def save_tree(ddnnf, show=False, path='output', filename='graph'):
    graph = graphviz.Graph(format='svg', node_attr={'shape':'circle'})

    add_to_graph(graph, 0, 1, ddnnf)

    graph.render(path+'/'+filename+'.gv', view=show)


def add_to_graph(g, root, new_id, formula):
    nodes = 1

    if formula.is_Atom:
        g.node(str(new_id), label=formula.__str__())
        if root != 0:
            g.edge(str(root), str(new_id))
        return nodes

    if formula.is_Not:
        g.node(str(new_id), label='¬', style='filled', fillcolor='lightgreen')
        if root != 0:
            g.edge(str(root), str(new_id))
        nodes += add_to_graph(g, new_id, new_id + nodes, Not(formula))

    if isinstance(formula, And):
        g.node(str(new_id), label='∧', style='filled', fillcolor='lightblue')
        if root != 0:
            g.edge(str(root), str(new_id))
        for clause in formula.args:
            nodes += add_to_graph(g, new_id, new_id + nodes, clause)

    if isinstance(formula, Or):
        g.node(str(new_id), label='∨', style='filled', fillcolor='lightcoral')
        if root != 0:
            g.edge(str(root), str(new_id))
        for clause in formula.args:
            nodes += add_to_graph(g, new_id, new_id + nodes, clause)

    return nodes
