from utils.fault import ErrorType
from utils.testcommand import TestCommand
import wpilib
from utils.property import autoproperty
import ports


class TestIntake(TestCommand):
    time_window = autoproperty(0.25)

    def __init__(self, intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self):
        if not self.intake._sensor.isAlive():
            self.intake.registerFault(
                "Intake sensor connection timed out. Check intake sensor connection.",
                ErrorType.ERROR,
            )

        if not self.intake._motor.isAlive():
            self.intake.registerFault(
                "Intake motor connection timed out. Check intake motor connection.",
                ErrorType.ERROR,
            )

        if self.intake.hasNote():
            self.intake.registerFault(
                "Sensor shouldn't detect object. Check for obstructions.",
                ErrorType.WARNING,
            )

    def isFinished(self) -> bool:
        return True
