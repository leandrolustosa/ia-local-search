import random
import time

from node import Node
from execucao import Execucao
from algoritmo import Algoritmo
from graficos import Graficos
from util import Util
from configuracao import Configuracao

class GeneticAlgorithm:
    def __init__(self, configuracao):
        self.configuracao = configuracao

        self.dadosIniciais = None
        self.dados = None

        self.problema = configuracao.problema
        self.algoritmo = Configuracao.genetic_algorithm
        self.funcaoObjetivo = configuracao.funcaoObjetivo

        self.limiteInferior = configuracao.limiteInferior
        self.limiteSuperior = configuracao.limiteSuperior

        self.tamanhoPopulacao = configuracao.tamanhoPopulacao
        self.probabilidadeMutacao = configuracao.probabilidadeMutacao
        
        self.iteracao = 0
        self.numeroTotalIteracoes = configuracao.numeroTotalIteracoes
        self.execucoes = []
        self.execucao = None

    def criarPopulacaoInicial(self):

        populacao = [self.dados]
        for p in range(self.tamanhoPopulacao-1):

            individuo = { "x": None, "y": None, "coordenadas": None, "ordemVisitacao": None }

            if self.dados["x"] != None:
                individuo["x"] = random.uniform(self.limiteInferior, self.limiteSuperior)

            if self.dados["y"] != None:
                individuo["y"] = random.uniform(self.limiteInferior, self.limiteSuperior)

            if self.dados["ordemVisitacao"] != None:
                individuo["coordenadas"] = self.dados["coordenadas"]
                individuo["ordemVisitacao"] = random.sample(range(1,self.limiteSuperior+1), self.limiteSuperior)

            populacao.append(individuo)

        return populacao

    def selecaoNatural(self, populacaoAnterior):
        
        i, j = Util.obterDoisNumerosInteirosDiferentes(len(populacaoAnterior)-1)

        selecao = [populacaoAnterior[i], populacaoAnterior[j]]

        individuosOrdenados = sorted(selecao, key=self.funcaoObjetivo)

        return individuosOrdenados[0]

    def obterIndividuosSelecionados(self, populacaoAnterior):
        individuo1 = self.selecaoNatural(populacaoAnterior)
        individuo2 = self.selecaoNatural(populacaoAnterior)
        while Node.iguais(individuo1, individuo2):
            individuo2 = self.selecaoNatural(populacaoAnterior)

        return individuo1, individuo2

    def criarNovaGeracao(self, populacaoAnterior):
        novaGeracao = []
        
        individuo1 = None
        individuo2 = None
        
        for iteracao in range(int(self.tamanhoPopulacao / 2)):
            individuo1, individuo2 = self.obterIndividuosSelecionados(populacaoAnterior)
            
            self.evoluir(novaGeracao, individuo1, individuo2, False)

        if self.tamanhoPopulacao % 2 == 1:
            individuo1, individuo2 = self.obterIndividuosSelecionados(populacaoAnterior)

            self.evoluir(novaGeracao, individuo1, individuo2, True)

        return novaGeracao

    def evoluir(self, populacao, individuo1, individuo2, apenasUm):
        filho1, filho2 = self.realizarCrossover(individuo1, individuo2)

        self.aplicarMutacao(filho1)
        self.aplicarMutacao(filho2)

        populacao.append(filho1)
        if apenasUm == False:
            populacao.append(filho2)

    def aplicarMutacao(self, individuo):
        numeroAleatorio = random.uniform(0.0, 1.0)

        if numeroAleatorio <= self.probabilidadeMutacao:

            if individuo["x"] != None:
                Util.gerarPerturbacao(individuo, self.configuracao, "x")

            if individuo["y"] != None:
                Util.gerarPerturbacao(individuo, self.configuracao, "y")

            if individuo["ordemVisitacao"] != None:
                Util.gerarNovaRotaComPequenaAlteracao(individuo, self.configuracao)

    def calcularMediaPonderada(self, individuo1, individuo2, filho1, filho2, propriedade):
        fator = random.uniform(0.0, 1.0)

        filho1[propriedade] = individuo1[propriedade] * fator + individuo2[propriedade] * (1 - fator)
        filho2[propriedade] = individuo2[propriedade] * fator + individuo1[propriedade] * (1 - fator)

    def permutar(self,ordemVisitacaoFilho,  ordemVisitacaoAux, indiceMargemSuperior):
        for indice in range(0, len(ordemVisitacaoAux)):
            if ordemVisitacaoAux[indice] not in ordemVisitacaoFilho:
                ordemVisitacaoFilho.append(ordemVisitacaoAux[indice])
            
        return ordemVisitacaoFilho[indiceMargemSuperior+1:len(ordemVisitacaoFilho)] + ordemVisitacaoFilho[0:indiceMargemSuperior+1]

    def realizarCrossoverOX(self, individuo1, individuo2, filho1, filho2):
        indiceCentral = int(len(self.dados["ordemVisitacao"]) / 2)
        indiceMargemInferior = int(indiceCentral / 2)
        indiceMargemSuperior = indiceCentral + indiceMargemInferior - 1

        ordemVisitacao1 = individuo1["ordemVisitacao"]
        ordemVisitacao2 = individuo2["ordemVisitacao"]

        ordemVisitacaoFilho1 = ordemVisitacao1[indiceMargemInferior:indiceMargemSuperior+1]
        ordemVisitacaoFilho2 = ordemVisitacao2[indiceMargemInferior:indiceMargemSuperior+1]

        ordemVisitacaoAux1 = ordemVisitacao1[indiceMargemSuperior+1:len(ordemVisitacao1)] + ordemVisitacao1[0:indiceMargemSuperior+1]
        ordemVisitacaoAux2 = ordemVisitacao2[indiceMargemSuperior+1:len(ordemVisitacao2)] + ordemVisitacao2[0:indiceMargemSuperior+1]
    
        filho1["ordemVisitacao"] = self.permutar(ordemVisitacaoFilho1, ordemVisitacaoAux2, indiceMargemSuperior)
        filho2["ordemVisitacao"] = self.permutar(ordemVisitacaoFilho2, ordemVisitacaoAux1, indiceMargemSuperior)

    def realizarCrossover(self, individuo1, individuo2):
        filho1 = { "x": None, "y": None, "coordenadas": self.dados["coordenadas"], "ordemVisitacao": None }
        filho2 = { "x": None, "y": None, "coordenadas": self.dados["coordenadas"], "ordemVisitacao": None }

        if "x" in individuo1 and individuo1["x"] != None and "x" in individuo2 and individuo2["x"] != None:
            self.calcularMediaPonderada(individuo1, individuo2, filho1, filho2, "x")

        if "y" in individuo1 and individuo1["y"] != None and "y" in individuo2 and individuo2["y"] != None:
            self.calcularMediaPonderada(individuo1, individuo2, filho1, filho2, "y")

        if individuo1["ordemVisitacao"] != None and individuo2["ordemVisitacao"] != None:
            self.realizarCrossoverOX(individuo1, individuo2, filho1, filho2)

        return filho1, filho2

    def executar(self, dados, iteracao):
        self.dadosIniciais = dados
        self.iteracao = iteracao
        self.execucoes = []
        self.dados = Node.copiarDados(self.dadosIniciais)
        
        populacaoInicial = self.criarPopulacaoInicial()
        atual = Node(populacaoInicial, self.funcaoObjetivo)

        contador = 0
        melhorValor = atual.value

        Util.imprimirArquivoDadosAbertura(self.problema, self.configuracao.versao, self.algoritmo, self.iteracao)

        while contador < int(self.numeroTotalIteracoes / self.tamanhoPopulacao):
            novaGeracao = self.criarNovaGeracao(atual.populacao)
            atual = Node(novaGeracao, self.funcaoObjetivo)

            if contador == 0:
                melhorValor = atual.value

            valorAnterior = Node(novaGeracao[0], self.funcaoObjetivo)
            for i in range(self.tamanhoPopulacao):                
                valorAtual = Node(novaGeracao[i], self.funcaoObjetivo)
                
                iteracao = contador*self.tamanhoPopulacao + i
                
                mantemValorAnterior = True
                if contador == 0 and i == 0:
                    mantemValorAnterior = False

                if valorAtual.value < melhorValor:
                    melhorValor = valorAtual.value

                if valorAtual.value < valorAnterior.value:
                    mantemValorAnterior = False

                self.execucao = Execucao(iteracao, Node(novaGeracao, self.funcaoObjetivo, melhorValor, mantemValorAnterior))
                self.execucao.atual.value = valorAtual.value if not mantemValorAnterior else valorAnterior.value
                self.execucao.atual.excluirPopulacao = i != 0
                    
                self.execucoes.append(self.execucao)

                valorAnterior = Node(self.execucao.atual.populacao, self.funcaoObjetivo)
                
                print(f"Execução do {self.algoritmo} {iteracao+1}/{self.configuracao.numeroTotalIteracoes}", end="\r")

            if contador > 0 and (self.numeroTotalIteracoes < 10000 or ((contador+1)*self.tamanhoPopulacao) % 10000 == 0):                
                
                execucoes = self.execucoes[:self.tamanhoPopulacao*-1]
                
                separador = ","
                if ((contador + 1) * self.tamanhoPopulacao) == self.numeroTotalIteracoes:
                    separador = ""
                    execucoes = self.execucoes[:]                    
                else:
                    self.execucoes = self.execucoes[self.tamanhoPopulacao*-1:]

                Util.imprimirArquivoDadosCompleto(self.problema, self.configuracao.versao, self.algoritmo, self.iteracao, execucoes, separador, True)
                
            contador += 1
            
        Util.imprimirArquivoDadosFechamento(self.problema, self.configuracao.versao, self.algoritmo, self.iteracao)

        return self.execucao.atual

def main():

    configuracao = Configuracao.startup()

    listaDadosIniciais = Configuracao.gerarDadosIniciais(configuracao)

    algoritmo = Algoritmo(Configuracao.genetic_algorithm, GeneticAlgorithm(configuracao))
    
    for iteracao in range(10):
        algoritmo.executar(listaDadosIniciais[iteracao], iteracao)

    Graficos.gerarGraficoFuncaoObjetivo(algoritmo, configuracao)
    
if __name__ == "__main__":
    main()