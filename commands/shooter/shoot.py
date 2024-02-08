from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from subsystems.shooter import Shooter
from commands2.parallelracegroup import ParallelRaceGroup
from commands2.sequentialcommandgroup import SequentialCommandGroup
from utils.safecommand import SafeMixin


class Shoot(SequentialCommandGroup, SafeMixin):
    def __init__(self, shooter: Shooter):
        super().__init__(
            ParallelRaceGroup(
                PrepareShoot(shooter),
                SequentialCommandGroup(
                    WaitShootSpeed(shooter),
                    #Load()
                )
            ),
            #MovePivot.toLoading()
        )