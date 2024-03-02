from typing import NewType

import wpilib

from subsystems.shooter import Shooter
from utils.property import autoproperty
from utils.safecommand import SafeCommand

NoReqShooter = NewType("NoReqShoot", Shooter)


class WaitShootSpeed(SafeCommand):
    delay = autoproperty(0.75)

    def __init__(self, shooter: NoReqShooter):
        super().__init__()
        self._shooter = shooter
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.reset()

    def execute(self):
        if self._shooter.hasReachedSpeed():
            self.timer.start()
        else:
            self.timer.stop()
            self.timer.reset()

    def isFinished(self) -> bool:
        return self._shooter.hasReachedSpeed()

    def end(self, interrupted: bool):
        self.timer.stop()
