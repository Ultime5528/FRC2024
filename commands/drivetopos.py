import math

from wpimath.controller import PIDController
from wpimath.geometry import Pose2d, Rotation2d

from alignbase import AlignBase
from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class DriveToPos(AlignBase):

    def __init__(self, drivetrain: Drivetrain, goal: Pose2d):
        super().__init__(False, drivetrain)
        self.goal = goal

    def computeGoal(self):
        return self.goal
