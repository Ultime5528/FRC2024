import commands2
from commands2.cmd import parallel, sequence, race, deadline

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.load import Load
from commands.intake.pickup import PickUp
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import PrepareAndShoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.auto import eitherRedBlue
from utils.property import autoproperty
from utils.safecommand import SafeMixin
from commands.vision.alignwithtag2d import AlignWithTag2D

class FarModeautonome(SafeMixin, commands2.SequentialCommandGroup):
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
                    pose(15.86, 4.385, -120),
                ),
                ResetPose(
                    drivetrain,
                    pose(0.681, 4.385, -60),
                ),
            ),

            PrepareAndShoot(shooter, pivot, intake),
            parallel(
                ResetPivotDown(pivot),
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [pose(14.7524, 2.4291, -165.5)],  # Point intermediere 1
                    [pose(1.7885, 2.4291, -14.5)]
                )
            ),
            parallel(
                MovePivotContinuous(pivot, vision),
                sequence(
                    deadline(
                        PickUp(intake),
                        DriveToPoses.fromRedBluePoints(
                            drivetrain,
                            [pose(8.27, 0.7527, -165.5)],  # first note taken
                            [pose(8.27, 0.7527, -14.5)]
                        )
                    ),

                    race(
                        PrepareShoot(shooter, pivot),
                        sequence(
                            DriveToPoses.fromRedBluePoints(
                                drivetrain,
                                [pose(14.77524, 2.4291, -120)],
                                [pose(1.7658, 2.4291, -60)],
                            ),
                            race(
                                AlignWithTag2D.toSpeaker(drivetrain, vision),  # first note shooted
                                sequence(
                                    WaitShootSpeed(shooter),
                                    Load(intake)
                                )
                            )
                        )
                    ),

                    DriveToPoses.fromRedBluePoints(
                        drivetrain,
                        [pose(10.69, 1.37, 156.581)],
                        [pose(5.85, 1.37, 23.41)]
                    ),
                    deadline(
                        PickUp(intake),
                        DriveToPoses.fromRedBluePoints(
                            drivetrain,
                            [pose(8.27, 2.4291, 156.581)],  # second note taken
                            [pose(8.27, 2.4291, 23.41)]
                        )
                    ),

                    race(
                        PrepareShoot(shooter, pivot),
                        sequence(
                            DriveToPoses.fromRedBluePoints(
                                drivetrain,
                                [pose(10.69, 1.37, -119.64),
                                 pose(14.75, 2.4291, -119.64)],
                                [pose(5.85, 1.37, -60),
                                 pose(1.79, 2.4291, -60)],
                            ),
                            race(
                                AlignWithTag2D.toSpeaker(drivetrain, vision),  # second note shooted
                                sequence(
                                    WaitShootSpeed(shooter),
                                    Load(intake)
                                )
                            )
                        )
                    ),
                )
            )
        )