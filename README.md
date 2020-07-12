# Local Search
Trabalho de programação de algoritmos de local search Hill-Climbing, Hill-Climbing com Restart, Simulated Annealing e Genetic Algorithm, para o curso de mestrado do IFES campus Serra turma 2 de 2020.

# Ambiente

- Todo o trabalho foi feito em sistema operacional windows, mas com tecnologias independentes de SO
- IDE: Visual Studio Code versão 1.46.1
  - Extensões
    C#
    Python
    LaTeX Workshop
    LaTeX Utilities    
- Python versão 3.6.6
- .NET Core versão 3.1.101
- Latex compilado com MikTeX versão 2.9

# Organização

## Código fonte em Python

### Estrutura de arquivos / classes

- local_search - Classe principal que configura e executa os algoritmos, aceita um argumento --problema [1, 2, 3]
- resultado - Classe que consolida os resultados de todos os algoritmos para um determinado problema
- algoritmo - Classe que consolida as execuções de um determinado algoritmo
- execucao - Classe que contém as informações de cada execução do algoritmo, pode ser utilizada em diferentes contextos, tanto pode armazenar cada uma das 1000 iterações que são realizadas em cada execução de um algoritmo, como também pode armazenar apenas os resultados finais de cada uma das 10 iterações realizadas para cada algoritmo.
- node - Classe que representa um nó na forma de um dicionário, para cada problema terá uma configuração específica:
  - problema 1 - apenas "x" estará preenchido
  - problema 2 - apenas "x" e "y" estarão preenchidos
  - problema 3 - apenas "coordenadas" e "ordemVisitacao" estarão preenchidos
- hill_climbing - implementação do algoritmo hill-climbing
- hill_climbing_restart - implementação do algoritmo hill-climbing com restart
- simulated_annealing - implementação do algoritmo simulated annealing
- genetic_algorithm - implementação do algoritmo genetic algorithm
- util - Classe contendo métodos utilitários que são utilizados principalmente pelas implementações dos algoritmos
- configuracao - Classe contendo métodos para configuração dos algoritmos e do módulo principal LocalSearch

### Como executar

- Problema 1
```
python local_search.py [-p|--problema] 1
```
- Problema 2
```
python local_search.py [-p|--problema] 2
```
- Problema 3
```
python local_search.py [-p|--problema] 3
```

## Relatório em Latex

- /relatorio/main.tex - Arquivo principal do relatório
- /relatorio/relatorio_final.pdf - Relatório final com as conclusões e observações sobre os algoritmos
- /relatorio/imagens - Pasta onde ficam armazenadas as imagens geradas pelos algoritmos e também de onde o relatório referencia as imagens

## Aplicação Web para visualização de gráficos dinâmicos em .NET Core

- /visualizador-dinamico