from commands2 import SequentialCommandGroup

from commands.climber.lockratchet import LockRatchet
from subsystems.climber import Climber
from utils.safecommand import SafeCommand, SafeMixin


class RetractClimber(SequentialCommandGroup, SafeMixin):
    def __init__(self, climber: Climber):
        super().__init__(LockRatchet(climber), _RetractClimber(climber))


class _RetractClimber(SafeCommand):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)

    def execute(self):
        self.climber.retract()

    def isFinished(self) -> bool:
        return self.climber.isDown()

    def end(self, interrupted: bool):
        self.climber.stop()
