from subsystems.drivetrain import Drivetrain
from utils.safecommand import SafeCommand


class ResetGyro(SafeCommand):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        self.drivetrain.resetGyro()

    def isFinished(self) -> bool:
        return True
