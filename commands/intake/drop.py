import wpilib

from subsystems.intake import Intake
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class Drop(SafeCommand):
    delay = autoproperty(3.0)

    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.reset()

    def execute(self) -> None:
        self.intake.drop()
        if not self.intake.hasNote():
            self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool) -> None:
        self.intake.stop()
        self.timer.stop()
