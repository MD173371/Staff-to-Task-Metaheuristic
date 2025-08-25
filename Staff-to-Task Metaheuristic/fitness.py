# Functions for performing fitness evaluations
# Contributers: Michael Durkan

from data import tasks, employees
from classes import Task, Employee, Chromosome
import random
import copy

# Name: CalcOverloadPenalty 
# Purpose: Calculate the penalty for employees being given to many hours
# Input: vector: solution list, taskList: list of tasks, empList: list of employees
# Output: None 
def CalcOverloadPenalty(vector, taskList, empList):    
    # Calculate total hours assigned to each employee
    assignedHrs = [0] * len(empList)
    overloadList = []
    for i, entry in enumerate(vector.geneList):
        assignedHrs[entry-1] += taskList[i].time

    for i, emp in enumerate(empList):
        overload = empList[i].hours - assignedHrs[i]
        if overload < 0:
            vector.overPenalty += abs(overload) 
    
# Name: CalcSkillPenalty
# Purpose: Calculate Penalty for employees being assigned task off different skill requirement
# Input: vector: solution list, taskList: list of tasks, empList: list of employees
# Output: None
def CalcSkillPenalty(vector, taskList, empList):
    for i, entry in enumerate(vector.geneList):
        foundSkill = False
        if entry > 0:
            for skill in empList[entry-1].skills:
                if skill == taskList[i].skill:
                    foundSkill = True
            if foundSkill == False:
                vector.skillPenalty += 1

# Name: CalcDiffPenalty
# Purpose: Calculate penalty for employees being assigned to difficult a task
# Input: vector: solution list, taskList: list of tasks, empList: list of employees
# Output: None
def CalcDiffPenalty(vector, taskList, empList):
    for i, entry in enumerate(vector.geneList):
        if taskList[i].difficulty > empList[entry-1].level:
            vector.diffPenalty += taskList[i].difficulty - empList[entry-1].level

# Name: CalcDeadlinePenalty 
# Purpose: Calculate Penalty for employees being assigned tasks that run over deadlines
# Input: vector: solution list, taskList: list of tasks, empList: list of employees
# Output: None
def CalcDeadlinePenalty(vector, taskList, empList):
    empTaskList = [[],[],[],[],[]]
    # Create list for each employee containing there tasks
    for i, entry in enumerate(vector.geneList):
        empTaskList[entry - 1].append(taskList[i])
    # Sort each least by processing time
    for i, assignedTasks in enumerate(empTaskList):
        empTaskList[i] = SortTasksByTime(empTaskList[i])
    # Iterate through task lists
    for i, taskList in enumerate(empTaskList):
        finish = 0
        for task in taskList:
            finish += task.time
            viol = finish - task.deadline
            if viol > 0:
                vector.violation += viol
        if vector.violation > 0:
            vector.deadlinePenalty = vector.violation

# Name: CalcAssignmentPenalty 
# Purpose: Calculate penalty for multiple assignment of tasks to one employee
# Input: vector: solution list, taskList: list of tasks, empList: list of employees
# Output: None
def CalcAssignmentPenalty(vector, taskList, empList):
    for i, gene in enumerate(vector.geneList):
        if gene < 1:
            vector.assignPenalty += 1
 
# Name: SortTasksByTime
# Purpose: Sort tasks in a list by the time it takes to complete them
# Input: taskList: task List
# Output: sortedTask: sorted Task List
def SortTasksByTime(taskList):
    sortedTasks = taskList
    sortedTasks = sorted(sortedTasks, key=lambda x: x.time)
    return sortedTasks

       
# Name: CalcCost
# Purpose: Calculate the cost of each solution by applying penalties
# Input: inPopulation: List of solution vectors
# Output: None
def CalcCost(inPopulation):
    totalFitness = 0
    epsilon = 1e-8

    for chromo in inPopulation:
        chromo.cost = 0.2 * ( 
                        chromo.overPenalty + 
                        chromo.skillPenalty + 
                        chromo.diffPenalty + 
                        chromo.deadlinePenalty + 
                        chromo.assignPenalty )
    
        chromo.fitness = 1.0 / (chromo.cost + epsilon)
        totalFitness += chromo.fitness

    for chromo in inPopulation:
        chromo.fitnessRatio = chromo.fitness / totalFitness

# Name: CalcCumulative
# Purpose: Calculate the cumulative probabilities of each solution in a population
# Input: inPopulation: list of solution vectors
# Output: None
def CalcCumulative(inPopulation):
    inPopulation[0].cumulativeProb = inPopulation[0].fitnessRatio 
    for i in range(1, len(inPopulation)):
        inPopulation[i].cumulativeProb = inPopulation[i - 1].cumulativeProb + inPopulation[i].fitnessRatio

def totalViolations(self):
    return  self.overPenalty + self.skillPenalty + self.diffPenalty + self.deadlinePenalty + self.assignPenalty



# Name: EvaluateFitness 
# Purpose: Evalute the Fitness of each vecotr in a population, updating there
#   object fields.
# Input: population: list of solution vectors
# Output: None
def EvaluateFitness(population):
    
    # Create Employee and Task Lists with Synthetic data
    empList = [Employee(**empData) for empData in employees]
    taskList = [Task(**taskData) for taskData in tasks]
    
    for vector in population:
        vector.resetValues()
        CalcOverloadPenalty(vector, taskList, empList) 
        CalcSkillPenalty(vector, taskList, empList)
        CalcAssignmentPenalty(vector, taskList, empList)
        CalcDiffPenalty(vector, taskList, empList)
        CalcDeadlinePenalty(vector, taskList, empList)
    
        vector.totalViolations = (vector.overPenalty + vector.skillPenalty + 
                                  vector.diffPenalty + vector.deadlinePenalty + 
                                  vector.assignPenalty)
    CalcCost(population)
    CalcCumulative(population)
