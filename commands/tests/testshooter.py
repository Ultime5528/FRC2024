from wpilib import PowerDistribution

from utils.fault import Severity
from utils.testcommand import TestCommand


class TestShooter(TestCommand):
    def __init__(self, shooter, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(shooter)
        self.shooter = shooter

    def isFinished(self) -> bool:
        return True
