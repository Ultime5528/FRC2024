from commands2 import ParallelCommandGroup
from commands2.button import CommandXboxController

from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.shooter.prepareshoot import PrepareShoot
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.shootervision import ShooterVision
from utils.safecommand import SafeMixin


class AlignEverything(SafeMixin, ParallelCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        pivot: Pivot,
        shooter: Shooter,
        vision: ShooterVision,
        xbox_remote: CommandXboxController,
    ):
        super().__init__(
            AlignWithTag2D.toSpeaker(drivetrain, vision, xbox_remote),
            MovePivotContinuous(pivot, vision),
            PrepareShoot(shooter, pivot),
        )
