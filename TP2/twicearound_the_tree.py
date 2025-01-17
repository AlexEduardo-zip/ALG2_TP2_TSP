import networkx as nx

def twice_around_the_tree(grafo, raiz):
    arvore_geradora = nx.minimum_spanning_tree(grafo, algorithm='prim')

    percurso_euleriano = list(nx.dfs_preorder_nodes(arvore_geradora, source=raiz))
    percurso_euleriano.append(percurso_euleriano[0])  # Fecha o circuito

    peso_total = sum(grafo[percurso_euleriano[i]][percurso_euleriano[i + 1]]['weight'] for i in range(len(percurso_euleriano) - 1))

    return percurso_euleriano, peso_total
