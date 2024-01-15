import wpilib

from utils.property import autoproperty
from utils.safecommand import SafeCommand
from subsystems.drivetrain import Drivetrain


class DriveSquares(SafeCommand):
    line_duration = autoproperty(3)
    speed = autoproperty(0.25)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()

        self.drivetrain = drivetrain
        self.timer = wpilib.Timer()
        self.addRequirements(self.drivetrain)

    def initialize(self):
        self.timer.reset()
        self.timer.start()

    def execute(self):
        if 0 <= self.timer.get() < self.line_duration:
            self.drivetrain.drive(0.0, self.speed, 0.0)
        else:
            if self.line_duration <= self.timer.get() < (2 * self.line_duration):
                self.drivetrain.drive(self.speed, 0.0, 0.0)

            else:
                if (2 * self.line_duration) <= self.timer.get() < (3 * self.line_duration):
                    self.drivetrain.drive(0.0, -self.speed, 0.0)

                else:
                    if (3 * self.line_duration) <= self.timer.get() < (4 * self.line_duration):
                        self.drivetrain.drive(-self.speed, 0.0, 0.0)

                    else:
                        self.timer.restart()

    def isFinished(self):
        return False
