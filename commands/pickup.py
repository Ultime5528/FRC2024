import wpilib

from subsystems.intake import Intake
from utils.safecommand import SafeCommand
import ports


class PickUp(SafeCommand):
    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake

    def execute(self) -> None:
        self.intake.pickUp()

    def isFinished(self) -> bool:
        return self.intake.hasNote()

    def end(self, interrupted: bool) -> None:
        self.intake.stop()
