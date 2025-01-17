# Comparador de Algoritmos para o Problema do Caixeiro Viajante (TSP)

Este projeto implementa e compara algoritmos para resolver o **Problema do Caixeiro Viajante (TSP)**, incluindo:
- **Branch-and-Bound (BnB)**
- **Twice Around the Tree (TATT)**
- **Christofides (CHR)**

O objetivo é calcular soluções aproximadas para o TSP, avaliar seu desempenho em termos de tempo de execução, consumo de memória e fator de aproximação, e armazenar os resultados em arquivos CSV para análise.

---

## Tecnologias Usadas

- **Python 3.8+**
- **Bibliotecas**:
  - `networkx` - Manipulação de grafos.
  - `numpy` - Manipulação de arrays e cálculo de distâncias.
  - `pandas` - Manipulação de dados em CSV.
  - `os` e `sys` - Interação com o sistema operacional.
  - `csv` - Leitura e gravação de arquivos CSV.

---

## Estrutura do Projeto

```plaintext
.
├── main.py                 # Código principal do projeto
├── problemas.csv           # Arquivo com problemas de entrada (instâncias do TSP)
├── test_cases/             # Diretório com arquivos .tsp representando os problemas
├── resultados_com_fator.csv # Arquivo de saída com resultados
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo

Instalação e Configuração

Clone o repositório:

git clone https://github.com/seu-usuario/tsp-comparador.git
cd tsp-comparador
Crie e ative um ambiente virtual (opcional, mas recomendado):

python3 -m venv venv
source venv/bin/activate   # No Windows: venv\Scripts\activate
Instale as dependências:

pip install -r requirements.txt
Prepare os problemas:

Adicione instâncias TSP no diretório test_cases/ no formato .tsp.
Atualize o arquivo problemas.csv com o formato:

nome_problema,solucao_otima
exemplo1,1234.5
exemplo2,5678.9

Como Usar
Executar com o Arquivo problemas.csv

python main.py

O código lê os problemas listados no arquivo problemas.csv, executa os algoritmos selecionados (por padrão, bnb, tatt e chr), e salva os resultados no arquivo resultados_com_fator.csv.

Executar com um Caso de Teste Específico

python main.py exemplo1 1234.5 bnb tatt

Substitua exemplo1 pelo nome do problema (sem extensão .tsp), 1234.5 pela solução ótima, e informe os algoritmos desejados (bnb, tatt, chr).

Saída
Os resultados serão salvos no arquivo resultados_com_fator.csv no formato:

nome_problema,algoritmo,tempo_execucao,memoria_usada,fator_aproximacao