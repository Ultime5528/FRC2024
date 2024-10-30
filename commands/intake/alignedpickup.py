import commands2.parallelracegroup
from commands2 import ParallelDeadlineGroup, ParallelRaceGroup

from commands.intake.pickup import PickUp
from commands.vision.gotonote import GoToNote
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.vision2 import Vision2
from utils.safecommand import SafeMixin


class AlignedPickUp(SafeMixin, ParallelDeadlineGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        intake: Intake,
        vision: Vision2,
    ):
        super().__init__(
            PickUp(intake),
            GoToNote(drivetrain, vision)
        )