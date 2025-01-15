import math
import networkx as nx
import Christofides
import twicearound_the_tree as TAtT
import branch_and_bound as BnB
import time


def carregar_grafo(caminho_arquivo):
    """
    Lê um arquivo .tsp e constrói um grafo NetworkX com os pesos baseados na distância euclidiana.
    
    Parâmetros:
    - caminho_arquivo: Caminho para o arquivo .tsp.

    Retorna:
    - grafo: Objeto NetworkX Graph contendo os nós e arestas com pesos.
    - tamanho: Número de nós no grafo.
    - nome: Nome do problema (extraído do arquivo .tsp).
    """
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    # Variáveis para armazenar informações do grafo
    nome = ""
    tamanho = 0
    nos = []
    secao_nos = False

    # Processa o arquivo linha a linha
    for linha in linhas:
        linha = linha.strip()
        partes = linha.split()
        
        # Verifica as informações do cabeçalho
        if partes[0] in {"NAME", "NAME:"}:
            nome = partes[-1]
            continue
        if partes[0] in {"DIMENSION", "DIMENSION:"}:
            tamanho = int(partes[-1])
            continue
        if partes[0] == "NODE_COORD_SECTION":
            secao_nos = True
            continue
        if partes[0] == "EOF":
            break
        
        # Lê os dados dos nós
        if secao_nos:
            id_no = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            nos.append((id_no, x, y))
    
    # Cria o grafo
    grafo = nx.Graph()
    for id_no, x, y in nos:
        grafo.add_node(id_no, pos=(x, y))
    
    # Adiciona arestas com pesos baseados na distância euclidiana
    for i in range(tamanho):
        for j in range(i + 1, tamanho):
            id1, x1, y1 = nos[i]
            id2, x2, y2 = nos[j]
            distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            grafo.add_edge(id1, id2, weight=distancia)
    
    return grafo, tamanho, nome


# Exemplo de uso
if __name__ == "__main__":
    # Carrega o grafo a partir do arquivo .tsp
    caminho_arquivo = 'test_cases/rl11849.tsp'  # Atualize com o caminho correto
    grafo, tamanho, nome_problema = carregar_grafo(caminho_arquivo)
    
    print(f"Problema: {nome_problema}")
    print(f"Número de nós: {tamanho}")
    
    # Medição de tempo para cada algoritmo
    inicio = time.time()
    
    # Branch and Bound
    inicio_bnb = time.time()
    resultado_bnb = BnB.BnB(grafo, tamanho, 1)
    fim_bnb = time.time()
    
    # Twice Around the Tree
    inicio_tatt = time.time()
    resultado_tatt = TAtT.twice_around_the_tree(grafo, 1)
    fim_tatt = time.time()
    
    # Christofides
    inicio_christofides = time.time()
    resultado_christofides = Christofides.Christofides(grafo, 1)
    fim_christofides = time.time()
    
    # Resultados
    print("\nResultados:")
    print(f"Branch and Bound: {resultado_bnb}, Tempo: {fim_bnb - inicio_bnb:.2f} segundos")
    print(f"Twice Around the Tree: {resultado_tatt}, Tempo: {fim_tatt - inicio_tatt:.2f} segundos")
    print(f"Christofides: {resultado_christofides}, Tempo: {fim_christofides - inicio_christofides:.2f} segundos")
    
    fim = time.time()
    print(f"\nTempo total de execução: {fim - inicio:.2f} segundos")
