from typing import NewType

from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from utils.property import autoproperty
from utils.safecommand import SafeCommand

NoReqPivot = NewType("NoReqPivot", Pivot)


class PrepareShoot(SafeCommand):
    speed_amp = autoproperty(1350.0)
    speed_max = autoproperty(5200.0)

    def __init__(self, shooter: Shooter, pivot: NoReqPivot):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(shooter)
        self.pivot = pivot

    def execute(self):
        if self.pivot.state == Pivot.State.Amp:
            self.shooter.shoot(rpm=self.speed_amp)
        else:
            self.shooter.shoot(rpm=self.speed_max)

    def end(self, interrupted: bool):
        self.shooter.stop()
