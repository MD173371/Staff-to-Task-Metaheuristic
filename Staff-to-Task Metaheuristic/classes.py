# Classes for use in implementations
# Contributers: Michael Durkan

class Error(Exception):
    pass

class Employee: 
    def __init__(self, id, hours, level, skills):
        self.id = id
        self.hours = hours
        self.level = level
        self.skills = skills

class Task:
    def __init__(self, id, time, difficulty, deadline, skill):
        self.id = id
        self.time = time
        self.difficulty = difficulty
        self.deadline = deadline
        self.skill = skill

class Chromosome:
    def __init__(self, geneList=None):
        self.geneList = geneList
        self.fitness = 0
        self.finish = 0
        self.violation = 0
        self.overPenalty = 0
        self.skillPenalty = 0
        self.diffPenalty = 0
        self.deadlinePenalty = 0
        self.assignPenalty = 0
        self.cost = 0
        self.fitnessRatio = 0
        self.cumulativeProb = 0
        self.totalViolations = 0

    def resetValues(self):
        self.fitness = 0
        self.finish = 0
        self.violation = 0
        self.overPenalty = 0
        self.skillPenalty = 0
        self.diffPenalty = 0
        self.deadlinePenalty = 0
        self.assignPenalty = 0
        self.cost = 0
        self.fitnessRatio = 0
        self.cumulativeProb = 0 
        self.totalViolations = 0
