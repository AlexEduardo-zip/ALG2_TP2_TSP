import os
import csv

# Função para ler as soluções do arquivo 1solutions.txt
def read_solutions(file_path):
    solutions = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                problem, solution = line.split(':', 1)
                solutions[problem.strip()] = int(solution.strip())  # Converter para inteiro
                # print(problem.strip(), int(solution.strip()))
    return solutions

# Função para verificar se o EDGE_WEIGHT_TYPE é EUC_2D
def is_euc_2d(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('EDGE_WEIGHT_TYPE'):
                return 'EUC_2D' in line
    return False

# Diretório onde os arquivos de teste estão localizados
test_cases_dir = 'test_cases'

# Caminho para o arquivo de soluções
solutions_file = os.path.join(test_cases_dir, '1solutions.txt')

# Lê as soluções do arquivo
solutions = read_solutions(solutions_file)

# Nome do arquivo CSV de saída
output_csv = 'test_cases_solutions.csv'

# Lista para armazenar os dados dos arquivos filtrados
filtered_test_cases_data = []

# Percorre todos os arquivos no diretório de casos de teste
for filename in os.listdir(test_cases_dir):
    if filename.endswith('.tsp') and filename != '1solutions.txt':  # Considera apenas arquivos .txt, exceto o de soluções
        file_path = os.path.join(test_cases_dir, filename)
        if is_euc_2d(file_path):  # Filtra apenas arquivos com EDGE_WEIGHT_TYPE : EUC_2D
            problem_name = filename.rsplit('.', 1)[0]  # Remove a extensão do nome do arquivo
            solution = solutions.get(problem_name, 'N/A')  # Busca a solução no dicionário
            filtered_test_cases_data.append([problem_name, solution])

# Escreve os dados filtrados no arquivo CSV
with open(output_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['nome_do_problema', 'solucao'])  # Cabeçalho do CSV
    csv_writer.writerows(filtered_test_cases_data)

print(f'Dados dos casos de teste foram salvos em {output_csv}')
