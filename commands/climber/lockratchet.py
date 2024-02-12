import wpilib

from subsystems.climber import Climber
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class LockRatchet(SafeCommand):
    delay = autoproperty(0.5)

    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.climber.lockRatchet()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        self.timer.stop()
