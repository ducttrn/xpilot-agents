#Class to calculate degrees of membership for object distance. Points that are not 0 or 1 are calculated #based off of slope.
class ObjectDistance:
    def __init__(self, dist):
        self.dist = dist
        self.near_dom = self.calculate_dom_near_dist()
        self.medium_dom = self.calculate_dom_medium_dist()
        self.far_dom = self.calculate_dom_far_dist()

    def calculate_dom_near_dist(self):
        if 0 <= self.dist <= 200:
            dom = 1
        elif 200 < self.dist <= 300:
            dom = (-1 / 100) * self.dist + 3
        else:
            dom = 0
        return dom

    def calculate_dom_medium_dist(self):
        if 200 <= self.dist <= 300:
            dom = (1 / 100) * self.dist - 2
        elif 300 < self.dist <= 400:
            dom = (-1 / 100) * self.dist + 4
        else:
            dom = 0
        return dom

    def calculate_dom_far_dist(self):
        if 350 <= self.dist < 450:
            dom = (1 / 100) * self.dist - 7 / 2
        elif 450 <= self.dist:
            dom = 1
        else:
            dom = 0
        return dom
