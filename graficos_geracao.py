import math
import jsonpickle
import pandas
import time

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from hill_climbing import HillClimbing
from hill_climbing_restart import HillClimbingRestart
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm

from resultado import Resultado
from algoritmo import Algoritmo
from graficos import Graficos
from util import Util
from configuracao import Configuracao

class GraficosGeracao:
    
    def __init__(self, configuracao = None):
        self.configuracao = configuracao

    def executar(self):

        resultado = Resultado(self.configuracao.problema)

        for a in range(4):            

            algoritmo = None
            
            if (a == 0):
                algoritmo = Algoritmo(Configuracao.algoritmos[a], HillClimbing(self.configuracao))
            elif (a == 1):
                algoritmo = Algoritmo(Configuracao.algoritmos[a], HillClimbingRestart(self.configuracao))
            elif (a == 2):
                algoritmo = Algoritmo(Configuracao.algoritmos[a], SimulatedAnnealing(self.configuracao))
            else:
                algoritmo = Algoritmo(Configuracao.algoritmos[a], GeneticAlgorithm(self.configuracao))
            
            Graficos.gerarGraficoFuncaoObjetivo(algoritmo, self.configuracao)

            algoritmo.gerarEstatisticas()

            resultado.adicionar(algoritmo)

        inicioComparativo = time.perf_counter()

        GraficosGeracao.finalizar(self.configuracao, resultado)

        terminoComparativo = time.perf_counter()

        print(f"Geração da tabela/gráfico de comparativo de performance em {terminoComparativo - inicioComparativo:0.4f} segundos")

    @classmethod
    def gerarGraficoPerformance(cls, configuracao):
        
        tiposGrafico = []

        outroGrafico = "value"
        if configuracao.grafico == "value":
            outroGrafico = "best"

        tiposGrafico.append(outroGrafico)
        tiposGrafico.append(configuracao.grafico)        

        titulo = "Análise de Perfomance - " + configuracao.problema
        for grafico in tiposGrafico:
            rotulo = "{0}-performance-algoritmos-{1}".format(configuracao.problema.lower().replace(" ", "-"), grafico)
            
            caminhoImagem = "relatorio/imagens/{0}/{1}.png".format(configuracao.versao, rotulo)

            graficos = Graficos("iteração", "função objetivo", configuracao=configuracao)
            graficos.gerarGraficoPerformance(titulo, caminhoImagem, grafico)
            
            graficos = None

        return outroGrafico, rotulo, caminhoImagem

    @classmethod
    def finalizar(cls, configuracao, resultado):
        
        outroGrafico, rotulo, caminhoImagem = cls.gerarGraficoPerformance(configuracao)

        valoresTabela = str(resultado)
        textoResumo = ""
        with open("relatorio/tex/comparativo-template.tex", encoding="utf-8") as arquivo:
            textoResumo = arquivo.read()

            textoResumo = textoResumo.replace("#valores_tabela#", valoresTabela)
            textoResumo = textoResumo.replace(f"#rotulo_figura_{configuracao.grafico}#", rotulo)
            textoResumo = textoResumo.replace(f"#caminho_figura_{configuracao.grafico}#", caminhoImagem.replace("relatorio/", ""))

            textoResumo = textoResumo.replace(f"#rotulo_figura_{outroGrafico}#", rotulo.replace(configuracao.grafico, outroGrafico))
            textoResumo = textoResumo.replace(f"#caminho_figura_{outroGrafico}#", caminhoImagem.replace("relatorio/", "").replace(configuracao.grafico, outroGrafico))

        with open("relatorio/tex/{0}-comparativo.tex".format(configuracao.problema.lower().replace(" ", "-")), "w", encoding="utf-8") as arquivo:
            arquivo.write(textoResumo)

def main():
    configuracao = Configuracao.startup()

    geracao = GraficosGeracao(configuracao)

    geracao.executar()

if __name__ == "__main__":
    main()
