# Main executable file
# Contributers: Michael Durkan

from data import tasks, employees
from classes import Task, Employee, Chromosome
import ga as g
import test as t
import aco as a
import pso as p
import random
import copy

if __name__ == "__main__":
    
    # Run Genetic Algorithm
    bestSolGA = g.GeneticAlgorithm(60, 500, 0.77, 0.2, 1)
    print("GA Best sol:", bestSolGA.geneList)
    print("GA Best sol cost:", bestSolGA.cost) 

    # Run Ant Colony Optimisation
    bestSolACO, bestCostACO= a.AntColonyOptimisation(120,0.15,60,500)
    print("ACO Best sol:", bestSolACO)
    print("ACO Best sol cost:", bestCostACO)

    # Run Particle Swarm Optimisation
    bestSolPSO, bestCostPSO = p.pso(numTasks=10, numEmployee=5, numParticles=180,
        maxIter=500)
    print("PSO Best sol:", bestSolPSO)
    print("PSO Best sol cost:", bestCostPSO)
