class Chromosome:
    def __init__(self, genetic_code):
        self.genetic_code = genetic_code
        self.fitness = None

    @property
    def composition(self):
        return self.genetic_code

    def __repr__(self):
        return f"{self.genetic_code}"

    def evaluate_fitness(self, predictor, objective):
        property_value = predictor(self.composition)
        return objective(property_value)

    def update_fitness(self, predictor, objective):
        self.fitness = self.evaluate_fitness(predictor, objective)
        return self.fitness