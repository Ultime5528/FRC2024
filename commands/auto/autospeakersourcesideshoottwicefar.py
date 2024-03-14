import commands2
from commands2.cmd import deadline

from commands.auto.autospeakersourcesideshoottwiceline import (
    AutoSpeakerSourceSideShootTwiceLine,
)
from commands.drivetoposes import DriveToPoses, pose
from commands.intake.pickup import PickUp
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.safecommand import SafeMixin


class AutoSpeakerSourceSideShootTwiceFar(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            AutoSpeakerSourceSideShootTwiceLine(
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
