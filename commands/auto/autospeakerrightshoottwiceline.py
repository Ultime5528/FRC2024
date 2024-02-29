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
from commands.shooter.shoot import Shoot
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.property import autoproperty
from utils.safecommand import SafeMixin


class AutoSpeakerRightShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    position_pivot = autoproperty(25)

    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            ResetPose(
                drivetrain,
                Pose2d(16.08 - 0.22, 4.77 - 0.385, Rotation2d.fromDegrees(-120)),
            ),
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            Shoot(shooter, pivot, intake),
            ParallelCommandGroup(
                MovePivotContinuous(pivot, vision),
                SequentialCommandGroup(
                    deadline(
                        PickUp(intake),
                        DriveToPoses(
                            drivetrain,
                            [
                                pose(15, 4.1, 180),
                                pose(13.5, 4.1, 180),
                            ],
                        ),
                    ),
                    DriveToPoses(drivetrain, [pose(15, 4.1, -130)]),
                    race(
                        Shoot(shooter, pivot, intake),
                        AlignWithTag2D.toSpeaker(drivetrain, vision),
                    ),
                ),
            ),
        )
