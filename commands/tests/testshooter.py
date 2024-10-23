from utils.fault import ErrorType
from utils.testcommand import TestCommand


class TestShooter(TestCommand):
    def __init__(self, shooter):
        super().__init__()
        self.addRequirements(shooter)
        self.shooter = shooter

    def isFinished(self) -> bool:
        return True
