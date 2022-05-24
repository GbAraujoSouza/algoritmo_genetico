import numpy as np
import random as rd
import matplotlib.pyplot as plt
from funcoes_utilizadas import *

tamCromossomo=10
pc=0.95
pm=0.1
numGeracoes=100
tamPopulacao=200

# Passo 0: Variáveis do Problema -----------------------------------------------------------
limInferior = 0
limSuperior = 512
def func_objetivo(x: float) -> float:
    """Calcula f(x)"""
    return abs(x*np.sin(np.sqrt(abs(x))))+5

# Passo 1: Geração da população inicial - Aleatóriamente -----------------------------------
pop=np.zeros((tamPopulacao,tamCromossomo))  # MxN -> tamPopulação x tamCromossomos
for i in range(tamPopulacao):  #linhas
    a=rd.choices([0,1], k=tamCromossomo)
    for j in range(tamCromossomo):  #colunas
        pop[i][j] = a[j]

intervalos = np.zeros((tamPopulacao,2))
solucoes = np.zeros(numGeracoes)
melhorX = 0

# Passo 2: Criação de variáveis do AG --------------------------------------------------------------------------------------------
def valorRealGenoma(genoma: list) -> float:
    "Lê um genoma (número binário no formato de lista -> Ex.: [0,1,0,0,0,1]) e retorna o valor real correspondente"
    valorReal=0
    for i in range(len(genoma)):
        valorReal += genoma[i] * 2**(len(genoma) - (i+1))
    return limInferior+((limSuperior-limInferior)/((2**tamCromossomo)-1))*valorReal

def verifica_intervalo(inferior: float,superior: float, x: float) -> bool:
    """Verifica se um valor x está em [inferior ,superior["""
    if inferior <= x < superior:
        return True
    else:
        return False

# def fitness(genoma: list):
#     return func_objetivo(valorRealGenoma(genoma))

#Passo 3: Iniciar o Algoritmo Genético --------------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(111)

for geracao in range(numGeracoes):
    # 1: Verificar se existe uma solução na população que atenda o critério de parada

    solucoes[geracao] = func_objetivo(valorRealGenoma(pop[0]))
    melhorX = valorRealGenoma(pop[0])
    for individuo in range(tamPopulacao):
        if func_objetivo(valorRealGenoma(pop[individuo])) > solucoes[geracao]:
            solucoes[geracao] = func_objetivo(valorRealGenoma(pop[individuo]))
            melhorX = valorRealGenoma(pop[individuo])

    # 2: Criar proxima geração ----------------------------------------------------------------------------------------------------
    # 2.1: criar roleta de aptidão (fitness)
    # 2.1.1: Soma de valores reais da população
    somaValores = 0
    for individuo in range(tamPopulacao):
        somaValores += func_objetivo(valorRealGenoma(pop[individuo,:]))
    
    # 2.1.2: Geração dos intervalos
        intervalo_i = 0
        intervalo_s = 0
    for individuo in range(tamPopulacao):

        intervalo_i = intervalo_s
        intervalo_s = func_objetivo(valorRealGenoma(pop[individuo,:]))/somaValores + intervalo_i
        intervalos[individuo,0] = intervalo_i
        intervalos[individuo,1] = intervalo_s
    # 2.2: Seleção dos pais (individuos mais adaptados) para o cruzamento
    # 2.2.1: Geração de valores aleatórios de 0 a 1
    valAleatorio = [rd.uniform(0,1) for x in range(tamPopulacao)]
    pais = np.zeros((tamPopulacao,tamCromossomo))

    # 2.2.2: Criar matriz "pais" com os indivíduos selecionados
    for valor in range(len(valAleatorio)):  # len(intervalos == quantidade de intervalos)

        for intervalo in range(len(intervalos)):

            if (intervalos[intervalo,1] == 1.0):
                intervalos[intervalo,1] +=0.1

            if (verifica_intervalo(inferior = intervalos[intervalo,0], superior = intervalos[intervalo,1], x = valAleatorio[valor])):
            
                pais[valor,:] = (pop[intervalo,:])
                break
            else: 
                continue
    
    # 2.3: Realizar cruzamento (crossover) nos cromossomos pais selecionados
    filhos = np.zeros((tamPopulacao,tamCromossomo))
    # iterar de dois em dois
    for i in range(len(pais)):
        if i % 2 == 0: # par
            if i==(len(pais)-1): # Ultimo elemento
                # Em caso do numero de individuos ser impar
                # retornar por ultimo apenas um indivíduo
                filhos[i] = pais[i]
            else:
                filhos[i],filhos[i+1] = crossover(pais[i,:], pais[i+1,:], probabilidadeCruzamento=pc)
        else: # impar
            continue

    # 2.4 Realizar mutação
    for individuo in range(len(filhos)):
        filhos[individuo] = mutacao(filhos[individuo], probabilidadeMutacao=pm)

    # fim da criação da nova geração 
    pop = filhos

    # Plotar resultado atual
    x = np.linspace(limInferior,limSuperior,100)
    plt.xlim(300,550)
    plt.ylim(0,500)
    ax.scatter(melhorX,solucoes[geracao])
    plt.xlim(300,550)
    plt.ylim(0,500)
    ax.plot(x, func_objetivo(x))
    plt.pause(0.001)
        

# print(p)
# print(p[1,:])
# print(fitness)
# print(somaValores)
# print(valAleatorio)
# print(pais)
# print()
# print(filhos)
# print(intervalos)
print()
print(max(solucoes),"\n")

# import matplotlib.pyplot as plt
v = np.linspace(limInferior,limSuperior,100000)
# plt.plot(x,func_objetivo(x))
# plt.show()
# plt.close()
verdade = []
print("max:\n",max(func_objetivo(v)))
