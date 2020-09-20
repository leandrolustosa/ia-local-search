import os
import errno

import math
import numpy
import random
import jsonpickle

from node import Node

class Util:

    @classmethod
    def obterProbabilidade(cls, iteracao, numeroTotalIteracoes):
        if iteracao >= int(numeroTotalIteracoes*0.9):
            return 0.0

        fator = -1/int(numeroTotalIteracoes*0.9)

        # função linear => f(x) = mx + b
        return iteracao * fator + 1

    @classmethod
    def carregarConfiguracao(cls, problema, versao="otima", grafico="best"):

        config = None

        with open("dados/configuracoes/{0}-configuracao-{1}.cfg".format(problema.lower().replace(" ", "-"), versao) , "r") as arquivo:
            config = jsonpickle.decode(arquivo.read())

        config.versao = versao
        config.grafico = grafico

        return config

    @classmethod
    def carregarCidades(cls, arquivoCidades):

        coordenadas = []

        with open(arquivoCidades, "r") as arquivo:
            for linha in arquivo:
                ponto = linha.split(" ")
                x = float(ponto[0])
                y = float(ponto[1])
                coordenadas.append((x, y))

        return coordenadas

    @classmethod
    def gerarPerturbacao(cls, dados, configuracao, propriedade, contador=-1):
        valorDistNormal = numpy.random.normal(0.0, 2.0)
        dados[propriedade] += valorDistNormal

        if contador != -1 and (contador + 1) % configuracao.gatilhoRestart == 0:
            dados[propriedade] = numpy.random.randint(configuracao.limiteInferior, configuracao.limiteSuperior)
            
        if dados[propriedade] < configuracao.limiteInferior or dados[propriedade] > configuracao.limiteSuperior:
            dados[propriedade] += valorDistNormal*2*-1

    @classmethod
    def novoVizinho(cls, dados, configuracao, contador=-1):
        if dados["x"] != None:
            cls.gerarPerturbacao(dados, configuracao, "x", contador)

        if dados["y"] != None:
            cls.gerarPerturbacao(dados, configuracao, "y", contador)
        
        return Node(dados, configuracao.funcaoObjetivo)

    @classmethod
    def gerarVizinho(cls, dados, configuracao, contador=-1):
        vizinho = None
        if dados["x"] != None:
            vizinho = cls.novoVizinho(dados, configuracao, contador)
        else:
            vizinho = cls.gerarNovaRotaComPequenaAlteracao(dados, configuracao, contador)
        return vizinho

    @classmethod
    def gerarNovaRotaComPequenaAlteracaoRestart(cls, dados, configuracao, contador):
        if contador == -1:
            return None

        numeroCidades = len(dados["coordenadas"])

        novosDados = Node.copiarDados(dados)
        
        if ((contador + 1) % configuracao.gatilhoRestart == 0):
            
            novosDados["ordemVisitacao"] = random.sample(range(1,numeroCidades), numeroCidades-1)
            
            return Node(novosDados, configuracao.funcaoObjetivo)

        return None

    @classmethod
    def gerarNovaRotaComPequenaAlteracao(cls, dados, configuracao, contador=-1):
        restart = cls.gerarNovaRotaComPequenaAlteracaoRestart(dados, configuracao, contador)            
        if restart != None:
            return restart

        novosDados = Node.copiarDados(dados)

        cls.aplicarPequenaAlteracao(configuracao, dados, novosDados)
        
        return Node(novosDados, configuracao.funcaoObjetivo)

    @classmethod
    def aplicarPequenaAlteracao(cls, configuracao, dados, novosDados):
        iteracoes = 1

        for iteracao in range(iteracoes):
            i, j = cls.obterDoisNumerosInteirosDiferentes(len(dados["ordemVisitacao"])-1)
            
            if configuracao.problema == 3:
                dados["ordemVisitacao"][i], dados["ordemVisitacao"][j] = dados["ordemVisitacao"][j], dados["ordemVisitacao"][i]
            else:
                novosDados["ordemVisitacao"][i], novosDados["ordemVisitacao"][j] = dados["ordemVisitacao"][j], dados["ordemVisitacao"][i]

    @classmethod
    def obterDoisNumerosInteirosDiferentes(cls, limiteSuperior):
        i = random.randint(0, limiteSuperior)
        j = random.randint(0, limiteSuperior)
        while j==i:
            j = random.randint(0, limiteSuperior)

        return i, j

    @classmethod
    def inicializarNovaExecucao(cls, instance, dados, iteracao):
        instance.dadosIniciais = dados
        instance.iteracao = iteracao
        instance.execucoes = []
        instance.dados = Node.copiarDados(instance.dadosIniciais)

    @classmethod
    def criarDiretorioSeNaoExiste(cls, nomeArquivo):
        if not os.path.exists(os.path.dirname(nomeArquivo)):
            try:
                os.makedirs(os.path.dirname(nomeArquivo))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    @classmethod
    def imprimirArquivoDadosAbertura(cls, problema, versao, algoritmo, iteracao):
        nomeArquivo = "dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, "w") as arquivo:
            arquivo.write("[")

        nomeArquivo = "visualizador-dinamico/VisualizadorDinamicoGraficos/dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, "w") as arquivo:
            arquivo.write("[")

    @classmethod
    def imprimirArquivoDados(cls, problema, versao, algoritmo, iteracao, execucao, sinal):
        textoJson = jsonpickle.encode(execucao, make_refs=False) + sinal

        nomeArquivo = "dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, "a") as arquivo:
            arquivo.write(textoJson)

        nomeArquivo = "visualizador-dinamico/VisualizadorDinamicoGraficos/dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, "a") as arquivo:
            arquivo.write(textoJson)

    @classmethod
    def imprimirArquivoDadosFechamento(cls, problema, versao, algoritmo, iteracao):
        nomeArquivo = "dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, "a") as arquivo:
            arquivo.write("]")

        nomeArquivo = "visualizador-dinamico/VisualizadorDinamicoGraficos/dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, "a") as arquivo:
            arquivo.write("]")

    @classmethod
    def imprimirArquivoDadosCompleto(cls, problema, versao, algoritmo, iteracao, execucoes, separador = "", somenteObjetos=False):
        textoJson = jsonpickle.encode(execucoes, make_refs=False)
        modoEscrita = "w"
        if somenteObjetos:
            textoJson = textoJson[1:-1] + separador
            modoEscrita = "a"

        nomeArquivo = "dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, modoEscrita) as arquivo:
            arquivo.write(textoJson)

        nomeArquivo = "visualizador-dinamico/VisualizadorDinamicoGraficos/dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(iteracao))
        cls.criarDiretorioSeNaoExiste(nomeArquivo)
        with open(nomeArquivo, modoEscrita) as arquivo:
            arquivo.write(textoJson)

    @classmethod
    def calcularDistanciaEntreDoisPontos(cls, dados, indice):
        dadosVisitacao = dados["ordemVisitacao"].copy()
        dadosVisitacao.insert(0, 0)
        dadosVisitacao.append(0)

        i1 = dadosVisitacao[indice-1]
        i2 = dadosVisitacao[indice]

        p1 = dados["coordenadas"][i1]
        p2 = dados["coordenadas"][i2]
        
        return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))