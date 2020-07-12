import random
import time

from node import Node
from execucao import Execucao
from algoritmo import Algoritmo
from graficos import Graficos
from util import Util
from configuracao import Configuracao

class SimulatedAnnealing:
    def __init__(self, configuracao):
        self.configuracao = configuracao

        self.dadosIniciais = None
        self.dados = None

        self.problema = configuracao.problema
        self.algoritmo = Configuracao.simulated_annealing
        self.funcaoObjetivo = configuracao.funcaoObjetivo
        
        self.iteracao = 0
        self.numeroTotalIteracoes = configuracao.numeroTotalIteracoes
        self.execucoes = []

    def trocarPorVizinhoPior(self, probabilidade):        
        if probabilidade == 0:
            return False
        
        numeroAleatorio = random.uniform(0.0, 1.0)

        if numeroAleatorio <= probabilidade:
            return True

        return False

    def executar(self, dados, iteracao):
        Util.inicializarNovaExecucao(self, dados, iteracao)

        atual = Node(self.dados, self.funcaoObjetivo)

        contador = 0
        melhorValor = atual.value

        temperaturas = []
        probabilidades = []
        while contador < self.numeroTotalIteracoes:
            temperaturas.append(contador)
            probabilidade = Util.obterProbabilidade(contador, self.numeroTotalIteracoes)
            probabilidades.append(probabilidade)

            vizinho = Util.gerarVizinho(self.dados, self.configuracao)

            mantemValorAnterior = True
            if contador == 0:
                mantemValorAnterior = False

            if vizinho.value < melhorValor:
                melhorValor = vizinho.value
                
            if vizinho.value < atual.value:
                atual = vizinho
                mantemValorAnterior = False
            else:
                trocar = self.trocarPorVizinhoPior(probabilidade)
                if trocar:
                    atual = vizinho
                    mantemValorAnterior = False

            self.execucoes.append(Execucao(contador, Node(atual.state, self.funcaoObjetivo, melhorValor, mantemValorAnterior)))

            contador += 1
                
            print(f"Execução do {self.algoritmo} {contador}/{self.configuracao.numeroTotalIteracoes}", end="\r")
        
        Util.imprimirArquivoDadosCompleto(self.problema, self.configuracao.versao, self.algoritmo, self.iteracao, self.execucoes)

        Graficos.gerarGraficoFuncaoLinear(self.problema, self.configuracao.versao, temperaturas, probabilidades)

        atual.best = melhorValor

        return atual

def main():

    configuracao = Configuracao.startup()

    listaDadosIniciais = Configuracao.gerarDadosIniciais(configuracao)

    algoritmo = Algoritmo(Configuracao.simulated_annealing, SimulatedAnnealing(configuracao))

    for iteracao in range(10):
        algoritmo.executar(listaDadosIniciais[iteracao], iteracao)

    Graficos.gerarGraficoFuncaoObjetivo(algoritmo, configuracao)

if __name__ == "__main__":
    main()