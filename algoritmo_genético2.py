from unicodedata import decimal
import numpy as np
import random as rd
from funcoes_utilizadas import *

tamCromossomo=8
pc=0.95
pm=0.1
numGeracoes=5
tamPopulacao=8  #Criar condição que avalia populações impares

# Passo 0: Variáveis do Problema -----------------------------------------------------------
limInferior = 0
limSuperior = 512
def func_objetivo(x: int) -> int:
    """Calcula f(x)"""
    return abs(x*np.sin(np.sqrt(abs(x))))+5

# Passo 1: Geração da população inicial - Aleatóriamente -----------------------------------
pop=np.zeros((tamPopulacao,tamCromossomo))  # MxN -> tamPopulação x tamCromossomos
for i in range(tamPopulacao):  #linhas
    a=rd.choices([0,1], k=tamCromossomo)
    for j in range(tamCromossomo):  #colunas
        pop[i][j] = a[j]

# Passo 2: Criação de variáveis do AG --------------------------------------------------------------------------------------------
def valorRealGenoma(genoma: list) -> int:
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


intervalos = np.zeros((tamPopulacao,2))
#Passo 3: Iniciar o Algoritmo Genético --------------------------------------------------------------------------------------------

for geracao in range(numGeracoes):
    # 1: Verificar se existe uma solução na população que atenda o critério de parada

    # 2: Criar proxima geração
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

    # 2.2.2: Criar lista pais com os indivíduos selecionados
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
    crossover(pais[0,:], pais[1,:], probabilidadeCruzamento=pc)


    # proximos passos: 
    # 1.Aplicar o crossover em pais (criar função crossover()) 
    # 2.Aplicar mutação depois de crossover()
        

# print(p)
# print(p[1,:])
# print(fitness)
# print(somaValores)
# print(valAleatorio)
# print(pais)
#print(intervalos)