from utils.fault import Severity
from utils.testcommand import TestCommand


class TestClimber(TestCommand):
    def __init__(self, climber):
        super().__init__()
        self.addRequirements(climber)
        self.climber = climber

    def isFinished(self) -> bool:
        return True
