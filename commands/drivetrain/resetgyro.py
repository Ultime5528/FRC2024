from wpimath.geometry import Pose2d, Rotation2d

from subsystems.drivetrain import Drivetrain
from utils.safecommand import SafeCommand


class ResetGyro(SafeCommand):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        current = self.drivetrain.getPose()
        self.drivetrain.resetToPose(Pose2d(current.translation(), Rotation2d()))

    def isFinished(self) -> bool:
        return True
