# Class to calculate degrees of membership for turn angle. 
# Points that are not 0 or 1 are calculated #based off of slope.
class TurnAngle:
    def __init__(self, angle, chrms):
        self.angle = angle
        self.small_dom = self.calculate_dom_small_angle(chrms)
        self.medium_dom = self.calculate_dom_medium_angle(chrms)
        self.large_dom = self.calculate_dom_large_angle(chrms)

    def calculate_dom_small_angle(self, chrms):
        if 0 <= self.angle <= int(chrms[116:121], 2):
            dom = 1
        
        elif int(chrms[116:121], 2) < self.angle <= (int(chrms[116:121], 2) + int(chrms[121:126], 2)):
            dom = ((int(chrms[116:121], 2) + int(chrms[121:126], 2)) - self.angle) * (1 / (int(chrms[121:126], 2)))
        
        else:
            dom = 0
        
        return dom

    def calculate_dom_medium_angle(self, chrms):
        if (int(chrms[116:121], 2) + int(chrms[136:141], 2)) <= self.angle <= (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2)):
            dom = (1 / int(chrms[126:131], 2)) * (self.angle - (int(chrms[116:121], 2) + int(chrms[136:141], 2)))
        
        elif (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2)) < self.angle <= (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2) + int(chrms[126:131], 2)):
            dom = 1 - ((1 / int(chrms[126:131], 2)) * (self.angle - (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2))))
        
        else:
            dom = 0
        
        return dom

    def calculate_dom_large_angle(self, chrms):
        if (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2) + int(chrms[141:146], 2)) <= self.angle < (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2) + int(chrms[141:146], 2) + int(chrms[131:136], 2)):
            dom = (1 / int(chrms[131:136], 2)) * (self.angle - (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2) + int(chrms[141:146], 2)))
        
        elif (int(chrms[116:121], 2) + int(chrms[136:141], 2) + int(chrms[126:131], 2) + int(chrms[141:146], 2) + int(chrms[131:136], 2)) <= self.angle:
            dom = 1
        
        else:
            dom = 0
        
        return dom
