# Implementação do algoritmo de Christofides
import networkx as nx
import matplotlib.pyplot as plt


# Funções auxiliares
def plota_grafo(grafo):
    """
    Função para plotar o grafo, exibindo os pesos das arestas.
    """
    posicao = nx.spring_layout(grafo)  # Layout para distribuir os nós de forma legível
    nx.draw(grafo, posicao, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')

    # Desenha os pesos nas arestas
    rotulos_arestas = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, posicao, edge_labels=rotulos_arestas)

    # Exibe o grafo
    plt.show()


def dfs(grafo, no_inicial, visitados=None):
    """
    Realiza uma busca em profundidade (DFS) no grafo.
    Retorna as arestas do circuito Euleriano encontrado.
    """
    resultado = []
    if visitados is None:
        visitados = set()

    visitados.add(no_inicial)

    for vizinho in grafo.neighbors(no_inicial):
        if vizinho not in visitados:
            resultado.append([no_inicial, vizinho])
            resultado.extend(dfs(grafo, vizinho, visitados))

    return resultado


def calcula_peso(grafo, caminho):
    """
    Calcula o peso total de um caminho no grafo.
    """
    peso_total = 0
    for i in range(len(caminho) - 1):
        peso_total += grafo[caminho[i]][caminho[i + 1]]['weight']
    return peso_total


# Implementação do algoritmo de Christofides
def algoritmo_christofides(grafo, raiz):
    """
    Algoritmo de Christofides para o problema do caixeiro viajante.
    Retorna o menor caminho encontrado e seu peso total.
    """
    # Etapa 1: Calcula a árvore geradora mínima (Minimum Spanning Tree - MST)
    arvore_geradora = nx.minimum_spanning_tree(grafo, algorithm='prim')
    grafo_auxiliar = nx.MultiGraph(arvore_geradora)  # Grafo auxiliar para construir o circuito Euleriano

    # Identifica os nós de grau ímpar na árvore geradora
    nos_grau_impar = [no for no in arvore_geradora.nodes if arvore_geradora.degree[no] % 2 != 0]

    # Etapa 2: Calcula o emparelhamento mínimo (Minimum Weight Matching) para os nós de grau ímpar
    emparelhamento_minimo = nx.algorithms.min_weight_matching(grafo.subgraph(nos_grau_impar), weight='weight')
    grafo_auxiliar.add_edges_from(emparelhamento_minimo)

    # Etapa 3: Encontra o circuito Euleriano no grafo resultante
    circuito_euleriano = dfs(grafo_auxiliar, raiz)

    # Etapa 4: Constrói o caminho hamiltoniano (eliminando nós repetidos)
    caminho = []
    visitados = set()
    for u, v in circuito_euleriano:
        if u not in visitados:
            caminho.append(u)
            visitados.add(u)
        if v not in visitados:
            caminho.append(v)
            visitados.add(v)
    caminho.append(caminho[0])  # Retorna ao nó inicial para fechar o circuito

    # Calcula o peso total do caminho
    peso_total = calcula_peso(grafo, caminho)

    return caminho, peso_total
