import math

import wpilib

from utils.safecommand import SafeCommand
from subsystems.shooter import Shooter
from utils.property import autoproperty
from subsystems.pivot import Pivot
from commands.pivot.movepivot import properties


class PrepareShoot(SafeCommand):
    speed_far = autoproperty(1)
    speed_close = autoproperty(0.5)
    speed_amp = autoproperty(0.25)

    def __init__(self, shooter: Shooter, pivot: Pivot):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(shooter)
        self.pivot = pivot

    def execute(self):
        if self.pivot.state == Pivot.State.SpeakerFar:
            self.shooter.shoot(rpm=self.speed_far)
        elif self.pivot.state == Pivot.State.SpeakerClose:
            self.shooter.shoot(rpm=self.speed_close)
        elif self.pivot.state == Pivot.State.Amp:
            self.shooter.shoot(rpm=self.speed_amp)
        else:
            self.shooter.stop()
            wpilib.reportError(f"Can't shoot while in position ({self.pivot.state})")

    def end(self, interrupted: bool):
        self.shooter.stop()
