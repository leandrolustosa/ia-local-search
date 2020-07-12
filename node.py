import numpy as np

class Node:
    
    def __init__(self, state, funcaoObjetivo, best = -1, igualValorAnterior=False):
        self.igualValorAnterior = igualValorAnterior        
        self.best = best
        self.excluirPopulacao = False
        
        if type(state) is list:
            melhoresIndividuos = sorted(state, key=funcaoObjetivo)
            self.populacao = state.copy()
            self.state = Node.copiarDados(melhoresIndividuos[0])
            self.value = funcaoObjetivo(melhoresIndividuos[0])
        else:            
            self.state = Node.copiarDados(state)
            self.value = funcaoObjetivo(state)

        if best == -1:
            self.best = self.value

    def __str__(self):
        return "{{ state:{0:f}, value:{1:f} }}".format(self.state, self.value)

    def __getstate__(self):
        state = self.__dict__.copy()
        
        if not state["igualValorAnterior"]:

            Node.limparState(state["state"])

        elif state["igualValorAnterior"]:

            if "state" in state:
                del state["state"]

        Node.limparPopulacao(state)        
        del state["igualValorAnterior"]
        del state["excluirPopulacao"]
            
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def limparPopulacao(cls, state):
        if ("populacao" in state and state["excluirPopulacao"]):
            del state["populacao"]

        elif ("populacao" in state and state["populacao"] != None):
            
            for s in state["populacao"]:

                Node.limparState(s)

    @classmethod
    def limparState(cls, state):
        
        if "x" in state and state["x"] == None:
            del state["x"]

        if "y" in state and state["y"] == None:
            del state["y"]

        if "coordenadas" in state:
            del state["coordenadas"]

        if "ordemVisitacao" in state and state["ordemVisitacao"] == None:
            del state["ordemVisitacao"]

    @classmethod
    def copiarDados(cls, dados):
        aux = { "coordenadas": None, "ordemVisitacao": None }

        aux["ordemVisitacao"] = dados["ordemVisitacao"].copy() if dados["ordemVisitacao"]!=None else dados["ordemVisitacao"]

        if "x" in dados:
            aux["x"] = dados["x"]

        if "y" in dados:
            aux["y"] = dados["y"]

        if "coordenadas" in dados:
            aux["coordenadas"] = dados["coordenadas"].copy() if dados["coordenadas"]!=None else dados["coordenadas"]

        return aux

    @classmethod
    def iguais(cls, dados, outro):
        
        return (("x" not in dados or dados["x"] == outro["x"]) and 
                ("y" not in dados or dados["y"] == outro["y"]) and 
                np.array_equal(dados["ordemVisitacao"], outro["ordemVisitacao"]))