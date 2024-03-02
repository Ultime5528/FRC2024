import math
from typing import List

from commands2 import ConditionalCommand, Command
from wpilib import DriverStation
from wpimath.geometry import Pose2d, Rotation2d

from subsystems.drivetrain import Drivetrain
from utils.affinecontroller import AffineController
from utils.auto import eitherRedBlue
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def pose(x: float, y: float, deg: float) -> Pose2d:
    return Pose2d(x, y, Rotation2d.fromDegrees(deg))


class DriveToPoses(SafeCommand):
    max_speed = autoproperty(15.0)
    max_angular_speed = autoproperty(25.0)

    xy_p = autoproperty(0.4)
    xy_b = autoproperty(0.1)
    xy_tol_pos = autoproperty(0.5)
    xy_tol_pos_last = autoproperty(0.06)
    xy_tol_vel_last = autoproperty(10.0)
    xy_max = autoproperty(0.4)

    rot_p = autoproperty(0.008)
    rot_b = autoproperty(0.1)
    rot_tol_pos = autoproperty(10.0)
    rot_tol_pos_last = autoproperty(2.0)
    rot_tol_vel_last = autoproperty(10.0)
    rot_max = autoproperty(0.4)

    def __init__(self, drivetrain: Drivetrain, goals: List[Pose2d]):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.goals = goals

    @staticmethod
    def fromRedBluePoints(
        drivetrain: Drivetrain, red_poses: List[Pose2d], blue_poses: List[Pose2d]
    ) -> Command:
        return eitherRedBlue(
            DriveToPoses(drivetrain, red_poses),
            DriveToPoses(drivetrain, blue_poses),
        )

    def initialize(self):
        self.currGoal = 0
        currentGoal = self.goals[self.currGoal]

        self.pid_x = AffineController(self.xy_p, self.xy_b)
        self.pid_x.setTolerance(self.xy_tol_pos)
        self.pid_x.setMaximumOutput(self.xy_max)
        self.pid_x.setSetpoint(currentGoal.x)

        self.pid_y = AffineController(self.xy_p, self.xy_b)
        self.pid_y.setTolerance(self.xy_tol_pos)
        self.pid_y.setMaximumOutput(self.xy_max)
        self.pid_y.setSetpoint(currentGoal.y)

        self.pid_rot = AffineController(self.rot_p, self.rot_b)
        self.pid_rot.setTolerance(self.rot_tol_pos)
        self.pid_rot.setMaximumOutput(self.rot_max)
        self.pid_rot.enableContinuousInput(-180, 180)
        self.pid_rot.setSetpoint(currentGoal.rotation().degrees())

        if len(self.goals) == 1:
            self.setLastGoalSettings()

    def execute(self):
        current_pos = self.drivetrain.getPose()

        vel_x = self.pid_x.calculate(current_pos.x)
        vel_y = self.pid_y.calculate(current_pos.y)
        vel_rot = self.pid_rot.calculate(current_pos.rotation().degrees())

        self.drivetrain.driveRaw(
            vel_x * self.max_speed,
            vel_y * self.max_speed,
            vel_rot * self.max_angular_speed,
            True,
        )

        if (
            self.pid_x.atSetpoint()
            and self.pid_y.atSetpoint()
            and self.pid_rot.atSetpoint()
        ):
            self.currGoal += 1

            if self.currGoal < len(self.goals):
                print(len(self.goals) - 1, self.currGoal)

                currentGoal = self.goals[self.currGoal]
                self.pid_x.setSetpoint(currentGoal.x)
                self.pid_y.setSetpoint(currentGoal.y)
                self.pid_rot.setSetpoint(currentGoal.rotation().degrees())

                if self.currGoal == len(self.goals) - 1:
                    self.setLastGoalSettings()

    def end(self, interrupted):
        self.drivetrain.stop()

    def isFinished(self):
        return self.currGoal == len(self.goals)

    def setLastGoalSettings(self):
        self.pid_x.setTolerance(self.xy_tol_pos_last, self.xy_tol_vel_last)
        self.pid_y.setTolerance(self.xy_tol_pos_last, self.xy_tol_vel_last)
        self.pid_rot.setTolerance(self.rot_tol_pos_last, self.rot_tol_vel_last)
