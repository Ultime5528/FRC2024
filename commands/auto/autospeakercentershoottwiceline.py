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


class AutoSpeakerCenterShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    position_pivot = autoproperty(45)

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
                    Pose2d(15.20, 5.55, Rotation2d.fromDegrees(0)),
                    [Pose2d(14, 5.55, Rotation2d.fromDegrees(0))]
                ),
                PickUp(intake),
                MovePivot.auto(pivot, self.position_pivot),
            ),
            ShootQuick(shooter, pivot, intake),
        )
