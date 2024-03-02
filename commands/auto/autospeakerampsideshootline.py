import commands2
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetoposes import DriveToPoses
from commands.drivetrain.resetpose import ResetPose
from commands.pivot.movepivot import MovePivot
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import PrepareAndShoot
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from utils.auto import eitherRedBlue
from utils.safecommand import SafeMixin


class AutoSpeakerAmpSideShootLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake
    ):
        super().__init__(
            eitherRedBlue(
                ResetPose(
                    drivetrain,
                    Pose2d(15.86, 6.715, Rotation2d.fromDegrees(120)),
                ),
                ResetPose(
                    drivetrain,
                    Pose2d(0.681, 6.715, Rotation2d.fromDegrees(60)),
                ),
            ),
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            PrepareAndShoot(shooter, pivot, intake),
            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    Pose2d(15, 7, Rotation2d.fromDegrees(150)),
                    Pose2d(14, 7, Rotation2d.fromDegrees(180)),
                ],
                [
                    Pose2d(1.541, 7, Rotation2d.fromDegrees(30)),
                    Pose2d(2.541, 7, Rotation2d.fromDegrees(0)),
                ],
            ),
        )
