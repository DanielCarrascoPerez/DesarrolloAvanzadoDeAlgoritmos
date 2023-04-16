#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

_password = "Abre. Soy yo! Quién va a ser sino?"
_pop_size = 100

def get_password_len():
    """ Return the length of the current password, for simulation purposes """
    return len(_password)

def get_fitness(guess):
    """ Return the number of caracters in guess string mismathing the same position of the password """
    return sum(1 for expected, actual in zip(_password, guess) if expected!=actual)

def gene_set(): 
    """ Return the feasible characters of the password """
    return " 0123456789áéíóúabcdefghijklmnñopqrstuvwxyzÁÉÍÓÚABCDEFGHIJKLMNÑOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>¿?@[\\]^_`{|}"

def initial_population(pop_size, chromosome_len):
    """ Create a initial population """
    x = list()
    for i in range(_pop_size):
        x.append(random.sample(gene_set(), get_password_len()))
        print(i)
    return x

def mutate(chromosome):
    """ Mutate chromosome, which is a string with the characters of the password """
    i = random.randint(0, get_password_len()-1)

    gene = random.choice(gene_set())
    while chromosome[i] == gene:
        gene = random.choice(gene_set())

    chromosome[i]=gene
    return chromosome

def crossover(chromosome1, chromosome2):
    """ Perform a one point crossover of the chormosomes """
    crossover_index = random.randrange(1, get_password_len())
    child_1 = chromosome1[:crossover_index] + chromosome2[crossover_index:]
    child_2 = chromosome2[:crossover_index] + chromosome1[crossover_index:]
    return child_1, child_2

def sort(pop):
    fitness = list()
    for i in range(_pop_size):
        argmin = i
        minimum = get_fitness(pop[i])

        for j in range(i + 1, _pop_size - 1):
            if get_fitness(pop[j]) < minimum:
                argmin = j
        pop[argmin], pop[i] = pop[i], pop[argmin]
        fitness.append(get_fitness(pop[i]))
    return pop


def ga(pop_size=100, elite_rate=0.2, mutate_prob=0.8, max_generations = 10000):
    """ Genetic Algorithm driving the search of the password """
    pwd = 0
    _pop = initial_population(_pop_size, get_password_len())
    generations = 1
    print("1a Generación creada. Mejor candidato: ", ''.join(_pop[0]))
    #ordenar por fitness
    _pop = sort(_pop)
    if (get_fitness(_pop[0])==0):
        return _pop[0]
    #Creamos nueva generación
    while (pwd==0 and generations <= max_generations):
        #selecciona la elite, 20%
        _old_gen = list(_pop)
        _pop.clear()
        j=0
        while j<20:
            _pop.append(_old_gen[j])
            j+=1
        #crear siguiente generacion, 20% mutado 80% crossover
        i=19
        while (i<_pop_size-1):
            if (((random.randrange(1, _pop_size))<20)):
                _pop.append(mutate(_old_gen[i]))
                i+=1
            elif(i<=97):
                    aux1, aux2 = crossover(_old_gen[i], _old_gen[i+1])
                    _pop.append(aux1)
                    _pop.append(aux2)
                    i+=2
        _pop = sort(_pop)
        generations+=1
        print("Generación ", generations, " creada. Mejor candidato: ", ''.join(_pop[0]))
        #comprobar si se ha encontrado el password
        for n in range(_pop_size-1):
            if (get_fitness(_pop[n])==0):
                print("Password encontrado!")
                pwd=1
        # if (get_fitness(_pop[n])==0):
        #     print("Password encontrado!")
        #     pwd=1
    return _pop[0]


    
gpassword = ga()
print(''.join(gpassword))