import csv
import libpyAI as ai

from genetic_algorithm import evolve_one_generation


def convert_genes_to_weight(genes):
    return (int(genes, 2) / 64 - 0.5) * 2


def AI_loop():
    ai.setTurnSpeed(20)
    ai.setPower(35)
    ai.turnRight(0)
    ai.turnLeft(0)
    ai.thrust(0)

    global survival_time
    global weights_updated
    global row_count
    global weights

    # Count how long alive for fitness
    if ai.selfAlive() == 1:
        survival_time += 1
        weights_updated = False

    if ai.selfAlive() == 0 and weights_updated is False and row_count < 514:
        with open('nn_population.csv', newline='') as f:
            r = csv.reader(f)
            lines = list(r)
            lines[row_count - 1][1] = str(survival_time)
            writer = csv.writer(f)
            writer.writerows(lines)

            chromosome = lines[row_count - 1][0]
            weights = [
                convert_genes_to_weight(chromosome[i:i + 6])
                for i in range(0, len(chromosome), 6)
            ]

        row_count += 1
        weights_updated = True
        survival_time = 0

    elif ai.selfAlive() == 0 and weights_updated is False and row_count == 514:
        evolve_one_generation('nn_population.csv', 'nn_ga_config.json')
        weights = get_initial_weights()
        row_count = 2
        weights_updated = True
        survival_time = 0


def get_initial_weights():
    with open('nn_population.csv', newline='') as f:
        csv_reader = csv.reader(f)
        line = next(next(csv_reader))
        return [
            convert_genes_to_weight(line[0][i:i + 6])
            for i in range(0, len(line[0]), 6)
        ]


if __name__ == "__main__":
    survival_time = 0
    weights_updated = False
    row_count = 2
    weights = get_initial_weights()

    ai.start(AI_loop, ["-name", "NNBot", "-join", "localhost"])
