# Class to calculate degrees of membership for wall distance. 
# Points that are not 0 or 1 are calculated #based off of slope.
class WallDistance:
    def __init__(self, dist, chrms):
        self.dist = dist
        self.near_dom = self.calculate_dom_near_wall(chrms)
        self.medium_dom = self.calculate_dom_medium_wall(chrms)
        self.far_dom = self.calculate_dom_far_wall(chrms)

    def calculate_dom_near_wall(self, chrms):
        if 0 <= self.dist <= int(chrms[49:57], 2):
            dom = 1
            
        elif int(chrms[49:57], 2) < self.dist <= (int(chrms[49:57], 2) + int(chrms[58:65], 2)):
            dom = ((int(chrms[49:57], 2) + int(chrms[58:65], 2)) - self.dist) * (1 / (int(chrms[58:65], 2)))
            
        else:
            dom = 0
            
        return dom

    def calculate_dom_medium_wall(self, chrms):
        if (int(chrms[49:57], 2) + int(chrms[82:89], 2)) <= self.dist <= (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2)):
            dom = (1 / int(chrms[66:73], 2)) * (self.dist - (int(chrms[49:57], 2) + int(chrms[82:89], 2)))
        
        elif (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2)) < self.dist <= (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2) + int(chrms[66:73], 2)):
            dom = 1 - ((1 / int(chrms[66:73], 2)) * (self.dist - (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2))))
       
        else:
            dom = 0
        
        return dom

    def calculate_dom_far_wall(self, chrms):
        if (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2) + int(chrms[90:97], 2)) <= self.dist < (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2) + int(chrms[90:97], 2) + int(chrms[74:81], 2)):
            dom = (1 / int(chrms[74:81], 2)) * (self.dist - (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2) + int(chrms[90:97], 2)))
        
        elif (int(chrms[49:57], 2) + int(chrms[82:89], 2) + int(chrms[66:73], 2) + int(chrms[90:97], 2) + int(chrms[74:81], 2)) <= self.dist:
            dom = 1
        
        else:
            dom = 0
        
        return dom
