# Genetic Algorithm implementation file
# Contributers: Michael Durkan

import time
from data import tasks, employees
from classes import Task, Employee, Chromosome
import fitness as f
import random
import copy
import csv

# Inputs: 
#   PoulationSize: size of population
#   maxGenerations: maximum number of generations
#   crossoverRate: rate of genetic crossover
#   mutationRate: rate of genetic mutation
#   elitism: Number of best chromosomes kept each generation
# Outputs:
#   best: best chromosome in population after algorithm finishes 
def GeneticAlgorithm(populationSize, maxGenerations, crossoverRate, mutationRate, elitism):
    # Start the timer for iteration/generation time graph
    timeStart = time.perf_counter()
    
    # Create list for graphing results
    results = []

    # Generate the inital population
    population = GenInitPop(populationSize)
    bestInIteration = GetBestIndividual(population)

    # Evaluate the fitness of the population
    f.EvaluateFitness(population)
    
    generation = 0
  
    # Sum the total Violations of all vectors in population
    feasability = sum(chromo.totalViolations for chromo in population)
    
    # Update csv for intial generation
    results.append((generation, bestInIteration.cost, 0, feasability))

    # Iterate through generations of populations
    while generation < maxGenerations:
        #and bestInIteration.cost != 0.0: (Can close early this way)
        
        # Sort the population by fitness for elitism selection
        population.sort(key=lambda c: c.fitness, reverse=True)
        
        # Create new population with slice of len elitism values at start of list
        newPopulation = [copy.deepcopy(chromo) for chromo in population[:elitism]]
        
        # Generate the new population
        while len(newPopulation) < populationSize:
            # Choose parents based on fitness, roulette wheel
            parent1 = SelectIndividual(population)
            parent2 = SelectIndividual(population)

            # Combine parents by crossover to create offspring
            if (random.random() < crossoverRate):
                offspring1, offspring2 = Crossover(parent1, parent2)
            else:
                offspring1 = copy.deepcopy(parent1)
                offspring2 = copy.deepcopy(parent2)

            # Mutate the offspring to introduce variation
            offspring1 = Mutate(offspring1, mutationRate)
            offspring2 = Mutate(offspring2, mutationRate)

            # Reset the fitness values and variables of offspring objects
            offspring1.resetValues()
            offspring2.resetValues()
            
            # Add new offspring to new population
            newPopulation.append(offspring1)
            newPopulation.append(offspring2)

        # Replace old population with new one, ensuring size stays the same
        # with odd populations
        population = newPopulation[:populationSize]

        # Evaluate fitness of population and increase generation
        f.EvaluateFitness(population)
        generation += 1

        # Save cost/feasability of best individual and time elapsed for graphing
        bestInIteration = GetBestIndividual(population)
        elapsedTime = time.perf_counter() - timeStart
        feasability = sum(chromo.totalViolations for chromo in population)
        results.append((generation, bestInIteration.cost, elapsedTime,feasability))

    # Output the generation, cost, time and feasability to csv
    with open('gaCostResults.csv', 'w', newline='') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerow(['generation', 'bestCost', 'elapsedTime', 'feasability'])
        wr.writerows(results)

    # Get the best solution from population
    best = GetBestIndividual(population)

    return best

# Name: GenInitPop
# Purpose: Generate initial population of chromosomes, with random genes 
#          representing each employee do a task per the idx of the gene in the list.
# Input: Size of Population
# Output: List of Chromosome objects with randomized genes
def GenInitPop(populationSize):
    initPop = [ Chromosome([random.randint(1,5) for _ in range(10)])
        for _ in range(populationSize) ]

    return initPop

# Name: SelectIndividual
# Purpose: Select individuals for crossover by roulette wheel selection,
#   generating random number and selecting chromosome with value the first value
#   that has cumulative prob greater than random number
# Input: Population (list) of chromosome objects
# Output: Chromosome object selected
def SelectIndividual(population):     
    roulette = random.random()
    for chromo in population:
        if roulette <= chromo.cumulativeProb:
            return chromo
    return population[-1]

# Name: Crossover
# Purpose: Create two offspring from two parents, slicing them by a random interval
#   and returning offspring that take genes from alternate slices of chromosome
# Input: Two parent chromosome objects
# Output: Two offspring chromosome objects
def Crossover(parent1, parent2):
    x = random.randint(1,8)
    offspring1 = copy.deepcopy(parent1)
    offspring2 = copy.deepcopy(parent2)
    for i in range(0,x):
        offspring1.geneList[i] = parent2.geneList[i]
        offspring2.geneList[i] = parent1.geneList[i]
    return (offspring1, offspring2)

# Name: Mutate
# Purpose: Swap the genes from two indexes of a chromosome at rate of mutation
# Input: Offspring chromosome object, and rate of mutation
# Output: Mutated offspring chromosome object
def Mutate(offspring, mutationRate):
    swaps = []
    for i, gene in enumerate(offspring.geneList):
        if random.random() < mutationRate:
            if len(swaps) < 2:
                swaps.append(i)
            if len(swaps) == 2:
                temp = offspring.geneList[i]
                offspring.geneList[i] = offspring.geneList[swaps[0]]
                offspring.geneList[swaps[0]] = temp
                swaps.clear()

    return offspring

# Name : GetBestIndividual
# Purpose: Return the highest fitness individual from population
# Input: Population, list of chromosome objects
# Output: Highest fitness chromsome object from population list
def GetBestIndividual(population):
    return max(population, key=lambda c: c.fitness)

# Allows for seperate execution of genetic algorithm
if __name__ == "__main__":
    
    # Run Genetic Algorithm
    bestSolGA = GeneticAlgorithm(60, 500, 0.77, 0.2, 0)
    print("GA Best sol:", bestSolGA.geneList)
    print("GA Best sol cost:", bestSolGA.cost) 
