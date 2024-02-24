from typing import List, Tuple, Optional, Union


class LinearInterpolator:
    def __init__(self, points: List[Tuple[float, float]]):
        self.points = points
        self._interpolated_value: Optional[float] = None

    def getInterpolatedValue(self) -> Union[None, float]:
        return self._interpolated_value

    def interpolate(self, x):
        i = 1

        if x <= self.points[0][0]:
            self._interpolated_value = self.points[0][1]
            return self._interpolated_value

        while i < len(self.points) and x > self.points[i][0]:
            i += 1

        if i == len(self.points):
            self._interpolated_value = self.points[i - 1][1]
            return self._interpolated_value

        self._interpolated_value = (self.points[i][1] - self.points[i - 1][1]) / (
                self.points[i][0] - self.points[i - 1][0]) * (
                                          x - self.points[i - 1][0]) + self.points[i - 1][1]
        return self._interpolated_value
