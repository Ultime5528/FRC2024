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
from utils.auto import eitherRedBlue
from utils.property import autoproperty
from utils.safecommand import SafeMixin


class AutoSpeakerAmpSideShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
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
            eitherRedBlue(
                ResetPose(
                    drivetrain,
                    pose(15.86, 6.715, 120),
                ),
                ResetPose(
                    drivetrain,
                    pose(0.681, 6.715, 60),
                ),
            ),
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            Shoot(shooter, pivot, intake),
            ParallelCommandGroup(
                MovePivotContinuous(pivot, vision),
                SequentialCommandGroup(
                    deadline(
                        PickUp(intake),
                        DriveToPoses.fromRedBluePoints(
                            drivetrain,
                            [
                                Pose2d(15, 7, Rotation2d.fromDegrees(150)),
                                Pose2d(13.5, 7, Rotation2d.fromDegrees(180)),
                                pose(12.5, 8, 153),
                            ],
                            [
                                Pose2d(1.541, 7, Rotation2d.fromDegrees(30)),
                                Pose2d(3.041, 7, Rotation2d.fromDegrees(0)),
                                pose(4.041, 8, 27),
                            ]
                        ),
                    ),
                    DriveToPoses.fromRedBluePoints(
                        drivetrain,
                        [pose(15, 6.5, 153)],
                        [pose(1.541, 6.5, 27)]
                    ),
                    race(
                        Shoot(shooter, pivot, intake),
                        AlignWithTag2D.toSpeaker(drivetrain, vision),
                    ),
                ),
            ),
        )
