from commands2 import SequentialCommandGroup

from commands.climber.lockratchet import LockRatchet
from commands.climber.unlockratchet import UnlockRatchet
from subsystems.climber import Climber
from utils.safecommand import SafeCommand, SafeMixin


class ExtendClimber(SequentialCommandGroup, SafeMixin):
    def __init__(self, climber: Climber):
        super().__init__(UnlockRatchet(climber), _ExtendClimber(climber))


class _ExtendClimber(SafeCommand):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)

    def execute(self):
        self.climber.extend()

    def isFinished(self) -> bool:
        return self.climber.isUp()

    def end(self, interrupted: bool):
        self.climber.stop()
