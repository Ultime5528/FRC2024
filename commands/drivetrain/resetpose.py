from wpimath.geometry import Pose2d

from subsystems.drivetrain import Drivetrain
from utils.safecommand import SafeCommand


class ResetPose(SafeCommand):
    def __init__(self, drivetrain: Drivetrain, pose: Pose2d):
        super().__init__()
        self.pose = pose
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        self.drivetrain.resetToPose(self.pose)

    def isFinished(self) -> bool:
        return True
