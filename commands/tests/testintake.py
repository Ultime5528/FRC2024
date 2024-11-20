from wpilib import PowerDistribution
import ports
from subsystems.intake import Intake

from utils.fault import ErrorType
from utils.testcommand import TestCommand
import wpilib
from utils.property import autoproperty


class TestIntake(TestCommand):
    time_window = autoproperty(0.25)
    max_temp = autoproperty(50)

    def __init__(self, intake: Intake, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.pdp = pdp
        self.intake_current = ports.current_intake_motor
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.start()
        self.first_current = self.pdp.getCurrent(self.intake_current)

        if self.intake.hasNote():
            self.intake.registerFault(
                "Sensor shouldn't detect object. Check for obstructions.",
                ErrorType.WARNING,
            )

    def execute(self):
        self.intake.load()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.time_window

    def end(self, interrupted: bool):
        if self.pdp.getCurrent(self.intake_current) <= self.first_current:
            self.intake.registerFault(
                "Intake motor timed out. Check for connections", ErrorType.ERROR
            )
        self.intake.stop()
