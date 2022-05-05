# Class to calculate degrees of membership for turn angle. 
# Points that are not 0 or 1 are calculated #based off of slope.
class TurnAngle:
    def __init__(self, angle, chrms):
        self.angle = angle
        self.small_dom = self.calculate_dom_small_angle(chrms)
        self.medium_dom = self.calculate_dom_medium_angle(chrms)
        self.large_dom = self.calculate_dom_large_angle(chrms)

    def calculate_dom_small_angle(self, chrms):
        if 0 <= self.angle <= int(chrms[116:120], 2):
            dom = 1
        
        elif int(chrms[116:120], 2) < self.angle <= (int(chrms[116:120], 2) + int(chrms[121:125], 2)):
            dom = ((int(chrms[116:120], 2) + int(chrms[121:125], 2)) - self.angle) * (1 / (int(chrms[121:125], 2)))
        
        else:
            dom = 0
        
        return dom

    def calculate_dom_medium_angle(self, chrms):
        if (int(chrms[116:120], 2) + int(chrms[136:140], 2)) <= self.angle <= (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2)):
            dom = (1 / int(chrms[126:130], 2)) * (self.angle - (int(chrms[116:120], 2) + int(chrms[136:140], 2)))
        
        elif (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2)) < self.angle <= (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2) + int(chrms[126:130], 2)):
            dom = 1 - ((1 / int(chrms[126:130], 2)) * (self.angle - (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2))))
        
        else:
            dom = 0
        
        return dom

    def calculate_dom_large_angle(self, chrms):
        if (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2) + int(chrms[141:145], 2)) <= self.angle < (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2) + int(chrms[141:145], 2) + int(chrms[131:135], 2)):
            dom = (1 / int(chrms[131:135], 2)) * (self.angle - (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2) + int(chrms[141:145], 2)))
        
        elif (int(chrms[116:120], 2) + int(chrms[136:140], 2) + int(chrms[126:130], 2) + int(chrms[141:145], 2) + int(chrms[131:135], 2)) <= self.angle:
            dom = 1
        
        else:
            dom = 0
        
        return dom
