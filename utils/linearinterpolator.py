from typing import List, Tuple


class LinearInterpolator:
    def __init__(self, points: List[Tuple[float, float]]):
        self.points = points

    def interpolate(self, x):
        i = 1

        if x <= self.points[0][0]:
            return self.points[0][1]

        while i < len(self.points) and x > self.points[i][0]:
            i += 1

        if i == len(self.points):
            return self.points[i - 1][1]

        return (self.points[i][1] - self.points[i - 1][1]) / (self.points[i][0] - self.points[i - 1][0]) * (
                    x - self.points[i - 1][0]) + self.points[i - 1][1]