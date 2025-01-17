import math
import networkx as nx
import Christofides
import twicearound_the_tree as TAtT
import branch_and_bound as BnB 
import time
import threading
import psutil
import os
import csv

# def carregar_grafo(caminho_arquivo):
#     with open(caminho_arquivo, 'r') as arquivo:
#         linhas = arquivo.readlines()
    
#     nome = ""
#     tamanho = 0
#     nos = []
#     secao_nos = False

#     for linha in linhas:
#         linha = linha.strip()
#         partes = linha.split()
        
#         if partes[0] in {"NAME", "NAME:"}:
#             nome = partes[-1]
#             continue
#         if partes[0] in {"DIMENSION", "DIMENSION:"}:
#             tamanho = int(partes[-1])
#             continue
#         if partes[0] == "NODE_COORD_SECTION":
#             secao_nos = True
#             continue
#         if partes[0] == "EOF":
#             break
        
#         if secao_nos:
#             id_no = int(partes[0])
#             x = float(partes[1])
#             y = float(partes[2])
#             nos.append((id_no, x, y))
    
#     grafo = nx.Graph()
#     for id_no, x, y in nos:
#         grafo.add_node(id_no, pos=(x, y))
    
#     for i in range(tamanho):
#         for j in range(i + 1, tamanho):
#             id1, x1, y1 = nos[i]
#             id2, x2, y2 = nos[j]
#             distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#             grafo.add_edge(id1, id2, weight=distancia)
    
#     return grafo, tamanho, nome

def carregar_grafo(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    nome = ""
    tamanho = 0
    nos = []
    secao_nos = False

    for linha in linhas:
        linha = linha.strip()
        partes = linha.split()
        
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
        
        if secao_nos:
            id_no = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            nos.append((id_no, x, y))
    
    # Criar o grafo
    grafo = nx.Graph()
    
    # Adicionar nós com suas posições
    for id_no, x, y in nos:
        grafo.add_node(id_no, pos=(x, y))
    
    # Adicionar as arestas com o peso calculado pela distância euclidiana
    for i in range(tamanho):
        for j in range(i + 1, tamanho):
            id1, x1, y1 = nos[i]
            id2, x2, y2 = nos[j]
            distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            grafo.add_edge(id1, id2, weight=distancia)
    
    return grafo, tamanho, nome

def executar_com_tempo_limite(func, args, timeout):
    resultado = [None]
    excecao = [None]

    def wrapper():
        try:
            resultado[0] = func(*args)
        except Exception as e:
            excecao[0] = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return "Excedeu o limite de tempo"
    if excecao[0]:
        raise excecao[0]
    return resultado[0]

def monitorar_memoria(func, *args):

    processo = psutil.Process(os.getpid())
    memoria_inicial = processo.memory_info().vms  
    
    inicio = time.time()
    resultado = func(*args)  
    fim = time.time()

    memoria_final = processo.memory_info().vms 
    memoria_usada = memoria_final - memoria_inicial

    tempo_execucao = fim - inicio

    if isinstance(resultado, tuple) and len(resultado) == 2:
        caminho, peso_total = resultado
    else:
        caminho, peso_total = None, None

    return caminho, peso_total, memoria_usada, tempo_execucao

def executar_algoritmo(nome_problema, solucao_otima, grafo, tamanho, algoritmo_func, nome_algoritmo):
    resultado = executar_com_tempo_limite(monitorar_memoria, (algoritmo_func, grafo, 1), 1800)
    
    if resultado == "Excedeu o limite de tempo":
        return {
            'nome_do_problema': nome_problema,
            'algoritmo_utilizado': nome_algoritmo,
            'quantidade_Nos': tamanho,
            'tempo_de_Execucao': 'Excedeu o limite de tempo',
            'quantidade_memoria_em_mb': 'N/A',
            'fator_aproximacao': 'N/A',
            'caminho': 'N/A',
            'peso_total': 'N/A',
            'solucao_otima': solucao_otima
        }

    caminho, peso_total, memoria, tempo_execucao = resultado
    fator_aproximacao = peso_total / solucao_otima if peso_total != 'Excedeu o limite de tempo' else 'N/A'
    return {
        'nome_do_problema': nome_problema,
        'algoritmo_utilizado': nome_algoritmo,
        'quantidade_Nos': tamanho,
        'tempo_de_Execucao': f"{tempo_execucao:.5f}",
        'quantidade_memoria_em_mb': f"{memoria / (1024 ** 2):.2f}",
        'fator_aproximacao': fator_aproximacao,
        'caminho': caminho,
        'peso_total': peso_total,
        'solucao_otima': solucao_otima
    }

def ler_problemas_csv(caminho_arquivo):
    problemas = []
    with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nome_problema = row['nome_do_problema']
            solucao_otima = float(row['solucao'])
            problemas.append((nome_problema, solucao_otima))
    return problemas

def executar_todos_algoritmos(nome_problema, solucao_otima, grafo, tamanho, algoritmos_escolhidos):
    algoritmos_disponiveis = {
        'bnb': (BnB.branch_and_bound, 'Branch and Bound'),
        'tatt': (TAtT.twice_around_the_tree, 'Twice Around the Tree'),
        'chr': (Christofides.algoritmo_christofides, 'Christofides')
    }

    # Se algoritmos_escolhidos estiver vazio, usa todos os algoritmos disponíveis
    if not algoritmos_escolhidos:
        algoritmos_escolhidos = ['bnb', 'tatt', 'chr']

    # Filtra os algoritmos com base na escolha do usuário
    algoritmos = [
        algoritmos_disponiveis[alg]
        for alg in algoritmos_escolhidos if alg in algoritmos_disponiveis
    ]

    resultados = []
    for algoritmo_func, nome_algoritmo in algoritmos:
        if algoritmo_func == BnB.branch_and_bound and tamanho > 16:
            resultados.append({
                'nome_do_problema': nome_problema,
                'algoritmo_utilizado': nome_algoritmo,
                'quantidade_Nos': tamanho,
                'tempo_de_Execucao': 'Excedeu o limite de tempo',
                'quantidade_memoria_em_mb': 'N/A',
                'fator_aproximacao': 'N/A',
                'caminho': 'N/A',
                'peso_total': 'N/A',
                'solucao_otima': solucao_otima
            })
        else:
            resultados.append(executar_algoritmo(nome_problema, solucao_otima, grafo, tamanho, algoritmo_func, nome_algoritmo))

        print(f"{nome_problema} - {nome_algoritmo} finalizado.")

    return resultados


# Função para salvar ou adicionar resultados ao arquivo CSV
def salvar_resultados_csv(nome_arquivo, dados):
    campos = ['nome_do_problema', 'algoritmo_utilizado', 'quantidade_Nos', 'tempo_de_Execucao', 'quantidade_memoria_em_mb', 'caminho', 'peso_total', 'solucao_otima', 'fator_aproximacao']
    # Verifica se o arquivo já existe
    modo = 'a' if os.path.exists(nome_arquivo) else 'w'
    with open(nome_arquivo, mode=modo, newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        if modo == 'w':  # Se o arquivo foi criado agora, escreve o cabeçalho
            writer.writeheader()
        writer.writerows(dados)


if __name__ == "__main__":
    import os
    import sys

    caminho_problemas = 'problemas.csv'
    nome_arquivo_resultados = 'resultados_com_fator.csv'

    # Verifica se um test_case específico foi passado como parâmetro
    if len(sys.argv) > 1:
        test_case = sys.argv[1]
        solucao_otima = float(sys.argv[2])  # Segundo argumento é o valor ótimo
        algoritmos_escolhidos = sys.argv[3:]  # Algoritmos específicos fornecidos como argumentos adicionais
        problemas = [(test_case, solucao_otima)]
    else:
        # Carrega todos os problemas do arquivo CSV
        problemas = ler_problemas_csv(caminho_problemas)
        algoritmos_escolhidos = ['bnb', 'tatt', 'chr']  # Executa todos os algoritmos por padrão

    for nome_problema, solucao_otima in problemas:
        caminho_arquivo = f'test_cases/{nome_problema}.tsp'
        grafo, tamanho, _ = carregar_grafo(caminho_arquivo)

        resultados_algoritmos = executar_todos_algoritmos(nome_problema, solucao_otima, grafo, tamanho, algoritmos_escolhidos)

        # Salva os resultados interativamente, adicionando ao arquivo existente
        salvar_resultados_csv(nome_arquivo_resultados, resultados_algoritmos)
        print(f"Resultados para o problema {nome_problema} salvos no arquivo '{nome_arquivo_resultados}'.")
