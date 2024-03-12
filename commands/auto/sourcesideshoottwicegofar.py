import commands2
from commands2 import ParallelCommandGroup, SequentialCommandGroup
from commands2.cmd import race, deadline
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.pickup import PickUp
from commands.pivot.movepivot import MovePivot
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import PrepareAndShoot
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.auto import eitherRedBlue
from utils.safecommand import SafeMixin
from commands.auto.sourcesideshoottwiceline import (
    SourceSideShootTwiceLine,
)


class SourceSideShootTwiceGoFar(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            SourceSideShootTwiceLine(
                drivetrain, shooter, pivot, intake, vision
            ),
            deadline(
                PickUp(intake),
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [
                        pose(14.7524, 2.4291, -180),
                        pose(8.27, 0.7527, -180),
                    ],  # Point intermediaire 1
                    [pose(1.7885, 2.4291, 0), pose(8.27, 0.7527, 0)],
                ),
            ),
        )
