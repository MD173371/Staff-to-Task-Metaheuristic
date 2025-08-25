# Particle Swarm implementation file
# Contributers: Michael Durkan + Alexander Carey
# brief:implementation of a PSO to create a swarm that solves an assignment task

import time
import csv
import random
import numpy as np
from classes import Chromosome
from fitness import EvaluateFitness

# Inputs:
#       numTasks: number of tasks to assign
#       numEmployee: number of employees
#       numParticles: number of particles
#       maxiter: number of iterations to run
#       w: inertia
#       c1: cognitive coefficent
#       c2: Social coefficient 
# Outputs:
#       GlobalBestPosition: best assignment of tasks to employees
#       GlobalBestCost:     total cost of best solution
def pso(numTasks, numEmployee, numParticles=90, maxIter=500, w=0.95, c1=1.5, c2=1.3):
    startTime = time.perf_counter()#track time for data collection
    results = []
    #intialise a swarm
    swarm = [Particle(numTasks, numEmployee) for _ in range(numParticles)]
    #find global best given the lowest cost
    globalBest = min(swarm, key=lambda p: p.cost)
    globalBestPosition = globalBest.position[:]
    globalBestCost = globalBest.cost

    for iteration in range(1, maxIter + 1):
        for p in swarm:
            #random factors for c1 and c2
            r1 = np.random.rand(numTasks)
            r2 = np.random.rand(numTasks)

            # Update velocity given inertia, c1 and c2
            p.velocity = [
                w * v +
                c1 * r1[i] * (p.bestPosition[i] - p.position[i]) +
                c2 * r2[i] * (globalBestPosition[i] - p.position[i])
                for i, v in enumerate(p.velocity)
            ]

            # apply the velocy and rounde to an employee
            p.position = [
                int(np.clip(round(p.position[i] + p.velocity[i]), 1, numEmployee))
                for i in range(numTasks)
            ]

            # Evaluate new position
            particleWrapper = Chromosome(p.position[:])
            EvaluateFitness([particleWrapper])
            p.violation = particleWrapper.totalViolations

            # Update if personal best is better
            if particleWrapper.fitness > p.bestFitness:
                p.bestPosition = p.position[:]
                p.bestFitness = particleWrapper.fitness
                p.cost = particleWrapper.cost

                # Update global best if personal best is better
                if particleWrapper.cost < globalBestCost:
                    globalBestPosition = p.position[:]
                    globalBestCost = particleWrapper.cost
        # timings for data collection
        elapsed = time.perf_counter() - startTime
        totalViolations = sum(particle.violation for particle in swarm)
        results.append([iteration, globalBestCost, elapsed, totalViolations])
    # writing to file gor graph
    with open('psoCostResults.csv', 'w', newline='') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerow(['generation', 'bestCost', 'elapsedTime', 'feasability'])
        wr.writerows(results)

    return globalBestPosition, globalBestCost

#Particle class, 
#Import number of tasks and number of employees
class Particle:
    def __init__(self, numTasks, numEmployee):
        #randomly assign employees (between 1 and10)
        self.position = [random.randint(1, numEmployee) for _ in range(numTasks)]
        self.velocity = [0.0] * numTasks #creates arry for velocity @ 0
        self.bestPosition = self.position[:]#stores personal best

        # Evaluate initial fitness
        particleWrapper = Chromosome(self.position[:])
        EvaluateFitness([particleWrapper])
        self.bestFitness = particleWrapper.fitness
        self.cost = particleWrapper.cost
        self.violation = particleWrapper.totalViolations

# allows for execution of particle swarm indivdually
if __name__ == "__main__":
    
    bestSolPSO, bestScorePSO = p.pso(numTasks=10, numEmployee=5, numParticles=180,
        maxIter=500)
    print("PSO Best sol:", bestSolPSO)
    print("PSO Best sol cost:", bestScorePSO)



