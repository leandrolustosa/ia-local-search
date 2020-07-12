
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np  
import jsonpickle

from configuracao import Configuracao

sns.set(style="darkgrid")

def gen_performance_curve(problema, versao, algoritmo, numeroTotalIteracoes):
    lista = []

    for i in range(10):
        with open("dados/{0}/{1}/{2}-{3}.dat".format(problema.lower().replace(" ", "-"), versao, algoritmo.lower().replace(" ", "-"), str(i))) as arquivo:
            execucoes = jsonpickle.decode(arquivo.read())
            
            lista.append(list(map(lambda x: x.atual.best, execucoes)))            
    
    matriz = np.array(lista)
    # matriz = ndarray.reshape(1000,10)
    print("shift.shape:", matriz.shape)
    return matriz

def plot_performance(n_calls, mat_10_x_1000, color):
    mean = np.mean(mat_10_x_1000, axis=0)
    std = np.std(mat_10_x_1000, axis=0)
    plt.plot(n_calls, mean) 
    plt.plot(n_calls, mean-std, color=color, alpha=0.2, linewidth=0.7) 
    plt.plot(n_calls, mean+std, color=color, alpha=0.2, linewidth=0.7) 
    plt.fill_between(n_calls, mean-std, mean+std, alpha=0.1, facecolor=color)


hill_climbing = gen_performance_curve("Problema 1", "otima", "Hill-Climbing", 1000)
hill_climbing_restart = gen_performance_curve("Problema 1", "otima", "Hill-Climbing com restart", 1000)

n_obj_function_calls = range(1000)
plot_performance(n_obj_function_calls, hill_climbing, 'blue')
plot_performance(n_obj_function_calls, hill_climbing_restart, 'red')
plt.legend(['hill_climbing', 'hill_climbing_restart'])
plt.show()