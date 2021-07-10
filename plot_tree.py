import networkx
import pydot

dot_string = """graph my_graph {
    bgcolor="yellow";
    a [label="Foo"];
    b [shape=circle];
    a -- b -- c [color=blue];
    a -- g;
}"""

graphs = pydot.graph_from_dot_data(dot_string)
graph = graphs[0]

#graph.write("output.png")
graph.write_png("output.png")

"USE COLAB"
