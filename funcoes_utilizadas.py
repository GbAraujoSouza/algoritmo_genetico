from turtle import pos
import numpy as np
import random as rd

def crossover(cromossomo1: np.array, cromossomo2: np.array, probabilidadeCruzamento: float) -> np.array and np.array:

    # Verificar se ocorrerá o cruzamento 
    # Cria-se um numero aleatório "na" de 0 a 1.
    na = rd.random()
    # Caso o número aleatório seja maior que a probabilidade de cruzamento, ocorrerá o cruzamento
    if na < probabilidadeCruzamento:
        # Realizar cruzamento
        posAleatoria = rd.randint(1,len(cromossomo1)-1)
        
        novoCromossomo1 = np.concatenate((cromossomo1[0:posAleatoria], cromossomo2[posAleatoria:]))
        novoCromossomo2 = np.concatenate((cromossomo2[0:posAleatoria], cromossomo1[posAleatoria:]))

        return novoCromossomo1,novoCromossomo2
    else:
        # Não realizar cruzamento e retornar cromossomos originais
        return cromossomo1,cromossomo2

def mutacao(cromossomo: np.array, probabilidadeMutacao: float) -> np.array:
    # Criar "chance" de mutação 
    na = rd.random()
    if na < probabilidadeMutacao:
        # Criar posição aleatória
        posAleatoria = rd.randint(0,len(cromossomo)-1)
        # realizar mutação
        cromossomo[posAleatoria] = abs(cromossomo[posAleatoria]-1)
        return cromossomo
    else:
        return cromossomo
    
