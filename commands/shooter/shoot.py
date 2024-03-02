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


class Shoot(SafeMixin, SequentialCommandGroup):
    def __init__(self, shooter: Shooter, intake: Intake):
        super().__init__(
            WaitShootSpeed(shooter),
            Load(intake),
        )

class PrepareAndShoot(SafeMixin, ParallelRaceGroup):
    def __init__(self, shooter: Shooter, pivot: Pivot, intake: Intake):
        super().__init__(
            PrepareShoot(shooter, pivot),
            Shoot(shooter, intake),
        )


class PrepareAndShootAndMovePivotLoading(SafeMixin, SequentialCommandGroup):
    """
    La commande Shoot ne requiert pas le Pivot, il lit seulement sa hauteur.

    Pendant qu'on tire, on veut qu'en arrière-plan, la commande par défaut MaintainPivot
    s'exécute.

    À la toute fin, on veut faire un MovePivot. Proxy est nécessaire
    pour que le Pivot ne soit pas dans les requirements et que le Maintain poursuive de
    s'exécute pendant le Shoot.

    """

    def __init__(self, shooter: Shooter, pivot: Pivot, intake: Intake):
        super().__init__(
            PrepareAndShoot(shooter, pivot, intake),
            ProxyCommand(MovePivot.toLoading(pivot)),
        )
