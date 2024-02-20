from commands2 import ProxyCommand

from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from subsystems.shooter import Shooter
from commands2.parallelracegroup import ParallelRaceGroup
from commands2.sequentialcommandgroup import SequentialCommandGroup
from utils.safecommand import SafeMixin
from subsystems.pivot import Pivot
from commands.pivot.movepivot import MovePivot
from subsystems.intake import Intake
from commands.intake.load import Load


class Shoot(SequentialCommandGroup, SafeMixin):
    def __init__(self, shooter: Shooter, pivot: Pivot, intake: Intake):
        super().__init__(
            ParallelRaceGroup(
                PrepareShoot(shooter, pivot),
                SequentialCommandGroup(WaitShootSpeed(shooter), Load(intake)),
            ),
            ProxyCommand(MovePivot.toLoading(pivot)),
        )
