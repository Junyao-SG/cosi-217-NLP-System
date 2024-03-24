import graphviz


def create_graph(dependencies: list):
    graph = graphviz.Digraph('graph')
    for (node1, relation, node2) in dependencies:
        if relation == 'ROOT':
            graph.node(node1, shape='box', color='blue3')
        graph.edge(node1, node2, label=relation)
    return graph
