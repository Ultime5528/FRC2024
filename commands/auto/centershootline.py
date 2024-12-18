import commands2
from wpimath.geometry import Pose2d, Rotation2d

from commands.auto.centershoot import CenterShoot
from commands.drivetoposes import DriveToPoses
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.shootervision import ShooterVision
from utils.safecommand import SafeMixin


class CenterShootLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: ShooterVision,
    ):
        super().__init__(
            CenterShoot(drivetrain, shooter, pivot, intake, vision),
            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [Pose2d(14, 5.55, Rotation2d.fromDegrees(180))],
                [Pose2d(2.541, 5.55, Rotation2d.fromDegrees(0))],
            ),
        )
