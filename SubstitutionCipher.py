import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

pset = gp.PrimitiveSet("MAIN",1)
pset.addPrimitive(str.find, 3)
pset.addPrimitive(str.split, 2)
pset.addPrimitive(str.join, 1)
pset.addPrimitive(str.replace, 3)

def score_func(actual, expected):
    return 0 # Placeholder

def eval_individual(indvidual, str1, str2, str3):
    func = toolbox.compile(expr=indvidual)

    errors = score_func()
    # input = func(str1, str2, str3)

    fitness = 1 if output == expected else 0
    return str

creator.create("FitnessMin", base.Fitness, weights=(-1,0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()