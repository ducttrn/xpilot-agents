#Class to calculate degrees of membership for wall distance. Points that are not 0 or 1 are calculated #based off of slope.
class WallDistance:
    def __init__(self, dist):
        self.dist = dist
        self.near_dom = self.calculate_dom_near_wall()
        self.medium_dom = self.calculate_dom_medium_wall()
        self.far_dom = self.calculate_dom_far_wall()

    def calculate_dom_near_wall(self):
        if 0 <= self.dist <= 200:
            dom = 1
        elif 200 < self.dist <= 250:
            dom = (-1 / 50) * self.dist + 5
        else:
            dom = 0
        return dom

    def calculate_dom_medium_wall(self):
        if 200 <= self.dist <= 300:
            dom = (1 / 100) * self.dist - 2
        elif 300 < self.dist <= 400:
            dom = (-1 / 100) * self.dist + 4
        else:
            dom = 0
        return dom

    def calculate_dom_far_wall(self):
        if 350 < self.dist <= 450:
            dom = (1 / 100) * self.dist - 3.5
        elif self.dist > 450:
            dom = 1
        else:
            dom = 0
        return dom
