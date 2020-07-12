import statistics
import time

from execucao import Execucao

class Algoritmo:

    def __init__(self, nome, estrategia):
        self.estrategia = estrategia

        self.nome = nome
        self.execucoes = []
        self.min = 0.0
        self.max = 0.0
        self.media = 0.0
        self.desvioPadrao = 0.0

    def executar(self, dados, iteracao):
        inicio = time.perf_counter()

        estadoFinal = self.estrategia.executar(dados, iteracao)

        self.adicionarExecucao(Execucao(iteracao, estadoFinal))

        self.estrategia.execucoes = None
        
        termino = time.perf_counter()
        
        print(f"Execução do {self.nome} com valor final de {estadoFinal.best} iteração {iteracao} em {termino - inicio:0.4f} segundos", end="\r")
        print("")
    
    def gerarEstatisticas(self):
        valores = list(map(lambda x: x.atual.best, self.execucoes))

        if len(valores) > 0:
            self.min = round(min(valores), 3)
            self.max = round(max(valores), 3)
            self.media = round(sum(valores) / len(valores), 3)
            self.desvioPadrao = round(statistics.stdev(valores), 3)

        self.execucoes = None

    def adicionarExecucao(self, execucao):
        self.execucoes.append(execucao)
    
    def __str__(self):
        return f"{self.nome} & {self.max} & {self.min} & {self.media} & {self.desvioPadrao} \\\\"
    