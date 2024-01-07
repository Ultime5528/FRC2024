from commands2 import InstantCommand

from subsystems.drivetrain import Drivetrain
from utils.safecommand import SafeCommand, SafeMixin


class ResetGyro(InstantCommand, SafeMixin):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def execute(self):
        self.drivetrain.resetGyro()
