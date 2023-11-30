import csv
import json
import secrets


class Chromosome:
    def __init__(self, genes=None):
        self.genes = genes

    def get_fitness(self, population_file):
        """
        Read the population file and query for the corresponding fitness
        """
        with open(population_file, 'r', newline='') as f:
            for line in f:
                if line.startswith(self.genes):
                    return int(line.split(",")[1])


class Population:
    def __init__(self, population_file):
        self.chromosomes = []
        self.file = population_file
        self.chromosome_len = 0

        # Read the population file and create Chromosome object
        # for each chromosome in the file
        with open(population_file, 'r', newline='') as f:
            for line in f:
                if not line.startswith("chromosome,fitness"):
                    genes = line.split(",")[0]
                    chromosome = Chromosome(genes=genes)
                    self.chromosome_len = len(genes)
                    self.chromosomes.append(chromosome)

    def evolve(self, crossover_probability, mutation_probability):
        # Crossover the population
        crossover_result = self.crossover_population(crossover_probability)
        # Mutate the crossover-ed population
        mutate_result = self.mutate_population(crossover_result, mutation_probability)
        self.chromosomes = mutate_result

    def crossover_population(self, crossover_probability):
        crossover_result = []
        # Set the weights of chromosomes to their corresponding fitness
        # to do roulette wheel crossover
        weights = [c.get_fitness(self.file) for c in self.chromosomes]
        # Add squaring weights to increase probability crossover of fitter chromosomes
        sqr_weights = [sqr ** 2 for sqr in weights]

        # Crossover until have a new population with size equal to the current one
        while len(crossover_result) < len(self.chromosomes):
            # Select 2 chromosomes to be parents
            parent_1, parent_2 = secrets.SystemRandom().choices(population=self.chromosomes,
                weights=sqr_weights,
                k=2
            )
            # Perform crossover on the 2 selected chromosomes
            crossover_result.extend(self.crossover_chromosomes(parent_1, parent_2, crossover_probability))

        return crossover_result

    def crossover_chromosomes(self, parent_1, parent_2, crossover_probability):
        """
        Function to crossover two chromosomes
        """
        offspring_1 = Chromosome()
        offspring_2 = Chromosome()
        if secrets.SystemRandom().random() < crossover_probability:
            # Double Crossover happens
            # Select the 2 crossover points randomly
            crossover_point_1 = secrets.SystemRandom().randint(1, self.chromosome_len // 2)
            crossover_point_2 = secrets.SystemRandom().randint(self.chromosome_len // 2 + 1, self.chromosome_len - 1)
            offspring_1.genes = parent_1.genes[:crossover_point_1] \
                                + parent_2.genes[crossover_point_1:crossover_point_2] \
                                + parent_1.genes[crossover_point_2:]
            offspring_2.genes = parent_2.genes[:crossover_point_1] \
                                + parent_1.genes[crossover_point_1:crossover_point_2] \
                                + parent_2.genes[crossover_point_2:]
        else:
            # Crossover does not happen
            # then offsprings are identical to parents
            offspring_1.genes = parent_1.genes
            offspring_2.genes = parent_2.genes

        return offspring_1, offspring_2

    def mutate_population(self, crossover_result, mutation_probability):
        mutate_result = []
        for chromosome in crossover_result:
            if secrets.SystemRandom().random() < mutation_probability:
                # If mutation happens
                # Select a random mutation point
                mutation_point = secrets.SystemRandom().randint(0, self.chromosome_len - 1)
                # Flip the gene at the mutation point (1 -> 0, 0 -> 1)
                chromosome.genes = chromosome.genes[:mutation_point] + str(
                    1 - int(chromosome.genes[mutation_point])) + chromosome.genes[mutation_point + 1:]

            mutate_result.append(chromosome)

        return mutate_result


def generate_initial_population(population_file, population_size, chromosome_len):
    """
    Function to randomly generate the initial population of any size and chromosome length
    """
    with open(population_file, 'w', newline='') as f:
        fieldnames = ['chromosome', 'fitness']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(population_size):
            genes = ''
            for _ in range(chromosome_len):
                if secrets.SystemRandom().random() > 0.5:
                    genes += '1'
                else:
                    genes += '0'

            writer.writerow({"chromosome": genes, "fitness": 0})


def evolve_one_generation(population_file, config_file):
    """
    Function that takes in a population and evolve it one generation
    """
    with open(config_file, 'r') as f:
        config = json.load(f)

    population = Population(population_file)

    # Read the configured crossover_probability and mutation_probability in the configuration file
    population.evolve(config['crossover_probability'], config['mutation_probability'])
    _write_population_to_file(population, population_file)


def _write_population_to_file(population, population_file):
    """
    Function to write the population to a CSV file
    """
    with open(population_file, 'w', newline='') as f:
        fieldnames = ['chromosome', 'fitness']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in population.chromosomes:
            writer.writerow({"chromosome": c.genes, "fitness": 0})
