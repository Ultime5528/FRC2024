import commands2
from commands2.cmd import deadline
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

from commands.pivot.movepivotcontinuous import MovePivotContinuous
from subsystems.vision import Vision
from commands.vision.alignwithtag2d import AlignWithTag2D
from commands.auto.autospeakerampsideshoot import AutoSpeakerAmpSideShoot

class AutoSpeakerAmpSideShootLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake, vision: Vision
    ):
        super().__init__(
            AutoSpeakerAmpSideShoot(drivetrain, shooter, pivot, intake, vision),
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
