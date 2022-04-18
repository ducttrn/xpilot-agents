import csv
import json
import random


class Chromosome:
    def __init__(self, genes=None):
        self.genes = genes

    def get_fitness(self, population_file):
        with open(population_file, 'r', newline='') as f:
            for line in f:
                if line.startswith(self.genes):
                    return int(line.split(",")[1])


class Population:
    def __init__(self, population_file):
        self.chromosomes = []
        self.file = population_file
        self.chromosome_len = 0

        with open(population_file, 'r', newline='') as f:
            for line in f:
                if not line.startswith("chromosome,fitness"):
                    genes = line.split(",")[0]
                    chromosome = Chromosome(genes=genes)
                    self.chromosome_len = len(genes)
                    self.chromosomes.append(chromosome)

    def evolve(self, crossover_probability, mutation_probability):
        crossover_result = self.crossover_population(crossover_probability)
        mutate_result = self.mutate_population(crossover_result, mutation_probability)
        self.chromosomes = mutate_result

    # Add squaring weights to increase probability crossover of fitter chromosomes
    def crossover_population(self, crossover_probability):
        crossover_result = []
        weights = [c.get_fitness(self.file) for c in self.chromosomes]
        sqr_weights = [sqr ** 2 for sqr in weights]
        while len(crossover_result) < len(self.chromosomes):
            parent_1, parent_2 = random.choices(
                population=self.chromosomes,
                weights=sqr_weights,
                k=2
            )
            print(parent_1.genes)
            crossover_result.extend(self.crossover_chromosomes(parent_1, parent_2, crossover_probability))
        return crossover_result

    def crossover_chromosomes(self, parent_1, parent_2, crossover_probability):
        offspring_1 = Chromosome()
        offspring_2 = Chromosome()
        if random.random() < crossover_probability:
            # Crossover happens
            crossover_point = random.randint(1, self.chromosome_len - 2)
            offspring_1.genes = parent_1.genes[:crossover_point] + parent_2.genes[crossover_point:]
            offspring_2.genes = parent_2.genes[:crossover_point] + parent_1.genes[crossover_point:]
        else:
            offspring_1.genes = parent_1.genes
            offspring_2.genes = parent_2.genes
        return offspring_1, offspring_2

    def mutate_population(self, crossover_result, mutation_probability):
        mutate_result = []
        for chromosome in crossover_result:
            if random.random() < mutation_probability:
                mutation_point = random.randint(0, self.chromosome_len - 1)
                chromosome.genes = chromosome.genes[:mutation_point] + str(
                    1 - int(chromosome.genes[mutation_point])) + chromosome.genes[mutation_point + 1:]

            mutate_result.append(chromosome)
        return mutate_result


def generate_initial_population(population_file, population_size, chromosome_len):
    with open(population_file, 'w', newline='') as f:
        fieldnames = ['chromosome', 'fitness']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(population_size):
            genes = ''
            for _ in range(chromosome_len):
                if random.random() > 0.5:
                    genes += '1'
                else:
                    genes += '0'

            writer.writerow({"chromosome": genes, "fitness": 0})


def evolve_one_generation(population_file, config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    population = Population(population_file)
    population.evolve(config['crossover_probability'], config['mutation_probability'])
    _write_population_to_file(population, population_file)


def _write_population_to_file(population, population_file):
    with open(population_file, 'w', newline='') as f:
        fieldnames = ['chromosome', 'fitness']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in population.chromosomes:
            writer.writerow({"chromosome": c.genes, "fitness": 0})


if __name__ == "__main__":
    generate_initial_population('population.csv', 10, 6)
