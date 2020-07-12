import argparse
import jsonpickle
import math
import random
import numpy as np

from util import Util

class Configuracao:

    problemas = ["Problema 1", "Problema 2", "Problema 3"]
    algoritmos = ["Hill-Climbing", "Hill-Climbing com restart", "Simulated Annealing", "Genetic Algorithm"]
    cores = ["blue", "red", "green", "orange"]
    hill_climbing = algoritmos[0]
    hill_climbing_restart = algoritmos[1]
    simulated_annealing = algoritmos[2]
    genetic_algorithm = algoritmos[3]

    @classmethod
    def funcaoObjetivo1(cls, dados):
        return pow(dados["x"], 2) / 100 + 10*math.sin(dados["x"] - math.pi/2)

    @classmethod
    def funcaoObjetivo2(cls, dados):
        return 20 + (pow(dados["x"], 2) - 10 * math.cos(2 * math.pi * dados["x"])) + (pow(dados["y"], 2) - 10 * math.cos(2 * math.pi * dados["y"]))

    @classmethod
    def funcaoObjetivo3(cls, dados):
        if dados["coordenadas"] == None or dados["ordemVisitacao"] == None:
            return 0

        distancias = [] 
        
        for i in range(1, len(dados["ordemVisitacao"])+2):
            distancias.append(Util.calcularDistanciaEntreDoisPontos(dados, i))
        
        return sum(distancias)

    @classmethod
    def gerarDadosIniciais(cls, configuracao):
        
        dadosIniciais = []
        if configuracao.codigoProblema == 1:
            with open("dados/configuracoes/{0}-inicializacao.cfg".format(configuracao.problema.lower().replace(" ", "-")), "r") as arquivo:
                for linha in arquivo:
                    dados = { "x": float(linha), "y": None, "coordenadas": None, "ordemVisitacao": None }
                    dadosIniciais.append(dados)
                    print("f({0:f}) = {1:f}".format(dados["x"], configuracao.funcaoObjetivo(dados)))

        elif configuracao.codigoProblema == 2:
            with open("dados/configuracoes/{0}-inicializacao.cfg".format(configuracao.problema.lower().replace(" ", "-")), "r") as arquivo:
                for linha in arquivo:
                    ponto = linha.split(" ")
                    dados = { "x": float(ponto[0]), "y": float(ponto[1]), "coordenadas": None, "ordemVisitacao": None }                    
                    dadosIniciais.append(dados)
                    print("f({0:f},{1:f}) = {2:f}".format(dados["x"], dados["y"], configuracao.funcaoObjetivo(dados)))
            
        elif configuracao.codigoProblema == 3:
            coordenadas = Util.carregarCidades(configuracao.arquivoCidades)
            for visita in range(10):
                if visita == 0:
                    np.random.seed(1)
                    solucaoInicial = np.random.permutation(range(1, configuracao.limiteSuperior + 1))

                    dados = { "x": None, "y": None, "coordenadas": coordenadas.copy(), "ordemVisitacao": solucaoInicial.tolist() }
                elif visita != 0:
                    seed_for_rerandomization = np.random.randint(0, 1e6)                    
                    np.random.seed(seed_for_rerandomization)
                    solucaoAleatoria = np.random.permutation(range(1, configuracao.limiteSuperior + 1))

                    dados = { "x": None, "y": None, "coordenadas": coordenadas.copy(), "ordemVisitacao": solucaoAleatoria.tolist() }
                    
                dadosIniciais.append(dados)
                print("f(d) = {0:f}".format(configuracao.funcaoObjetivo(dados)))

            print("")

        return dadosIniciais

    @classmethod
    def startup(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--problema", dest="problema", type=int, required=True, help="Informe o problema [1, 2 ou 3]")
        parser.add_argument("-v", "--versao", dest="versao", type=str, required=False, default="otima", help="Informe a versão da configuração (opcional) ex.: v1, v2, etc")
        parser.add_argument("-g", "--grafico", dest="grafico", type=str, required=False, default="best", help="Informe o tipo de gráfico a ser gerado (opcional) ex.: best, value")

        args = parser.parse_args()

        problema = Configuracao.problemas[args.problema-1]
        print("Problema escolhido " + problema)
        print("")

        configuracao = Util.carregarConfiguracao(problema, args.versao, args.grafico)

        if configuracao.codigoProblema == 1:
            configuracao.funcaoObjetivo = Configuracao.funcaoObjetivo1

        elif configuracao.codigoProblema == 2:
            configuracao.funcaoObjetivo = Configuracao.funcaoObjetivo2

        elif configuracao.codigoProblema == 3:
            configuracao.funcaoObjetivo = Configuracao.funcaoObjetivo3

        return configuracao

    def __init__(self):
        
        self.dadosIniciais = None
        self.dados = None
        
        self.codigoProblema = 1
        self.problema = "problema-1"
        self.algoritmo = "hill-climbing"

        self.limiteInferior = -100
        self.limiteSuperior = 100

        self.gatilhoRestart = 50
        self.tamanhoPopulacao = 20
        self.probabilidadeMutacao = 0.3
        
        self.iteracao = 0
        self.numeroTotalIteracoes = 1000

        self.funcaoObjetivo = None