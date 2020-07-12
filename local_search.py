import argparse
import math
import random
import numpy
import time

from hill_climbing import HillClimbing
from hill_climbing_restart import HillClimbingRestart
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm

from graficos import Graficos
from graficos_geracao import GraficosGeracao
from resultado import Resultado
from algoritmo import Algoritmo
from execucao import Execucao
from util import Util
from configuracao import Configuracao

class LocalSearch:

    def __init__(self, configuracao):
        self.configuracao = configuracao
        self.listaDadosIniciais = []

    def executar(self):

        self.listaDadosIniciais = Configuracao.gerarDadosIniciais(self.configuracao)

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
            
            for iteracao in range(10):
                algoritmo.executar(self.listaDadosIniciais[iteracao], iteracao)

            algoritmo.gerarEstatisticas()

            Graficos.gerarGraficoFuncaoObjetivo(algoritmo, self.configuracao)            

            resultado.adicionar(algoritmo)

        inicioComparativo = time.perf_counter()

        self.finalizar(resultado)

        terminoComparativo = time.perf_counter()

        print(f"Geração da tabela/gráfico de comparativo de performance em {terminoComparativo - inicioComparativo:0.4f} segundos")

    def finalizar(self, resultado):

        GraficosGeracao.finalizar(self.configuracao, resultado)

def main():
    configuracao = Configuracao.startup()

    localSerach = LocalSearch(configuracao)

    localSerach.executar()

if __name__ == "__main__":
    main()