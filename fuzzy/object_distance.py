#Class to calculate degrees of membership for object distance. Points that are not 0 or 1 are calculated #based off of slope.
class ObjectDistance:
    def __init__(self, dist):
        self.dist = dist
        self.near_dom = self.calculate_dom_near_dist()
        self.medium_dom = self.calculate_dom_medium_dist()
        self.far_dom = self.calculate_dom_far_dist()

    def calculate_dom_near_dist(self, chromosome):
        
        if 0 <= self.dist <= int(chromosome[0:8], 2):
            dom = 1
        elif int(chromosome[0:8], 2) < self.dist <= (int(chromosome[0:8], 2) + int(chromosome[9:16], 2)):
            dom = ((int(chromosome[0:8], 2) + int(chromosome[9:16], 2)) - self.dist) * (1 / (int(chromosome[9:16], 2)))
        else:
            dom = 0
        return dom

    def calculate_dom_medium_dist(self, chromosome):
        if (int(chromosome[0:8], 2) + int(chromosome[33:40], 2)) <= self.dist <= (int(chromosome[0:8], 2) + int(chromosome[33:40], 2) + int(chromosome[17:24], 2)):
            dom = (1 / int(chromosome[17:24], 2)) * (self.dist - (int(chromosome[0:8], 2) + int(chromosome[33:40], 2)))
        elif (int(chromosome[0:8], 2) + int(chromosome[33:40], 2) + int(chromosome[17:24], 2)) < self.dist <= (int(chromosome[0:8], 2) + int(chromosome[33:40], 2) + int(chromosome[17:24], 2) + int(chromosome[17:24], 2)):
            dom = 1 - ((1 / int(chromosome[17:24], 2)) * (self.dist - (int(chromosome[0:8],2) + int(chromosome[33:40],2) + int(chromosome[17:24], 2))))
        else:
            dom = 0
        return dom

    def calculate_dom_far_dist(self, chromosome):
        if (int(chromosome[0:8],2) + int(chromosome[33:40],2) + int(chromosome[17:24],2) + int(chromosome[41:48],2)) <= self.dist < (int(chromosome[0:8],2) + int(chromosome[33:40],2) + int(chromosome[17:24],2) + int(chromosome[41:48],2) + int(chromosome[25:32],2)):
            dom = (1 / int(chromosome[25:32],2)) * (self.dist - (int(chromosome[0:8],2) + int(chromosome[33:40],2) + int(chromosome[17:24],2) + int(chromosome[41:48],2)))
        elif (int(chromosome[0:8],2) + int(chromosome[33:40],2) + int(chromosome[17:24],2) + int(chromosome[41:48],2) + int(chromosome[25:32],2)) <= self.dist:
            dom = 1
        else:
            dom = 0
        return dom
