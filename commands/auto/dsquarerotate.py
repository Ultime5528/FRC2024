import wpilib

from utils.property import autoproperty
from utils.safecommand import SafeCommand
from subsystems.drivetrain import Drivetrain


class DriveSquaresRotate(SafeCommand):
    line_duration = autoproperty(1.0)
    speed = autoproperty(0.25)
    rotate_speed = autoproperty(0.25)

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
            self.drivetrain.drive(0.0, self.speed, self.rotate_speed)
        else:
            if self.line_duration <= self.timer.get() < (2 * self.line_duration):
                self.drivetrain.drive(self.speed, 0.0, self.rotate_speed)

            else:
                if (2 * self.line_duration) <= self.timer.get() < (3 * self.line_duration):
                    self.drivetrain.drive(0.0, -self.speed, self.rotate_speed)

                else:
                    if (3 * self.line_duration) <= self.timer.get() < (4 * self.line_duration):
                        self.drivetrain.drive(-self.speed, 0.0, self.rotate_speed)

                    else:
                        self.timer.restart()

    def isFinished(self):
        return False
