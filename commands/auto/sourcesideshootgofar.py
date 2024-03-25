import commands2
from commands2.cmd import parallel

from commands.auto.sourcesideshoot import SourceSideShoot
from commands.drivetoposes import DriveToPoses, pose
from commands.intake.pickup import PickUp
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.safecommand import SafeMixin


class SourceSideShootGoFar(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            SourceSideShoot(drivetrain, shooter, pivot, intake, vision),
            parallel(
                PickUp(intake),
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [pose(15.86, 1.245, -120), pose(8.15, 0.745, -180)],
                    [pose(0.681, 1.245, -60), pose(8.39, 0.745, 0)],
                ),
            ),
        )
