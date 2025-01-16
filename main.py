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
    
    grafo = nx.Graph()
    for id_no, x, y in nos:
        grafo.add_node(id_no, pos=(x, y))
    
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
    memoria_inicial = processo.memory_info().rss  
    
    inicio = time.time()
    resultado = func(*args)  
    fim = time.time()

    memoria_final = processo.memory_info().rss 
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
            'peso_total': 'N/A'
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

def salvar_resultados_csv(nome_arquivo, dados):
    campos = ['nome_do_problema', 'algoritmo_utilizado', 'quantidade_Nos', 'tempo_de_Execucao', 'quantidade_memoria_em_mb', 'caminho', 'peso_total', 'solucao_otima', 'fator_aproximacao']
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

def ler_problemas_csv(caminho_arquivo):
    problemas = []
    with open(caminho_arquivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nome_problema = row['nome_do_problema']
            solucao_otima = float(row['solucao'])
            problemas.append((nome_problema, solucao_otima))
    return problemas

def executar_todos_algoritmos(nome_problema, solucao_otima, grafo, tamanho):
    algoritmos = [
        # (BnB.branch_and_bound, 'Branch and Bound'),
        (TAtT.twice_around_the_tree, 'Twice Around the Tree'),
        (Christofides.algoritmo_christofides, 'Christofides')
    ]
    
    resultados = []
    for algoritmo_func, nome_algoritmo in algoritmos:
        resultados.append(executar_algoritmo(nome_problema, solucao_otima, grafo, tamanho, algoritmo_func, nome_algoritmo))
    
    return resultados

if __name__ == "__main__":
    caminho_problemas = 'problemas.csv'
    problemas = ler_problemas_csv(caminho_problemas)
    
    resultados = []

    for nome_problema, solucao_otima in problemas:
        caminho_arquivo = f'test_cases/{nome_problema}.tsp'
        grafo, tamanho, _ = carregar_grafo(caminho_arquivo)
        
        resultados_algoritmos = executar_todos_algoritmos(nome_problema, solucao_otima, grafo, tamanho)
        resultados.extend(resultados_algoritmos)
    
    salvar_resultados_csv('resultados_com_fator.csv', resultados)

    print("\nResultados salvos no arquivo 'resultados_com_fator.csv'.")
