import wpilib

from subsystems.pivot import Pivot
from subsystems.shootervision import ShooterVision, getSpeakerTagIDFromAlliance
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class MovePivotContinuous(SafeCommand):
    threshold = autoproperty(1.0)

    def __init__(self, pivot: Pivot, vision: ShooterVision):
        super().__init__()
        self.pivot = pivot
        self.vision = vision
        self.addRequirements(pivot)

    def initialize(self):
        self.pivot.updateInterpolationPoints()

    def execute(self):
        if self.pivot.hasReset():
            target = self.vision.getTargetWithID(getSpeakerTagIDFromAlliance())
            if target:
                interpolated_value = self.pivot.getInterpolatedPosition(
                    target.getPitch()
                )
            else:
                interpolated_value = 57

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
