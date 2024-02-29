import commands2
from commands2.cmd import parallel, sequence, race, deadline

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.load import Load
from commands.intake.pickup import PickUp
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import Shoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.auto import eitherRedBlue
from utils.property import autoproperty
from utils.safecommand import SafeMixin


class MegaModeAutonome(SafeMixin, commands2.SequentialCommandGroup):
    position_pivot = autoproperty(45)

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
                ResetPose(drivetrain, pose(15.2029, 5.553, 180)),
                ResetPose(drivetrain, pose(1.3381, 5.553, 0)),
            ),
            Shoot(shooter, pivot, intake),
            parallel(
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [pose(13.645, 5.553, 180)],
                    [pose(2.896, 5.553, 0)],
                ),
                ResetPivotDown(pivot),
                PickUp(intake),
            ),
            parallel(
                MovePivotContinuous(pivot, vision),
                sequence(
                    race(
                        PrepareShoot(shooter, pivot),
                        sequence(
                            DriveToPoses.fromRedBluePoints(
                                drivetrain,
                                [pose(14.1, 6.772, 153.36)],
                                [pose(2.441, 6.772, 26.64)],
                            ),
                            WaitShootSpeed(shooter),
                            Load(intake),
                        ),
                    ),
                    race(  # Second Note Taken Shoot
                        PrepareShoot(shooter, pivot),
                        sequence(
                            deadline(
                                PickUp(intake),
                                DriveToPoses.fromRedBluePoints(
                                    drivetrain,
                                    [
                                        pose(13, 8, 153.36),  # 13, 7
                                    ],
                                    [
                                        pose(3.5, 8, 26.64),  # 13, 7
                                    ],
                                ),
                            ),
                            DriveToPoses.fromRedBluePoints(
                                drivetrain,
                                [pose(14.1, 6.772, 153.36)],
                                [pose(3, 6.9, 26.64)]
                            ),
                            WaitShootSpeed(shooter),
                            Load(intake),
                        ),
                    ),
                ),
            ),
        )
