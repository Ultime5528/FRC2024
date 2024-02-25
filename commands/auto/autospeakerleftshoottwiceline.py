import commands2
from commands2 import ParallelCommandGroup
from wpimath.geometry import Pose2d, Rotation2d

from commands.intake.pickup import PickUp
from commands.pivot.resetpivotdown import ResetPivotDown
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeMixin
from commands.shooter.shoot import ShootQuick
from commands.pivot.movepivot import MovePivot
from commands.drivetoposes import DriveToPoses


class AutoSpeakerLeftShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    position_pivot = autoproperty(25)

    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake
    ):
        super().__init__(
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            ShootQuick(shooter, pivot, intake),
            ParallelCommandGroup(
                DriveToPoses(
                    drivetrain,
                    Pose2d(16.08 - 0.22, 6.33 + 0.385, Rotation2d.fromDegrees(-60)),
                    [Pose2d(15, 7, Rotation2d.fromDegrees(-30)),
                     Pose2d(14, 7, Rotation2d.fromDegrees(0))]
                ),
                PickUp(intake),
                MovePivot.auto(pivot, self.position_pivot),
            ),
            ShootQuick(shooter, pivot, intake),
        )
