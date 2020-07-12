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

- local_search - Classe principal que configura e executa os algoritmos, aceita um argumento obrigatório [-p|--problema] [1, 2, 3] e dois opcionais [-v|--versao] [otima (default), v1, v2, ...] e [-g|--grafico] [best, value]
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
- configuracao - Classe contendo métodos para configuração dos algoritmos, da geração de gráficos e do módulo principal LocalSearch

### Como executar
- Pré-requisitos
  - Instalar no mínimo as versões dos aplicativos listados em ambiente.
  - Instalar as dependências exigidas pelo projeto, basta digitar:
  ```
  pip install -r requirements.txt
  ```

- Problema 1
```
python local_search.py -p|--problema 1 [-v|--versao otima] [-g|--grafico best]
```
- Problema 2
```
python local_search.py -p|--problema 2 [-v|--versao otima] [-g|--grafico best]
```
- Problema 3
```
python local_search.py -p|--problema 3 [-v|--versao otima] [-g|--grafico best]
```
- Algoritmos (individualmente)
```
python hill_climbing.py -p|--problema 3 [-v|--versao otima] [-g|--grafico best]
python hill_climbing_restart.py -p|--problema 3 [-v|--versao otima] [-g|--grafico best]
python simulated_annealing.py -p|--problema 3 [-v|--versao otima] [-g|--grafico best]
python genetic_algorithm.py -p|--problema 3 [-v|--versao otima] [-g|--grafico best]
```
- Geração de gráficos (após geração dos arquivos de dados)
```
python graficos_geracao.py -p|--problema 3 [-v|--versao otima] [-g|--grafico best]
```
- Observações
  - As versões disponíveis vai de acordo com os arquivos de configuração gerados para cada problema, ou seja, pode-se copiar uma configuração pré-existente e renomear o seu sufixo, esse sufixo será o nome da versão. Ex.: Arquivo de configuração pré-existente: /dados/configuracoes/problema-1-configuracao-otima.cfg, pode-se copiar esse arquivo, e alterar o seu sufixo de "otima" para "v1", então para o problema 1, você poderá agora informar a versão v1, que ele funcionará.
  - As opções para geração de gráfico são "best" para gráficos por melhor valor e "value" para gráficos por valor atual da função objetivo.

## Relatório em Latex

- /relatorio/relatorio_final.pdf - Relatório final com as conclusões e observações sobre os algoritmos.
- /relatorio/main.tex - Arquivo principal do relatório.
- /relatorio/tex/comparativo_template.tex - Arquivo de template para a geração da página final de cada problema.
- /relatorio/tex/problema-{num}-analise.tex - Arquivo contendo a conclusão do problema e as referências das imagens.
- /relatorio/tex/problema-{num}-comparativo.tex - Arquivo gerado automaticamente pelo sistema contendo a tabela de resumo e os gráficos de performance.
- /relatorio/imagens - Pasta onde ficam armazenadas as imagens geradas pelos algoritmos e também de onde o relatório referencia as imagens

## Aplicação Web para visualização de gráficos dinâmicos em dotnet core

- /visualizador-dinamico - Pasta contendo a solução em dotnet core, para a visualização dos gráficos dinamicamente
- /visualizador-dinamico/VisualizadorDinamicoGraficos - Pasta raiz da solução web
- /visualizador-dinamico/VisualizadorDinamicoGraficos/dados - Para onde os arquivos de dados zipados, que podem ser encontrados no caminho /dados/dados.zip, deverão ser extraídos.
  - No final essa pasta deverá ficar com esse aspecto
  - /configuracoes
  - /problema-1
  - /problema-2
  - /problema-3

### Como executar

Pré-requisitos:
- Instalar o VS Code, download no link [Baixar instalador do VS Code](https://code.visualstudio.com/download)
- Instalar o .NET Core 3.1.301, download no link [Baixar instalador do .NET Core](https://dotnet.microsoft.com/download/dotnet-core/3.1)

No diretório /visualizador-dinamico, basta digitar as linhas de comando:
```
dotnet restore
dotnet run
```
Pelo VS Code, deixei configurados Launchs, tanto para o Python como para o .NET Core, clique no ícone de Run (Play com um Bug) ou pressione as teclas Ctrl+Shift+D. Selecione uma das opções e clique no botão "Play", ou pressione a tecla F5. Se quiser executar sem rodar o Debug, basta pressionar as teclas Ctrl+F5.
