import commands2
from commands2.cmd import parallel, race
from wpimath.geometry import Pose2d, Rotation2d

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

from commands.pivot.movepivotcontinuous import MovePivotContinuous
from subsystems.vision import Vision
from commands.vision.alignwithtag2d import AlignWithTag2D


class CenterShoot(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake, vision: Vision
    ):
        super().__init__(
            eitherRedBlue(
                ResetPose(drivetrain, Pose2d(15.20, 5.55, Rotation2d.fromDegrees(180))),
                ResetPose(drivetrain, Pose2d(1.341, 5.55, Rotation2d.fromDegrees(0))),
            ),
            ResetPivotDown(pivot),
            race(
                PrepareAndShoot(shooter, pivot, intake),
                MovePivotContinuous(pivot, vision),
                AlignWithTag2D.toSpeaker(drivetrain, vision)
            )
        )