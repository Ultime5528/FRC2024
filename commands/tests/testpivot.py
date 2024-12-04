import wpilib
from wpilib import PowerDistribution

import ports
from subsystems.pivot import Pivot
from utils.fault import Severity
from utils.property import FloatProperty, autoproperty
from utils.testcommand import TestCommand


class TestPivot(TestCommand):
    time_window = autoproperty(0.25)
    def __init__(self, pivot: Pivot, pdp: PowerDistribution):
        super().__init__()
        self.pdp = pdp
        self.addRequirements(pivot)
        self.pivot = pivot
        self.pivot_current = ports.current_pivot_motor
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()
        self.first_pivot_current = self.pdp.getCurrent(self.pivot_current)
        self.first_pivot_velocity = self.pivot._encoder.get()

    def execute(self):
        if self.pivot.isUp():
            self.pivot.moveUp()
        else:
            self.pivot.moveUp()

    def isFinished(self) -> bool:
        return self.time_window <= self.timer.get()

    def end(self, interrupted: bool):
        if self.pdp.getCurrent(self.pivot_current) <= self.first_pivot_current:
            self.pivot.registerFault(
                "Pivot motor timed out. Check for connections", Severity.ERROR
            )
        if self.pivot._encoder.get() <= self.first_pivot_velocity:
            self.pivot.registerFault("Pivot encoder timed out. Check for connections", Severity.ERROR)

        self.pivot.stop()
