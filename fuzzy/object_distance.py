# Class to calculate degrees of membership for object distance. 
# Points that are not 0 or 1 are calculated #based off of slope.
class ObjectDistance:
    def __init__(self, dist, chrms):
        self.dist = dist
        self.near_dom = self.calculate_dom_near_dist(chrms)
        self.medium_dom = self.calculate_dom_medium_dist(chrms)
        self.far_dom = self.calculate_dom_far_dist(chrms)

    def calculate_dom_near_dist(self, chrms):
        
        if 0 <= self.dist <= int(chrms[0:8], 2):
            dom = 1
            
        elif int(chrms[0:8], 2) < self.dist <= (int(chrms[0:8], 2) + int(chrms[9:16], 2)):
            dom = ((int(chrms[0:8], 2) + int(chrms[9:16], 2)) - self.dist) * (1 / (int(chrms[9:16], 2)))
            
        else:
            dom = 0
            
        return dom

    def calculate_dom_medium_dist(self, chrms):
        if (int(chrms[0:8], 2) + int(chrms[33:40], 2)) <= self.dist <= (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2)):
            dom = (1 / int(chrms[17:24], 2)) * (self.dist - (int(chrms[0:8], 2) + int(chrms[33:40], 2)))
            
        elif (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2)) < self.dist <= (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2) + int(chrms[17:24], 2)):
            dom = 1 - ((1 / int(chrms[17:24], 2)) * (self.dist - (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2))))
        
        else:
            dom = 0
            
        return dom

    def calculate_dom_far_dist(self, chrms):
        if (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2) + int(chrms[41:48], 2)) <= self.dist < (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2) + int(chrms[41:48], 2) + int(chrms[25:32], 2)):
            dom = (1 / int(chrms[25:32], 2)) * (self.dist - (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2) + int(chrms[41:48], 2)))
        
        elif (int(chrms[0:8], 2) + int(chrms[33:40], 2) + int(chrms[17:24], 2) + int(chrms[41:48], 2) + int(chrms[25:32], 2)) <= self.dist:
            dom = 1
        
        else:
            dom = 0
        
        return dom
