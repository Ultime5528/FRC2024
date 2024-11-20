import wpilib
from wpilib import PowerDistribution

import ports
from utils.fault import ErrorType
from utils.testcommand import TestCommand


class TestPivot(TestCommand):
    def __init__(self, pivot, pdp: PowerDistribution):
        super().__init__()
        self.pdp = pdp
        self.addRequirements(pivot)
        self.pivot = pivot
        self.pivot_current = ports.current_pivot_motor
        self.timer = wpilib.Timer

    def initialize(self):
        self.timer.start()
        self.first_current = self.pdp.getCurrent(self.pivot_current)

    #    def execute(self):
    #        self.pivot.

    def isFinished(self) -> bool:
        return True
