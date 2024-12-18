import commands2
from commands2.cmd import race
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetrain.resetpose import ResetPose
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import PrepareAndShoot
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.shootervision import ShooterVision
from utils.auto import eitherRedBlue
from utils.safecommand import SafeMixin


class SourceSideShoot(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: ShooterVision,
    ):
        super().__init__(
            eitherRedBlue(
                ResetPose(
                    drivetrain,
                    Pose2d(15.86, 4.385, Rotation2d.fromDegrees(-120)),
                ),
                ResetPose(
                    drivetrain,
                    Pose2d(0.681, 4.385, Rotation2d.fromDegrees(-60)),
                ),
            ),
            ResetPivotDown(pivot),
            race(
                PrepareAndShoot(shooter, pivot, intake),
                MovePivotContinuous(pivot, vision),
                AlignWithTag2D.toSpeaker(drivetrain, vision),
            ),
        )
