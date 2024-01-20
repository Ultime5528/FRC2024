import wpilib

from utils.property import autoproperty
from utils.safecommand import SafeCommand
from subsystems.drivetrain import Drivetrain
from commands.drive import Drive


class DriveSquaresPauses(SafeCommand):
    line_duration = autoproperty(1.0)
    speed = autoproperty(0.25)
    pause = autoproperty(1.0)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()

        self.drivetrain = drivetrain
        self.timer = wpilib.Timer()
        self.addRequirements(self.drivetrain)

    def initialize(self):
        self.timer.reset()
        self.timer.start()

    def execute(self):
        if self.pause <= self.timer.get() < (self.line_duration + self.pause):
            self.drivetrain.drive(0.0, self.speed, 0.0)
        else:
            if (self.line_duration + 2 * self.pause) <= self.timer.get() < (2 * self.line_duration + 2 * self.pause):
                self.drivetrain.drive(self.speed, 0.0, 0.0)

            else:
                if (2 * self.line_duration + 3 * self.pause) <= self.timer.get() < (
                        3 * (self.line_duration + self.pause)
                ):
                    self.drivetrain.drive(0.0, -self.speed, 0.0)

                else:
                    if (3 * self.line_duration + 4 * self.pause) <= self.timer.get() < (
                            4 * (self.line_duration + self.pause)
                    ):
                        self.drivetrain.drive(-self.speed, 0.0, 0.0)

                    else:
                        if (4 * self.line_duration + 4 * self.pause) <= self.timer.get():
                            self.timer.reset()

                        else:
                            pass

    def isFinished(self):
        return False
