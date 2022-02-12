class Speed:
    def __init__(self, spd):
        self.spd = spd
        self.slow_dom = self.calculate_dom_low_spd()
        self.medium_dom = self.calculate_dom_medium_spd()
        self.fast_dom = self.calculate_dom_fast_spd()

    def calculate_dom_low_spd(self):
        if 0 <= self.spd <= 4:
            dom = 1
        elif 4 < self.spd <= 6:
            dom = (-1 / 2) * self.spd + 3
        else:
            dom = 0
        return dom

    def calculate_dom_medium_spd(self):
        if 5 <= self.spd <= 6:
            dom = self.spd - 5
        elif 6 <= self.spd <= 7:
            dom = 1
        elif 7 <= self.spd <= 8:
            dom = - self.spd + 8
        else:
            dom = 0
        return dom

    def calculate_dom_fast_spd(self):
        if 7 <= self.spd <= 10:
            dom = (1 / 3) * self.spd - (7 / 3)
        elif self.spd >= 10:
            dom = 1
        else:
            dom = 0
        return dom
