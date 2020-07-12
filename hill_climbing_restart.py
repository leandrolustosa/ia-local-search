import time

from node import Node
from execucao import Execucao
from algoritmo import Algoritmo
from graficos import Graficos
from util import Util
from configuracao import Configuracao

class HillClimbingRestart:
    def __init__(self, configuracao):
        self.configuracao = configuracao

        self.dadosIniciais = None
        self.dados = None

        self.problema = configuracao.problema
        self.algoritmo = Configuracao.hill_climbing_restart
        self.funcaoObjetivo = configuracao.funcaoObjetivo
        
        self.iteracao = 0
        self.numeroTotalIteracoes = configuracao.numeroTotalIteracoes
        self.execucoes = []

    def executar(self, dados, iteracao):
        Util.inicializarNovaExecucao(self, dados, iteracao)

        atual = Node(self.dados, self.funcaoObjetivo)

        contador = 0
        melhorValor = atual.value

        while contador < self.configuracao.numeroTotalIteracoes:            
            vizinho = Util.gerarVizinho(self.dados, self.configuracao, contador)
            
            mantemValorAnterior = True
            if contador == 0:
                mantemValorAnterior = False
            
            if vizinho.value < melhorValor:
                melhorValor = vizinho.value

            if vizinho.value < atual.value or ( contador + 1) % self.configuracao.gatilhoRestart == 0:
                atual = vizinho
                mantemValorAnterior = False

            self.execucoes.append(Execucao(contador, Node(atual.state, self.funcaoObjetivo, melhorValor, mantemValorAnterior)))

            contador += 1
                
            print(f"Execução do {self.algoritmo} {contador}/{self.configuracao.numeroTotalIteracoes}", end="\r")
        
        Util.imprimirArquivoDadosCompleto(self.problema, self.configuracao.versao, self.algoritmo, self.iteracao, self.execucoes)

        atual.best = melhorValor
        
        return atual

def main():

    configuracao = Configuracao.startup()

    listaDadosIniciais = Configuracao.gerarDadosIniciais(configuracao)

    algoritmo = Algoritmo(Configuracao.hill_climbing_restart, HillClimbingRestart(configuracao))

    for iteracao in range(10):
        algoritmo.executar(listaDadosIniciais[iteracao], iteracao)

    Graficos.gerarGraficoFuncaoObjetivo(algoritmo, configuracao)
    
if __name__ == "__main__":
    main()