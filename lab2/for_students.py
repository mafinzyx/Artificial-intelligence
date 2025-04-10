from itertools import compress
import random
import time
import matplotlib.pyplot as plt

from data import *

def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness

def roulette_wheel_selection(population, fitnesses, n_selection):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]                    # formula z instrukcji
    return random.choices(population, weights=selection_probs, k=n_selection)   # we select randomly, so the same individual may be chosen multiple times

# two parents – two children
# for each pair, the crossover point is selected randomly
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# mutation_rate should be equal to 1 / number of genes in an individual (len(items))
def mutate(individual, mutation_rate):
    return [not gene if random.random() < mutation_rate else gene for gene in individual]

items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200   
n_selection = population_size
n_elite = 2                     # always select only two best individuals
mutation_rate = 1/len(items)

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []

population = initial_population(len(items), population_size)

for _ in range(generations):
    population_history.append(population)
    
    fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]

    # Parent selection
    # individuals can be repeated
    parents = roulette_wheel_selection(population, fitnesses, n_selection)

    # Crossover and offspring generation
    offspring = []
    for i in range(0, len(parents), 2):
        if i + 1 < len(parents):
            child1, child2 = crossover(parents[i], parents[i+1])
            offspring.append(mutate(child1, mutation_rate))
            offspring.append(mutate(child2, mutation_rate))

    # Population update with elitism
    elite = sorted(population, key=lambda individual: fitness(items, knapsack_max_capacity, individual), reverse=True)[:n_elite]
    #population = elite + offspring[:population_size - n_elite]
    population = offspring[:-len(elite)] + elite

    # Update the best individual
    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
