from wpimath.geometry import Pose2d, Transform2d

from alignbase import AlignBase
from subsystems.drivetrain import Drivetrain


class DriveToPos(AlignBase):
    def __init__(self, drivetrain: Drivetrain, goal: Pose2d, relative: bool = False):
        super().__init__(drivetrain, False)
        self.drivetrain = drivetrain
        self.relative = relative
        self.local_goal = goal

    def computeGoal(self):
        if self.relative:
            pose = self.drivetrain.getPose()
            rel_goal = Pose2d(
                pose.x + self.local_goal.x,
                pose.y + self.local_goal.y,
                pose.rotation().rotateBy(self.local_goal.rotation()),
            )
            return rel_goal
        return self.local_goal
