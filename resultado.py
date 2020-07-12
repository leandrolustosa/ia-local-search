import pandas

class Resultado:

    def __init__(self, problema):
        self.problema = problema

        self.consolidado = []        

    def adicionar(self, resultadoAlgoritmo):        
        self.consolidado.append(resultadoAlgoritmo)
    
    def __str__(self):
        resultado = ""
        for algoritmo in self.consolidado:
            resultado += str(algoritmo)
            resultado += "\n"
            resultado += "\\hline"
            resultado += "\n"
        return resultado