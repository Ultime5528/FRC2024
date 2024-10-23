from utils.fault import ErrorType
from utils.testcommand import TestCommand


class TestClimber(TestCommand):
    def __init__(self, climber):
        super().__init__()
        self.addRequirements(climber)
        self.climber = climber

    def initialize(self):
        if not self.climber._motor.isAlive():
            self.climber.registerFault(
                "Climber motor connection timed out. Check climber motor connection.",
                ErrorType.ERROR,
            )

    def isFinished(self) -> bool:
        return True
