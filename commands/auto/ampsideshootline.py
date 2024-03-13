import commands2
from wpimath.geometry import Pose2d, Rotation2d

from commands.auto.ampsideshoot import AmpSideShoot
from commands.drivetoposes import DriveToPoses
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.safecommand import SafeMixin


class AmpSideShootLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            AmpSideShoot(drivetrain, shooter, pivot, intake, vision),
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
