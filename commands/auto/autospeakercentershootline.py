import commands2
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetoposes import DriveToPoses
from commands.drivetrain.resetpose import ResetPose
from commands.pivot.movepivot import MovePivot
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import Shoot
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from utils.safecommand import SafeMixin


class AutoSpeakerCenterShootLine(SafeMixin, commands2.SequentialCommandGroup):

    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake
    ):
        super().__init__(
            ResetPose(drivetrain, Pose2d(15.20, 5.55, Rotation2d.fromDegrees(180))),
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            Shoot(shooter, pivot, intake),
            DriveToPoses(drivetrain, [Pose2d(14, 5.55, Rotation2d.fromDegrees(180))]),
        )
