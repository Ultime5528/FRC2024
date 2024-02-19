import commands2

from subsystems.drivetrain import Drivetrain


class ResetGyro(commands2.InstantCommand):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        self.drivetrain.resetGyro()

    def isFinished(self) -> bool:
        return True
