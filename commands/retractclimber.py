from utils.safecommand import SafeCommand
from subsystems.climber import Climber


class RetractClimber(SafeCommand):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber

    def execute(self):
        self.climber.retract()

    def isFinished(self) -> bool:
        self.climber.isDown()

    def end(self, interrupted: bool):
        self.climber.stop()

