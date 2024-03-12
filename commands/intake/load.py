import wpilib

from subsystems.intake import Intake
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class Load(SafeCommand):
    delay = autoproperty(0.25)

    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.reset()

    def execute(self):
        self.intake.load()
        if not self.intake.hasNote():
            self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        self.intake.stop()
        self.timer.stop()
