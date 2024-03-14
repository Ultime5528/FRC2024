import commands2
from commands2 import SequentialCommandGroup
from commands2.cmd import race, deadline
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.pickup import PickUp
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


class SourceSideShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
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
                    pose(15.783, 4.385, -120),
                ),
                ResetPose(
                    drivetrain,
                    pose(0.758, 4.385, -60),
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
                                pose(15, 3.844, -150),
                                pose(13.5, 3.844, -180),
                                pose(12.5, 3.144, -153),
                            ],
                            [
                                pose(1.541, 3.844, -30),
                                pose(3.041, 3.844, 0),
                                pose(4.041, 3.144, -27),
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
