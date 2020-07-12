from datetime import datetime

class Execucao(object):

    def __init__(self, iteracao, atual):        
        self.iteracao = iteracao + 1
        self.atual = atual