from utils.fault import ErrorType
from utils.testcommand import TestCommand


class TestClimber(TestCommand):
    def __init__(self, climber):
        super().__init__()
        self.addRequirements(climber)
        self.climber = climber

    def initialize(self):
        self.climber.registerFault("Test", ErrorType.WARNING)

    def isFinished(self) -> bool:
        return True
