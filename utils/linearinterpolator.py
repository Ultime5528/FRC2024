from typing import List, Tuple, Optional, Union


class LinearInterpolator:
    def __init__(self, points: List[Tuple[float, float]]):
        self._points = points

    def interpolate(self, x):
        i = 1

        if x <= self._points[0][0]:
            return self._points[0][1]

        while i < len(self._points) and x > self._points[i][0]:
            i += 1

        if i == len(self._points):
            return self._points[i - 1][1]

        return (self._points[i][1] - self._points[i - 1][1]) / (
                self._points[i][0] - self._points[i - 1][0]
        ) * (x - self._points[i - 1][0]) + self._points[i - 1][1]
