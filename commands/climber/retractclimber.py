from utils.safecommand import SafeCommand
from subsystems.climber import Climber


class RetractClimber(SafeCommand):
    def __init__(self, climber: Climber):
        super().__init__()
        self._climber = climber
        self.addRequirements(climber)
        assert self.checkInvariants()

    def execute(self):
        assert self.checkInvariants()
        self._climber.retract()
        assert self.checkInvariants()

    def isFinished(self) -> bool:
        assert self.checkInvariants()
        return self._climber.isDown()

    def end(self, interrupted: bool):
        assert self.checkInvariants()
        self._climber.stop()
        assert self.checkInvariants()

    def checkInvariants(self) -> bool:
        assert self._climber
        assert self._climber in self.getRequirements()
        return True