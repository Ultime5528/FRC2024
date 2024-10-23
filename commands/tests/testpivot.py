from utils.fault import ErrorType
from utils.testcommand import TestCommand


class TestPivot(TestCommand):
    def __init__(self, pivot):
        super().__init__()
        self.addRequirements(pivot)
        self.pivot = pivot

    def initialize(self):
        if not self.pivot._motor.isAlive():
            self.pivot.registerFault(
                "Pivot motor connection timed out. Check pivot motor connection.",
                ErrorType.ERROR,
            )

    def isFinished(self) -> bool:
        return True
