#Class to calculate degrees of membership for wall distance. Points that are not 0 or 1 are calculated #based off of slope.
class WallDistance:
    def __init__(self, dist):
        self.dist = dist
        self.near_dom = self.calculate_dom_near_wall()
        self.medium_dom = self.calculate_dom_medium_wall()
        self.far_dom = self.calculate_dom_far_wall()

    def calculate_dom_near_wall(self, chromosome):
        if 0 <= self.dist <= int(chromosome[49:57], 2):
            dom = 1
        elif int(chromosome[49:57], 2) < self.dist <= (int(chromosome[49:57], 2) + int(chromosome[58:65], 2)):
            dom = ((int(chromosome[49:57], 2) + int(chromosome[58:65], 2)) - self.dist) * (1 / (int(chromosome[58:65], 2)))
        else:
            dom = 0
        return dom

    def calculate_dom_medium_wall(self, chromosome):
        if (int(chromosome[49:57], 2) + int(chromosome[82:89], 2)) <= self.dist <= (int(chromosome[49:57], 2) + int(chromosome[82:89], 2) + int(chromosome[66:73], 2)):
            dom = (1 / int(chromosome[66:73], 2)) * (self.dist - (int(chromosome[49:57], 2) + int(chromosome[82:89], 2)))
        elif (int(chromosome[49:57], 2) + int(chromosome[82:89], 2) + int(chromosome[66:73], 2)) < self.dist <= (int(chromosome[49:57], 2) + int(chromosome[82:89], 2) + int(chromosome[66:73], 2) + int(chromosome[66:73], 2)):
            dom = 1 - ((1 / int(chromosome[66:73], 2)) * (self.dist - (int(chromosome[49:57],2) + int(chromosome[82:89],2) + int(chromosome[66:73], 2))))
        else:
            dom = 0
        return dom

    def calculate_dom_far_wall(self, chromosome):
        if (int(chromosome[49:57],2) + int(chromosome[82:89],2) + int(chromosome[66:73],2) + int(chromosome[90:97],2)) <= self.dist < (int(chromosome[49:57],2) + int(chromosome[82:89],2) + int(chromosome[66:73],2) + int(chromosome[90:97],2) + int(chromosome[74:81],2)):
            dom = (1 / int(chromosome[74:81],2)) * (self.dist - (int(chromosome[49:57],2) + int(chromosome[82:89],2) + int(chromosome[66:73],2) + int(chromosome[90:97],2)))
        elif (int(chromosome[49:57],2) + int(chromosome[82:89],2) + int(chromosome[66:73],2) + int(chromosome[90:97],2) + int(chromosome[74:81],2)) <= self.dist:
            dom = 1
        else:
            dom = 0
        return dom
