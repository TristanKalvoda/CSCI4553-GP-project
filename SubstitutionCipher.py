import numpy
import random
import operator
import matplotlib.pyplot as plt
import networkx as nx
from deap import algorithms, base, creator, tools, gp
from functools import partial

def find_char(c, s):
    return s.find(c)

def char_at(i, s):
    if 0 <= i < len(s):
        return s[i]
    return ""

pset = gp.PrimitiveSetTyped("MAIN", [str, str, str], str) # 3 input arguments for GP program
pset.addPrimitive(find_char, [str, str], int)
pset.addPrimitive(char_at, [int, str], str)
pset.addEphemeralConstant(name="rand_int", ephemeral=partial(random.randint, 0, 25), ret_type=int)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

char_examples = [
    ("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "s"),
    ("abc","cba","c"),
    # ("yhk","pcd","f"),
    # ("yhk","pcd","c")
]

def evalCipher(individual):
    func = toolbox.compile(expr=individual) 
    errors = 0
    for example in char_examples:
        str1, str2, encoded = example
        table = str.maketrans(str1, str2)
        expected = encoded.translate(table)
        if func(str1, str2, encoded) != expected:
            errors += 1
    return errors,

toolbox.register("evaluate", evalCipher)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

# toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17)) # maximum height of a tree after mate
# toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17)) # maximum height of a tree after mutate

def main():
    # random.seed(318)

    # Sets the population size to 300.
    pop = toolbox.population(n=300)
    # Tracks the single best individual over the entire run.
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    # Does the run, going for 40 generations (the 5th argument to `eaSimple`).
    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 40, stats=mstats,
                                   halloffame=hof, verbose=True)

    # print log

    # Print the members of the hall of fame
    print("\nBest individual:")
    print(hof[0])
    func = toolbox.compile(expr=hof[0])
    for example in char_examples:
        str1, str2, encoded = example
        table = str.maketrans(str1, str2)
        expected = encoded.translate(table)
        print("Decoded message:", func(str1,str2,encoded), "expected message: ", expected)
    
    print("======")
    
    string_cipher_example = ("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "svooldliow")
    str1, str2, encoded = string_cipher_example
    output_str = ""
    for char in range(len(encoded)):
        output_str += func(str1, str2, encoded[char])
    print("Decoded string: ", output_str, "\nExpected string:  helloworld")
    return pop, log, hof

    # print("Decoded message:", func("abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "svool dliow"))
    # print("Decoded message:", func("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ZYXWVUTSRQPONMLKJIHGFEDCBA", "HELLO WORLD"))  
    # print("Decoded message:", func("abc", "xyz", "cab"))

if __name__ == "__main__":
    pop, log, hof = main()  # Capture the returned hof object

    # Visualize the best individual
    import matplotlib.pyplot as plt
    import networkx as nx

    nodes, edges, labels = gp.graph(hof[0])  # Use hof[0] here
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, labels=labels, node_size=5000, node_color="lightblue")
    plt.show()