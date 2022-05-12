# Class to calculate degrees of membership for speed. Points that are not 0 or 1 are calculated #based off of slope.
class Speed:
    def __init__(self, spd, chrms):
        self.spd = spd
        self.slow_dom = self.calculate_dom_low_spd(chrms)
        self.medium_dom = self.calculate_dom_medium_spd(chrms)
        self.fast_dom = self.calculate_dom_fast_spd(chrms)

    def calculate_dom_low_spd(self, chrms):
        if 0 <= self.spd <= int(chrms[98:101], 2):
            dom = 1
            
        elif int(chrms[98:101], 2) < self.spd <= (int(chrms[98:101], 2) + int(chrms[101:104], 2)):
            dom = ((int(chrms[98:101], 2) + int(chrms[101:104], 2)) - self.spd) * (1 / (int(chrms[101:104], 2)))
            
        else:
            dom = 0
            
        return dom

    def calculate_dom_medium_spd(self, chrms):
        if (int(chrms[98:101], 2) + int(chrms[110:113], 2)) <= self.spd <= (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2)):
            dom = (1 / int(chrms[104:107], 2)) * (self.spd - (int(chrms[98:101], 2) + int(chrms[110:113], 2)))
        
        elif (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2)) < self.spd <= (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2) + int(chrms[104:107], 2)):
            dom = 1 - ((1 / int(chrms[104:107], 2)) * (self.spd - (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2))))
        
        else:
            dom = 0
        
        return dom

    def calculate_dom_fast_spd(self, chrms):
        if (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2) + int(chrms[113:116], 2)) <= self.spd < (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2) + int(chrms[113:116], 2) + int(chrms[107:110], 2)):
            dom = (1 / int(chrms[107:110], 2)) * (self.spd - (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2) + int(chrms[113:116], 2)))

        elif (int(chrms[98:101], 2) + int(chrms[110:113], 2) + int(chrms[104:107], 2) + int(chrms[113:116], 2) + int(chrms[107:110], 2)) <= self.spd:
            dom = 1

        else:
            dom = 0

        return dom
