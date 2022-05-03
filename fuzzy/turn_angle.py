#Class to calculate degrees of membership for turn angle. Points that are not 0 or 1 are calculated #based off of slope.
class TurnAngle:
    def __init__(self, angle, chromosome):
        self.angle = angle
        self.small_dom = self.calculate_dom_small_angle(chromosome)
        self.medium_dom = self.calculate_dom_medium_angle(chromosome)
        self.large_dom = self.calculate_dom_large_angle(chromosome)

    def calculate_dom_small_angle(self, chromosome):
        if 0 <= self.angle <= int(chromosome[116:120], 2):
            dom = 1
        elif int(chromosome[116:120], 2) < self.angle <= (int(chromosome[116:120], 2) + int(chromosome[121:125], 2)):
            dom = ((int(chromosome[116:120], 2) + int(chromosome[121:125], 2)) - self.angle) * (1 / (int(chromosome[121:125], 2)))
        else:
            dom = 0
        return dom

    def calculate_dom_medium_angle(self, chromosome):
        if (int(chromosome[116:120], 2) + int(chromosome[136:140], 2)) <= self.angle <= (int(chromosome[116:120], 2) + int(chromosome[136:140], 2) + int(chromosome[126:130], 2)):
            dom = (1 / int(chromosome[126:130], 2)) * (self.angle - (int(chromosome[116:120], 2) + int(chromosome[136:140], 2)))
        elif (int(chromosome[116:120], 2) + int(chromosome[136:140], 2) + int(chromosome[126:130], 2)) < self.angle <= (int(chromosome[116:120], 2) + int(chromosome[136:140], 2) + int(chromosome[126:130], 2) + int(chromosome[126:130], 2)):
            dom = 1 - ((1 / int(chromosome[126:130], 2)) * (self.angle - (int(chromosome[116:120],2) + int(chromosome[136:140],2) + int(chromosome[126:130], 2))))
        else:
            dom = 0
        return dom

    def calculate_dom_large_angle(self, chromosome):
        if (int(chromosome[116:120],2) + int(chromosome[136:140],2) + int(chromosome[126:130],2) + int(chromosome[141:145],2)) <= self.angle < (int(chromosome[116:120],2) + int(chromosome[136:140],2) + int(chromosome[126:130],2) + int(chromosome[141:145],2) + int(chromosome[131:135],2)):
            dom = (1 / int(chromosome[131:135],2)) * (self.angle - (int(chromosome[116:120],2) + int(chromosome[136:140],2) + int(chromosome[126:130],2) + int(chromosome[141:145],2)))
        elif (int(chromosome[116:120],2) + int(chromosome[136:140],2) + int(chromosome[126:130],2) + int(chromosome[141:145],2) + int(chromosome[131:135],2)) <= self.angle:
            dom = 1
        else:
            dom = 0
        return dom
