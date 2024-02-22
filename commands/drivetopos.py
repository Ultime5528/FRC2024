from wpimath.geometry import Pose2d

from alignbase import AlignBase
from subsystems.drivetrain import Drivetrain


class DriveToPos(AlignBase):
    def __init__(self, drivetrain: Drivetrain, goal: Pose2d):
        super().__init__(drivetrain, False)
        self.goal = goal

    def computeGoal(self):
        return self.goal
