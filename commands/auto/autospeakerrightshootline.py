import commands2
from wpimath.geometry import Pose2d, Rotation2d

from commands.pivot.resetpivotdown import ResetPivotDown
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeMixin
from commands.shooter.shoot import Shoot
from commands.pivot.movepivot import MovePivot
from commands.drivetoposes import DriveToPoses
from commands.drivetrain.resetpose import ResetPose


class AutoSpeakerRightShootLine(SafeMixin, commands2.SequentialCommandGroup):

    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake
    ):
        super().__init__(
            ResetPose(drivetrain, Pose2d(16.08 - 0.22, 4.77 - 0.385, Rotation2d.fromDegrees(-120))),
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            Shoot(shooter, pivot, intake),
            DriveToPoses(
                drivetrain,
                [Pose2d(15, 4.1, Rotation2d.fromDegrees(-150)),
                 Pose2d(14, 4.1, Rotation2d(-180))]
            ),
        )
