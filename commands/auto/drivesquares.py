import wpilib

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class DriveSquares(SafeCommand):
    line_duration = autoproperty(1.0)
    speed = autoproperty(0.6)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()

        self.drivetrain = drivetrain
        self.timer = wpilib.Timer()
        self.addRequirements(self.drivetrain)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        if self.timer.get() < self.line_duration:
            self.drivetrain.drive(0.0, self.speed, 0.0, is_field_relative=False)
        elif self.timer.get() < 2 * self.line_duration:
            self.drivetrain.drive(self.speed, 0.0, 0.0, is_field_relative=False)
        elif self.timer.get() < 3 * self.line_duration:
            self.drivetrain.drive(0.0, -self.speed, 0.0, is_field_relative=False)
        elif self.timer.get() < 4 * self.line_duration:
            self.drivetrain.drive(-self.speed, 0.0, 0.0, is_field_relative=False)
        else:
            self.timer.restart()

    def isFinished(self):
        return False

    def end(self, interrupted: bool):
        self.drivetrain.stop()
