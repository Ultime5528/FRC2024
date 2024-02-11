import wpilib

from subsystems.intake import Intake
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class PickUp(SafeCommand):
    delay = autoproperty(1.0)

    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()

    def execute(self) -> None:
        self.intake.pickUp()
        if self.intake.hasNote():
            self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool) -> None:
        self.timer.stop()
        self.intake.stop()
