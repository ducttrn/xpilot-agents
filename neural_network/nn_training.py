import csv
import libpyAI as ai

from genetic_algorithm import evolve_one_generation

generation = 1
count = 0
check = 0
rowCount = 2
weights = []


def AI_loop():
    ai.setTurnSpeed(20)
    ai.setPower(35)
    ai.turnRight(0)
    ai.turnLeft(0)
    ai.thrust(0)

    global count
    global check
    global rowCount
    global weights
    global generation

    # Count how long alive for fitness
    if ai.selfAlive() == 1:
        count += 1
        check = 0

    if ai.selfAlive() == 0 and check == 0 and rowCount < 514:
        with open('nn_population.csv', newline='') as f:
            r = csv.reader(f)
            lines = list(r)
            lines[rowCount - 1][1] = str(count)
            writer = csv.writer(f)
            writer.writerows(lines)

            chromosome = lines[rowCount - 1][0]
            weights = [chromosome[i:i + 6] for i in range(0, len(chromosome), 6)]

        rowCount += 1
        check = 1
        count = 0

    elif ai.selfAlive() == 0 and check == 0 and rowCount == 514:
        evolve_one_generation('nn_population.csv', 'nn_ga_config.json')
        with open('nn_population.csv', newline='') as f:
            csv_reader = csv.reader(f)
            line = next(csv_reader)
            chromosome = line[0]
            weights = [chromosome[i:i + 6] for i in range(0, len(chromosome), 6)]

        rowCount = 2
        count = 0
        check = 1
        generation += 1


ai.start(AI_loop, ["-name", "NNBot", "-join", "localhost"])
