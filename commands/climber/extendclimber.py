from utils.safecommand import SafeCommand
from subsystems.climber import Climber


class ExtendClimber(SafeCommand):
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
