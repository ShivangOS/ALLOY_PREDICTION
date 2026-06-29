import random 
from copy import deepcopy
from alloy_prediction.optimizers.genetic.chromosome import Chromosome
from alloy_prediction.optimizers.genetic.population import Population
from alloy_prediction.optimizers.genetic.genetic_algorithm import GeneticAlgorithm
from alloy_prediction.models.linear_regression import hardness_predictor

ELEMENTS = [
    "Al", "Co", "Cr", "Fe", "Ni",
    "Cu", "Mn", "Ti", "V", "Nb",
    "Mo", "Zr", "Hf", "Ta", "W",
    "C", "Mg", "Zn", "Si", "Re",
    "N", "Sc", "Li", "Sn", "Be",
]

POPULATION_SIZE = 100

initial_population = Population(
    chromosomes=[],
    generation=0,
)

for _ in range(POPULATION_SIZE):

    # Choose between 3 and 8 alloying elements
    selected_elements = random.sample(ELEMENTS, random.randint(3, 8))

    # Generate random percentages for the selected elements
    values = [random.random() for _ in selected_elements]
    total = sum(values)

    # Start with every element absent
    genetic_code = {element: 0.0 for element in ELEMENTS}

    # Assign normalized percentages
    for element, value in zip(selected_elements, values):
        genetic_code[element] = value / total

    chromosome = Chromosome(genetic_code)

    initial_population.chromosomes.append(chromosome)



def crossover_strategy(parent_1: Chromosome, parent_2: Chromosome) -> tuple[Chromosome, Chromosome]:
    child_1_code = {}
    child_2_code = {}

    for element in parent_1.genetic_code:
        if random.random() < 0.5:
            child_1_code[element] = parent_1.genetic_code[element]
            child_2_code[element] = parent_2.genetic_code[element]
        else:
            child_1_code[element] = parent_2.genetic_code[element]
            child_2_code[element] = parent_1.genetic_code[element]
    # Normalize
    total = sum(child_1_code.values())
    if total > 0:
        child_1_code = {
            e: value / total
            for e, value in child_1_code.items()
        }

    total = sum(child_2_code.values())
    if total > 0:
        child_2_code = {
            e: value / total
            for e, value in child_2_code.items()
        }

    return Chromosome(child_1_code),Chromosome(child_2_code)
    
def mutating_strategy(
    chromosome,
    mutation_strength=0.1,
):

    element = random.choice(list(chromosome.genetic_code.keys()))

    chromosome.genetic_code[element] += (random.uniform(-mutation_strength,mutation_strength))

    chromosome.genetic_code[element] = max(chromosome.genetic_code[element], 0.0,)

    total = sum(chromosome.genetic_code.values())

    if total > 0:
        for key in chromosome.genetic_code:
            chromosome.genetic_code[key] /= total

    chromosome.fitness = None

def selecting_strategy(population,tournament_size=3,):

    def tournament():
        contestants = random.sample(population.chromosomes,tournament_size,)

        return max(contestants,key=lambda chromosome: chromosome.fitness,)

    return (tournament(),tournament(),)

def objective_function(property_value):
    return property_value

def continue_generating(current_population,next_population,):
    return len(next_population) < len(current_population)

def make_stagnation_stopper(patience=20):

    counter = 0

    def stopping(previous_best,
                 current_best):

        nonlocal counter

        if current_best > previous_best:
            counter = 0
        else:
            counter += 1

        return counter >= patience

    return stopping

optimization_stopping_function = make_stagnation_stopper(20)

ga = GeneticAlgorithm(continue_generating,crossover_strategy,mutating_strategy,objective_function,optimization_stopping_function,initial_population,predictor,selecting_strategy)