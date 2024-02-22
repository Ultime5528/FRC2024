from commands2 import ProxyCommand
from commands2.parallelracegroup import ParallelRaceGroup
from commands2.sequentialcommandgroup import SequentialCommandGroup

from commands.intake.load import Load
from commands.pivot.movepivot import MovePivot
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from utils.safecommand import SafeMixin


class ShootQuick(ParallelRaceGroup, SafeMixin):
    def __init__(self, shooter: Shooter, pivot: Pivot, intake: Intake):
        super().__init__(
            ParallelRaceGroup(
                PrepareShoot(shooter, pivot),
                SequentialCommandGroup(WaitShootSpeed(shooter), Load(intake)),
            )
        )


class Shoot(SequentialCommandGroup, SafeMixin):
    def __init__(self, shooter: Shooter, pivot: Pivot, intake: Intake):
        super().__init__(
            ShootQuick(shooter, pivot, intake),
            ProxyCommand(MovePivot.toLoading(pivot)),
        )
