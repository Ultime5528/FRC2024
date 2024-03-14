import commands2
from commands2.cmd import deadline

from commands.auto.autospeakerampsideshoottwiceline import (
    AutoSpeakerAmpSideShootTwiceLine,
)
from commands.drivetoposes import DriveToPoses, pose
from commands.intake.pickup import PickUp
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.safecommand import SafeMixin


class AutoSpeakerAmpSideShootTwiceFar(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            AutoSpeakerAmpSideShootTwiceLine(
                drivetrain, shooter, pivot, intake, vision
            ),
            deadline(
                PickUp(intake),
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [
                        pose(14.7524, 7.4583, -180),
                        pose(8.27, 7.4583, -180),
                    ],
                    [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
                ),
            ),
        )
