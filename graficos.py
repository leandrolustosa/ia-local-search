import math
import jsonpickle
import pandas
import time

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from execucao import Execucao
from util import Util
from configuracao import Configuracao

class Graficos:
    
    def __init__(self, xlabel, ylabel, algoritmo = None, configuracao = None):
        self.title = algoritmo
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.algoritmo = algoritmo
        self.configuracao = configuracao

    def gerar(self, algoritmo):

        plt.figure(figsize=(8,5), dpi=100)
        plt.title(self.title)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)

        if self.configuracao.codigoProblema == 1:
            plt.ylim(-15, 110)
        elif self.configuracao.codigoProblema == 2:
            plt.ylim(-5, 80)
            if algoritmo.nome == Configuracao.simulated_annealing:
                plt.ylim(-5, 350)
        else:
            plt.ylim(16000, 34000)

        for i in range(10):
            with open("dados/{0}/{1}/{2}-{3}.dat".format(self.configuracao.problema.lower().replace(" ", "-"), self.configuracao.versao, self.algoritmo.lower().replace(" ", "-"), str(i))) as arquivo:
                execucoes = jsonpickle.decode(arquivo.read())

                if algoritmo.execucoes != None:
                    algoritmo.adicionarExecucao(Execucao(i, execucoes[-1].atual))
                
                x = np.array(list(map(lambda x: x.iteracao, execucoes)))                            
                y = np.array(list(map(lambda x: getattr(x.atual, self.configuracao.grafico), execucoes)))

                plt.plot(x, y, '-')
        
        nomeArquivo = "relatorio/imagens/{0}/{1}-{2}-funcao-objetivo-{3}.png".format(self.configuracao.versao, self.configuracao.problema.lower().replace(" ", "-"), self.algoritmo.lower().replace(" ", "-"), self.configuracao.grafico)
        Util.criarDiretorioSeNaoExiste(nomeArquivo)
        plt.savefig(nomeArquivo)

    def gerarGraficoPerformanceSeaborn(self, titulo, caminhoImagem):
        plt.figure(figsize=(8,5), dpi=100)
        plt.title(titulo)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)

        if self.configuracao.codigoProblema == 1:
            plt.ylim(-20, 80)
        elif self.configuracao.codigoProblema == 2:
            plt.ylim(-20, 150)
        else:
            plt.ylim(16000, 34000)

        dicionario = {
            "iteracao": []
        }

        for algoritmo in Configuracao.algoritmos:
            dicionario[algoritmo] = []
        
            for i in range(10):
                with open("dados/{0}/{1}/{2}-{3}.dat".format(self.configuracao.problema.lower().replace(" ", "-"), self.configuracao.versao, algoritmo.lower().replace(" ", "-"), str(i))) as arquivo:
                    execucoes = jsonpickle.decode(arquivo.read())
                    
                    if Configuracao.algoritmos.index(algoritmo) == 0:
                        dicionario["iteracao"].extend(list(map(lambda x: x.iteracao, execucoes)))

                    dicionario[algoritmo].extend(list(map(lambda x: getattr(x.atual, self.configuracao.grafico), execucoes)))
            
        dados = pandas.DataFrame(dicionario)

        sns.set(style="darkgrid")
        sns.lineplot(x="iteracao", y="value", hue="variable", legend="brief", data=pandas.melt(dados, ["iteracao"]))

        Util.criarDiretorioSeNaoExiste(caminhoImagem)
        plt.savefig(caminhoImagem)

    def gen_performance_curve(self, algoritmo):
        lista = []

        for i in range(10):
            with open("dados/{0}/{1}/{2}-{3}.dat".format(self.configuracao.problema.lower().replace(" ", "-"), self.configuracao.versao, algoritmo.lower().replace(" ", "-"), str(i))) as arquivo:
                execucoes = jsonpickle.decode(arquivo.read())
                
                lista.append(list(map(lambda x: getattr(x.atual, self.configuracao.grafico), execucoes)))            
    
        matriz = np.array(lista)
        
        return matriz

    def plot_performance(self, n_calls, mat_10_x_1000, color):
        
        mean = np.mean(mat_10_x_1000, axis=0)
        std = np.std(mat_10_x_1000, axis=0)
        plt.plot(n_calls, mean, color=color)
        plt.fill_between(n_calls, mean-std, mean+std, alpha=0.1, facecolor=color)

    def gerarGraficoPerformance(self, titulo, caminhoImagem):

        plt.figure(figsize=(8,5), dpi=100)
        plt.title(titulo)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)

        if self.configuracao.codigoProblema == 1:
            plt.ylim(-20, 90)
        elif self.configuracao.codigoProblema == 2:
            plt.ylim(-20, 150)
        else:
            plt.ylim(16000, 34000)
        
        n_obj_function_calls = range(self.configuracao.numeroTotalIteracoes)
        for indice in range(4):

            algoritmo = self.gen_performance_curve(Configuracao.algoritmos[indice])
            
            self.plot_performance(n_obj_function_calls, algoritmo, Configuracao.cores[indice])
            
        plt.legend(Configuracao.algoritmos)

        Util.criarDiretorioSeNaoExiste(caminhoImagem)
        plt.savefig(caminhoImagem)


    @classmethod
    def gerarGraficoFuncaoObjetivo(cls, algoritmo, configuracao):
        inicioGraficos = time.perf_counter()

        graficos = Graficos("iteração", "função objetivo", algoritmo.nome, configuracao)
        graficos.gerar(algoritmo)

        graficos = None

        terminoGraficos = time.perf_counter()

        print(f"Geração do gráfico do {algoritmo.nome} da função objetivo em {terminoGraficos - inicioGraficos:0.4f} segundos")
        print("")

    @classmethod
    def gerarGraficoFuncaoLinear(cls, problema, versao, temperaturas, probabilidades):

        plt.figure(figsize=(8,5), dpi=100)
        plt.title("Teste função linear")
        plt.ylabel("Probabilidade")
        plt.xlabel("Temperatura")

        x = temperaturas
        y = probabilidades

        plt.plot(x, y, '-')
        
        plt.savefig("relatorio/imagens/{0}/{1}-teste-funcao-linear.png".format(versao, problema.lower().replace(" ", "-")))
