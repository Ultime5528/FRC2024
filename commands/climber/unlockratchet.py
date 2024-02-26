import wpilib

from subsystems.climber import Climber, RatchetState
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class UnlockRatchet(SafeCommand):
    delay = autoproperty(0.5)

    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.climber.unload()
        self.climber.unlockRatchet()

    def isFinished(self) -> bool:
        return (
            self.climber.ratchet_state == RatchetState.Unlocked
            or self.timer.get() >= self.delay
        )

    def end(self, interrupted: bool):
        self.climber.stop()
        self.timer.stop()

        if interrupted:
            self.climber.ratchet_state = RatchetState.Unknown
        else:
            self.climber.ratchet_state = RatchetState.Unlocked
