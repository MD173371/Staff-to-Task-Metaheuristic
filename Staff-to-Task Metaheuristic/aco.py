# Ant Colony Optimization implementation file
# Contributers: Michael Durkan + Alexander Carey


from data import tasks, employees
from classes import Task, Employee, Chromosome
from fitness import EvaluateFitness
import random
import copy
import time
import csv

# Inputs:
#   numAnts: number of ants in colony
#   evapRate: evaporation rate of pheremones
#   depositConstant: degree to which pheremones are deposited relative to fitness
#   maxIterations: number of times function creates new colonies
# Outputs:
#   bestSolution: best solution vector after completion
#   bestCost: best cost of that vector after completion
def AntColonyOptimisation(numAnts, evapRate, depositConstant, maxIterations):
    # Start timer and create results list for graphing
    timeStart = time.perf_counter()
    results = []

    # Create lists of tasks and employee objects and get there cardinality
    taskList = [Task(**taskData) for taskData in tasks]
    empList = [Employee(**empData) for empData in employees]
    numTasks = len(taskList)
    numEmps = len(empList)

    # Initialize matrix of inital pheremones
    tau = [[1.0 for _ in range(numEmps)] for _ in range(numTasks)]

    # Initialize best solution and score
    bestSol = None
    bestScore = -float("inf")

    for iteration in range(1, maxIterations + 1):
        # Create lists for ants in iteration and there fitness values  
        antChromos = [] 
        # Construct a solution for each ant in colony
        for _ in range(1, numAnts + 1):
            curSolution = []
            # Increment through tasks and build a solution
            for taskIdx in range(numTasks):
                # Create list for feasible next solution index
                allowed = list(range(numEmps))
                
                # Calculate total pheremone for emp-task assignments
                totalPheremone = sum(tau[taskIdx][empIdx] for empIdx in allowed)

                # Generate a random threshold between 0 and totalPheremone
                r = random.uniform(0.0, totalPheremone)

                # Select next move using cumulative pheremone
                cumulative = 0.0
                chosen = allowed[-1]

                # Calculate cumulative prob to decide which employee does task
                for empIdx in allowed:
                    cumulative += tau[taskIdx][empIdx]
                    if cumulative >= r:
                        chosen = empIdx
                        break
                curSolution.append(chosen + 1) 
            antChromos.append(Chromosome(curSolution))

        # Evaluate the constructed solution (uses chromosome fitness eval) 
        EvaluateFitness(antChromos)

        # Create list of ants and there scores for use in pheremone deposit
        antList = [c.geneList for c in antChromos]
        scoreList = [c.fitness for c in antChromos]
        
        # Compare get the best score, solution and cost of ants in colony
        for chromo in antChromos:
            if chromo.fitness > bestScore:
                bestScore = chromo.fitness
                bestSolution = chromo.geneList.copy()
        bestCost = min(c.cost for c in antChromos)

        # Calculate total violations of ants in population for graphing
        totalViolations = sum((chromo.overPenalty + chromo.skillPenalty + 
                               chromo.diffPenalty + chromo.deadlinePenalty + 
                               chromo.assignPenalty) for chromo in antChromos)

        # Calculate elapsed time of iteration and add to graphing list details
        elapsedTime = time.perf_counter() - timeStart
        results.append([iteration, bestCost, elapsedTime, totalViolations]) 
        
        # Calculate Pheremone evaporation
        tau = CalcPhereEvap(tau, numTasks, numEmps, evapRate)

        # Calculate Pheremone Deposit
        tau = CalcPhereDeposit(tau, antList, scoreList, bestScore, depositConstant)
    
    # Output generation, cost, time and feasability to csv
    with open('acoCostResults.csv', 'w', newline='') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerow(['generation', 'bestCost', 'elapsedTime', 'feasability'])
        wr.writerows(results)

    return bestSolution, bestCost

# Name: CalcPhereEvap
# Purpose: Calculate and update pheremone values due to evaporation
# Input: tau: pheremone matrix, numTaks: number of tasks, numEmps: number of
#   employees, evapRate: evaporationRate
# Output: tau: pheremone matrix
def CalcPhereEvap(tau, numTasks, numEmps, evapRate):
    for taskIdx in range(numTasks):
        for empIdx in range(numEmps):
            tau[taskIdx][empIdx] *= (1.0 - evapRate)
    
    return tau

# Name: CalcPhereDeposit
# Purpose: Calculate an update the pheremone matrix based on the score of solution
# Input: tau: pheremone matrix, antList: list of solutions, scoreList: list of scores
#   bestScore: best score achieved, depositConstant: how much pheremone left behind
# Output: tau: peheremone matrix 
def CalcPhereDeposit(tau, antList, scoreList, bestScore, depositConstant):
    for curAnt, curFit in zip(antList, scoreList):
        for taskIdx, emp in enumerate(curAnt):
            empIdx = emp - 1
            tau[taskIdx][empIdx] += depositConstant / (1.0 + (bestScore - curFit))

    return tau

# Allows for execution of ant colony optimization individually
if __name__ == "__main__":

    # Run Ant Colony Optimisation
    bestSolACO, bestScoreACO= AntColonyOptimisation(120,0.15,60,500)
    print("ACO Best sol:", bestSolACO)
    print("ACO Best sol score:", bestScoreACO)
