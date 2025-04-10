import numpy

from deap import algorithms, base, creator, tools, gp

pset = gp.PrimitiveSet("MAIN", 3) # 3 input arguments for GP program
pset.addPrimitive(str.find, 3)
pset.addPrimitive(str.split, 2)
pset.addPrimitive(str.join, 1)
pset.addPrimitive(str.replace, 3)
pset.addPrimitive(str.strip, 1)

def score_func(actual, expected):
   score = 0
   if len(actual) != len(expected):
       return 10000
   return sum(1 for a, b in zip(actual, expected) if a != b) # Sum of mismatched char
   # for i in range(len(actual)):
   #         if actual[i] != expected[i]:
   #             score += 1
   #     return score
   

   # Wrapper function to pass additional arguments
def eval_with_args(individual):
    return eval_individual(individual, "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "svool dliow")  # Replace with actual inputs

creator.create("FitnessMin", base.Fitness, weights=(-1,))  # Single-objective fitness

def eval_individual(indvidual, str1, str2, str3):
    func = toolbox.compile(expr=indvidual)
    try:
        output = func(str1, str2, str3)
    except Exception as e:
        return 10000,  # Return a single value as a tuple
    
    table = str.maketrans("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba")
    expected = str3.translate(table)

    errors = score_func(output, expected)
    return errors,  # Return a single value as a tuple

creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=3, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", eval_with_args)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
   pop = toolbox.population(n=1000)
   hof = tools.HallOfFame(1)


   stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
   stats_size = tools.Statistics(len)
   mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
   mstats.register("avg", numpy.mean)
   mstats.register("std", numpy.std)
   mstats.register("min", numpy.min)
   mstats.register("max", numpy.max)


   pop, log = algorithms.eaSimple(pop, toolbox, 0.4, 0.6, 200, stats=mstats,
                                  halloffame=hof, verbose=True)
  
   # Print the best solution
   print("Best individual:", hof[0])
   func = toolbox.compile(expr=hof[0])
   print("Decoded message:", func("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "svool dliow"))

if __name__ == "__main__":
   main()
