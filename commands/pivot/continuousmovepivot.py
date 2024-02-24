import wpilib

from subsystems.pivot import Pivot
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class ContinuousMovePivot(SafeCommand):
    threshold = autoproperty(1.0)

    def __init__(self, pivot: Pivot):
        super().__init__()
        self.pivot = pivot

    def execute(self):
        if self.pivot.hasReset():
            if self.pivot.getInterpolatedPosition() is not None:
                error = self.pivot.getInterpolatedPosition() - self.pivot.getHeight()
                if abs(error) <= self.threshold:
                    self.pivot.setSpeed(0.2)
                elif error < 0:
                    self.pivot.moveDown()
                else:
                    self.pivot.moveUp()
        else:
            wpilib.reportError("Pivot has not reset: cannot ContinuousMovePivot")

    def end(self, interrupted: bool):
        self.pivot.state = Pivot.State.LockedInterpolation
