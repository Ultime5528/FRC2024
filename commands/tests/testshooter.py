from utils.fault import ErrorType
from utils.testcommand import TestCommand


class TestShooter(TestCommand):
    def __init__(self, shooter):
        super().__init__()
        self.addRequirements(shooter)
        self.shooter = shooter

    def initialize(self):
        if not self.shooter._right_motor.isAlive():
            self.shooter.registerFault("Right shooter motor connection timed out. Check right shooter motor connection.", ErrorType.ERROR)

        if not self.shooter._left_motor.isAlive():
            self.shooter.registerFault("Left shooter motor connection timed out. Check left shooter motor connection.", ErrorType.ERROR)

    def isFinished(self) -> bool:
        return True
