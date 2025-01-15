import networkx as nx
import heapq as hq
import numpy as np

# Implementação do Branch and Bound

# Função para calcular o limite inferior (bound) de um caminho parcial no grafo
def limite_inferior(grafo, caminho=[]):
    soma = 0
    n_nos = grafo.number_of_nodes()  # Número total de nós no grafo
    restantes = list(range(1, n_nos + 1))  # Lista de nós restantes
    restantes = [x for x in restantes if x not in caminho]  # Filtra os nós que não estão no caminho
    ultimo_no = caminho[-1]  # Último nó no caminho

    # Soma os pesos das arestas no caminho parcial
    for i in range(len(caminho) - 1):
        soma += grafo[caminho[i]][caminho[i + 1]]['weight']

    # Adiciona o menor peso conectando o último nó a um nó restante (se existir)
    if restantes:
        menor_peso_ultimo_no = min(grafo[ultimo_no][v]['weight'] for v in restantes)
        soma += menor_peso_ultimo_no
    else:
        soma += grafo[ultimo_no][caminho[0]]['weight']

    # Adiciona os menores pesos das arestas conectando os nós restantes
    for v in restantes:
        menores_pesos = [grafo[v][w]['weight'] for w in restantes if w != v]
        if menores_pesos:
            soma += min(menores_pesos)

    return soma

# Função principal do Branch and Bound para encontrar o menor caminho hamiltoniano
def branch_and_bound(grafo, n, raiz):
    melhor_limite = limite_inferior(grafo, list(grafo.nodes()))  # Calcula um limite inicial
    raiz_no = (0, limite_inferior(grafo, [raiz]), 0, [raiz])  # (nível, limite, custo, caminho)
    solucao = list(grafo.nodes())  # Caminho inicial (solução trivial)
    fila_prioridade = [raiz_no]  # Heap de prioridades
    hq.heapify(fila_prioridade)

    # Loop principal para explorar os caminhos possíveis
    while fila_prioridade:
        nivel_antigo, limite_antigo, custo_antigo, caminho_antigo = hq.heappop(fila_prioridade)

        # Explorar novos caminhos se o limite for menor que o melhor limite conhecido
        if limite_antigo < melhor_limite:
            novo_nivel = nivel_antigo - 1
            for i in filter(lambda x: x not in caminho_antigo, range(1, n + 1)):
                novo_caminho = caminho_antigo + [i]
                novo_custo = custo_antigo + grafo[caminho_antigo[-1]][i]['weight']

                # Caso base: chegou ao último nível, verifica se o caminho é melhor
                if novo_nivel == -(n - 1):
                    novo_custo += grafo[i][raiz]['weight']  # Adiciona o peso para voltar ao início
                    if melhor_limite > novo_custo:
                        melhor_limite = novo_custo
                        solucao = novo_caminho

                # Caso recursivo: calcula o novo limite e adiciona à fila de prioridade
                else:
                    novo_limite = limite_inferior(grafo, novo_caminho)
                    if novo_limite < melhor_limite:
                        hq.heappush(fila_prioridade, (novo_nivel, novo_limite, novo_custo, novo_caminho))

    return solucao, melhor_limite
