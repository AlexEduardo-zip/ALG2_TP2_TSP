import csv
import subprocess

def executar_testes(arquivo_csv, script_programa, algoritmos):
    try:
        # Abrir o arquivo CSV e carregar os problemas
        with open(arquivo_csv, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular o cabeçalho, se houver
            
            # Iterar sobre os problemas no CSV
            for linha in reader:
                if len(linha) < 2:
                    print(f"Linha inválida no CSV: {linha}")
                    continue

                nome_do_problema, valor_otimo = linha[:2]

                # Rodar o programa para cada algoritmo
                for algoritmo in algoritmos:
                    print(f"Executando: {nome_do_problema}, Algoritmo: {algoritmo}")

                    # Comando para executar o script com os argumentos
                    comando = [
                        "python", script_programa, 
                        nome_do_problema, valor_otimo, algoritmo
                    ]

                    # Rodar o programa e capturar saída e erros
                    processo = subprocess.run(
                        comando, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        text=True
                    )

                    # Exibir a saída do programa
                    print(f"Saída do programa:\n{processo.stdout}")
                    if processo.stderr:
                        print(f"Erros:\n{processo.stderr}")

    except FileNotFoundError:
        print(f"Arquivo {arquivo_csv} não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # Arquivo CSV contendo os problemas
    arquivo_csv = "problemas.csv"

    # Nome do programa principal que você deseja executar
    script_programa = "main.py"

    # Algoritmos disponíveis
    algoritmos = ["bnb", "tatt", "chr"]

    # Executar os testes
    executar_testes(arquivo_csv, script_programa, algoritmos)
