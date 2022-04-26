#Class to calculate degrees of membership for speed. Points that are not 0 or 1 are calculated #based off of slope.
class Speed:
    def __init__(self, spd):
        self.spd = spd
        self.slow_dom = self.calculate_dom_low_spd()
        self.medium_dom = self.calculate_dom_medium_spd()
        self.fast_dom = self.calculate_dom_fast_spd()

    def calculate_dom_low_spd(self, chromosome):
        if 0 <= self.spd <= int(chromosome[98:100], 2):
            dom = 1
        elif int(chromosome[98:100], 2) < self.spd <= (int(chromosome[98:100], 2) + int(chromosome[101:103], 2)):
            dom = ((int(chromosome[98:100], 2) + int(chromosome[101:103], 2)) - self.spd) * (1 / (int(chromosome[101:103], 2)))
        else:
            dom = 0
        return dom

    def calculate_dom_medium_spd(self, chromosome):
        if (int(chromosome[98:100], 2) + int(chromosome[110:112], 2)) <= self.spd <= (int(chromosome[98:100], 2) + int(chromosome[110:112], 2) + int(chromosome[104:106], 2)):
            dom = (1 / int(chromosome[104:106], 2)) * (self.spd - (int(chromosome[98:100], 2) + int(chromosome[110:112], 2)))
        elif (int(chromosome[98:100], 2) + int(chromosome[110:112], 2) + int(chromosome[104:106], 2)) < self.spd <= (int(chromosome[98:100], 2) + int(chromosome[110:112], 2) + int(chromosome[104:106], 2) + int(chromosome[104:106], 2)):
            dom = 1 - ((1 / int(chromosome[104:106], 2)) * (self.spd - (int(chromosome[98:100],2) + int(chromosome[110:112],2) + int(chromosome[104:106], 2))))
        else:
            dom = 0
        return dom

    def calculate_dom_fast_spd(self, chromosome):
        if (int(chromosome[98:100],2) + int(chromosome[110:112],2) + int(chromosome[104:106],2) + int(chromosome[113:115],2)) <= self.spd < (int(chromosome[98:100],2) + int(chromosome[110:112],2) + int(chromosome[104:106],2) + int(chromosome[113:115],2) + int(chromosome[107:109],2)):
            dom = (1 / int(chromosome[107:109],2)) * (self.spd - (int(chromosome[98:100],2) + int(chromosome[110:112],2) + int(chromosome[104:106],2) + int(chromosome[113:115],2)))
        elif (int(chromosome[98:100],2) + int(chromosome[110:112],2) + int(chromosome[104:106],2) + int(chromosome[113:115],2) + int(chromosome[107:109],2)) <= self.spd:
            dom = 1
        else:
            dom = 0
        return dom
