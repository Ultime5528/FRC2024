import wpilib

from subsystems.intake import Intake
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class Drop(SafeCommand):
    delay = autoproperty(1.5)

    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self) -> None:
        self.intake.drop()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool) -> None:
        self.intake.stop()
        self.timer.stop()
