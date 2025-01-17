import numpy as np
import networkx as nx
import heapq

class NoDeBusca:
    def __init__(self, limite, custo, caminho, arestas_contadas, tamanho_do_grafo):
        self.limite = limite
        self.custo = custo
        self.caminho = caminho
        self.nivel = len(caminho)
        self.arestas_contadas = arestas_contadas
        self.visitados = np.zeros(tamanho_do_grafo, dtype=bool)
        self.visitados[caminho] = True

    def __lt__(self, outro):
        return self.limite < outro.limite or (self.limite == outro.limite and self.custo < outro.custo)

def atualizar_limite(limite_anterior, no_atual, novo_no, arestas_contadas, grafo):
    peso_min_atual = arestas_contadas[no_atual, 0]
    peso_min_novo = arestas_contadas[novo_no, 0]
    novo_peso = grafo[no_atual][novo_no]['weight']

    novo_limite = limite_anterior - (peso_min_atual + peso_min_novo) + 2 * novo_peso
    return novo_limite, arestas_contadas

def branch_and_bound(grafo, n):
    rotulos = [(i + 1) for i in range(grafo.number_of_nodes())]
    indices = {rotulo: i for i, rotulo in enumerate(rotulos)}
    grafo_com_indices = nx.Graph()
    
    for u, v, data in grafo.edges(data=True):
        grafo_com_indices.add_edge(indices[u], indices[v], weight=data['weight'])


    total = 0
    arestas_contadas = np.zeros((len(grafo), 2), dtype=int)

    for node in grafo.nodes:
        pesos = sorted(
            [grafo[node][vizinho]['weight'] for vizinho in grafo.neighbors(node)]
        )
        if len(pesos) >= 2:
            duas_menores_arestas = pesos[:2]
            total += sum(duas_menores_arestas)
        else:
            duas_menores_arestas = [pesos[0], 0]
            total += pesos[0]

        node_index = list(grafo.nodes).index(node)
        arestas_contadas[node_index, :] = np.argsort([grafo[node][vizinho]['weight'] for vizinho in grafo.neighbors(node)])[:2]

    limite_inicial = total / 2
    
    raiz = NoDeBusca(limite_inicial, 0, [indices[1]], arestas_contadas, len(grafo_com_indices))
    
    fila_de_prioridades = [raiz]
    heapq.heapify(fila_de_prioridades)
    
    melhor_custo = float('inf')
    melhor_caminho = []

    while fila_de_prioridades:
        no_atual = heapq.heappop(fila_de_prioridades)

        if no_atual.nivel == len(grafo_com_indices):
            custo_final = no_atual.custo + grafo_com_indices[no_atual.caminho[-1]][no_atual.caminho[0]]['weight']
            if custo_final < melhor_custo:
                melhor_custo = custo_final
                melhor_caminho = no_atual.caminho + [no_atual.caminho[0]]
        else:
            for proximo_no in range(len(grafo_com_indices)):
                if not no_atual.visitados[proximo_no]:
                    novo_limite, novas_arestas_contadas = atualizar_limite(
                        no_atual.limite,
                        no_atual.caminho[-1],
                        proximo_no,
                        no_atual.arestas_contadas,
                        grafo_com_indices,
                    )
                    if novo_limite < melhor_custo:
                        novo_caminho = no_atual.caminho + [proximo_no]
                        novo_no = NoDeBusca(
                            novo_limite,
                            no_atual.custo
                            + grafo_com_indices[no_atual.caminho[-1]][proximo_no]['weight'],
                            novo_caminho,
                            novas_arestas_contadas,
                            len(grafo_com_indices),
                        )
                        heapq.heappush(fila_de_prioridades, novo_no)

    melhor_caminho_rotulos = [rotulos[i] for i in melhor_caminho]
    return melhor_caminho_rotulos, melhor_custo

if __name__ == "__main__":
    grafo = nx.Graph()
    rotulos = ['A', 'B', 'C', 'D']  
    grafo.add_edge(1, 2, weight=1)
    grafo.add_edge(1, 3, weight=3)
    grafo.add_edge(1, 4, weight=4)
    grafo.add_edge(2, 3, weight=1)
    grafo.add_edge(2, 4, weight=2)
    grafo.add_edge(3, 4, weight=5)
    
    print("Grafo:")
    for u, v, attr in grafo.edges(data=True):
        print(f"Aresta ({u}, {v}) - Peso: {attr['weight']}")

    caminho, custo = branch_and_bound(grafo, rotulos)
    print("\nMelhor caminho encontrado:", caminho)
    print("Custo do melhor caminho:", custo)
