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

from commands.auto.sourcesideshoot import SourceSideShoot
from subsystems.vision import Vision


class SourceSideShootLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            SourceSideShoot(drivetrain, shooter, pivot, intake, vision),
            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    Pose2d(15, 4.1, Rotation2d.fromDegrees(-150)),
                    Pose2d(14, 4.1, Rotation2d.fromDegrees(-180)),
                ],
                [
                    Pose2d(1.841, 4.1, Rotation2d.fromDegrees(-30)),
                    Pose2d(2.541, 4.1, Rotation2d.fromDegrees(0)),
                ],
            ),
        )
