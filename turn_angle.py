class TurnAngle:
    def __init__(self, angle):
        self.angle = angle
        self.small_dom = self.calculate_dom_small_angle()
        self.medium_dom = self.calculate_dom_medium_angle()
        self.large_dom = self.calculate_dom_large_angle()

    def calculate_dom_small_angle(self):
        if 0 <= self.angle <= 15:
            dom = 1
        elif 15 < self.angle <= 25:
            dom = (-1 / 5) * self.angle + 4
        else:
            dom = 0
        return dom

    def calculate_dom_medium_angle(self):
        if 20 <= self.angle <= 40:
            dom = (1 / 20) * self.angle - 1
        elif 40 < self.angle <= 60:
            dom = (-1 / 20) * self.angle + 3
        else:
            dom = 0
        return dom

    def calculate_dom_large_angle(self):
        if 55 <= self.angle < 90:
            dom = (1 / 35) * self.angle - 11 / 7
        elif 90 <= self.angle:
            dom = 1
        else:
            dom = 0
        return dom
