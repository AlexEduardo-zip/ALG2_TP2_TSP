import networkx as nx

def calcula_peso(grafo, caminho):
    peso_total = 0
    for i in range(len(caminho) - 1):
        peso_total += grafo[caminho[i]][caminho[i + 1]]['weight']
    return peso_total


def twice_around_the_tree(grafo, raiz):
    # Etapa 1: Constrói a árvore geradora mínima (Minimum Spanning Tree - MST)
    arvore_geradora = nx.minimum_spanning_tree(grafo, algorithm='prim')

    # Etapa 2: Realiza uma busca em profundidade (DFS) para criar o circuito Euleriano
    percurso_euleriano = list(nx.dfs_preorder_nodes(arvore_geradora, source=raiz))
    percurso_euleriano.append(percurso_euleriano[0])  # Fecha o circuito adicionando o nó inicial ao final

    # Etapa 3: Calcula o peso total do circuito
    peso_total = calcula_peso(grafo, percurso_euleriano)

    return percurso_euleriano, peso_total
