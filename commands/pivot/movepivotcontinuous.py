import wpilib

from subsystems.pivot import Pivot
from subsystems.vision import Vision, getSpeakerTagIDFromAlliance
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class MovePivotContinuous(SafeCommand):
    threshold = autoproperty(1.0)

    def __init__(self, pivot: Pivot, vision: Vision):
        super().__init__()
        self.pivot = pivot
        self.vision = vision
        self.addRequirements(pivot)

    def execute(self):
        if self.pivot.hasReset():
            target = self.vision.getTargetWithID(getSpeakerTagIDFromAlliance())
            if target:
                interpolated_value = self.pivot.getInterpolatedPosition(
                    target.getPitch()
                )
                error = interpolated_value - self.pivot.getHeight()
                if abs(error) <= self.threshold:
                    self.pivot.maintain()
                elif error < 0:
                    self.pivot.moveDown()
                else:
                    self.pivot.moveUp()
        else:
            wpilib.reportError("Pivot has not reset: cannot MovePivotContinuous")

    def end(self, interrupted: bool):
        self.pivot.stop()
        self.pivot.state = Pivot.State.LockedInterpolation
