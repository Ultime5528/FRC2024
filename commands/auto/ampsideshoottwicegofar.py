import commands2
from commands2.cmd import deadline

from commands.auto.ampsideshoottwiceline import (
    AmpSideShootTwiceLine,
)
from commands.drivetoposes import DriveToPoses, pose
from commands.intake.pickup import PickUp
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.shootervision import ShooterVision
from utils.safecommand import SafeMixin


class AmpSideShootTwiceGoFar(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: ShooterVision,
    ):
        super().__init__(
            AmpSideShootTwiceLine(drivetrain, shooter, pivot, intake, vision),
            deadline(
                PickUp(intake),
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [
                        pose(14.7524, 6.85, -180),
                        pose(8.27, 6.85, -180),
                    ],
                    [pose(1.7885, 6.85, 0), pose(8.27, 6.85, 0)],
                ),
            ),
        )
