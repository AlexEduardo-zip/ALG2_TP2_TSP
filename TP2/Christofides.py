import networkx as nx

def algoritmo_christofides(G, no_inicial):

    MST = nx.minimum_spanning_tree(G)

    nos_impares = [no for no, grau in MST.degree() if grau % 2 == 1]

    subgrafo_nos_impares = G.subgraph(nos_impares)

    emparelhamento = nx.min_weight_matching(subgrafo_nos_impares)

    MSTMultigrafo = nx.MultiGraph(MST)

    for no1, no2 in emparelhamento:
        MSTMultigrafo.add_edge(no1, no2, weight=G[no1][no2]['weight'])

    caminho = [x[no_inicial] for x in nx.eulerian_circuit(MSTMultigrafo, source=no_inicial)]
    caminho_atalho = list(dict.fromkeys(caminho))
    caminho = caminho_atalho + [caminho_atalho[0]]

    peso = sum(G[caminho[i]][caminho[i + 1]]['weight'] for i in range(len(caminho) - 1))

    return caminho, peso
