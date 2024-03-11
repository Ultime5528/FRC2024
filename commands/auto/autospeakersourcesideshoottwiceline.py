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
from utils.property import autoproperty
from utils.safecommand import SafeMixin


class AutoSpeakerSourceSideShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
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
                MovePivotContinuous(pivot, vision),
                SequentialCommandGroup(
                    race(
                        PrepareAndShoot(shooter, pivot, intake),
                        AlignWithTag2D.toSpeaker(drivetrain, vision),
                    ),
                    deadline(
                        PickUp(intake),
                        DriveToPoses.fromRedBluePoints(
                            drivetrain,
                            [
                                pose(15, 4.1, 180),
                                pose(13.5, 4.1, 180),
                            ],
                            [
                                pose(1.541, 4.1, 0),
                                pose(3.041, 4.1, 0),
                            ],
                        ),
                    ),
                    DriveToPoses.fromRedBluePoints(
                        drivetrain, [pose(15, 4.1, -130)], [pose(1.541, 4.1, -50)]
                    ),
                    race(
                        PrepareAndShoot(shooter, pivot, intake),
                        AlignWithTag2D.toSpeaker(drivetrain, vision),
                    ),
                ),
            ),
        )