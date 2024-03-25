from typing import List

from commands2 import Command
from wpimath.geometry import Pose2d, Rotation2d, Translation2d

from subsystems.drivetrain import Drivetrain
from utils.auto import eitherRedBlue
from utils.property import autoproperty
from utils.safecommand import SafeCommand
from utils.trapezoidalmotion import TrapezoidalMotion


def pose(x: float, y: float, deg: float) -> Pose2d:
    return Pose2d(x, y, Rotation2d.fromDegrees(deg))


class DriveToPoses(SafeCommand):
    xy_accel = autoproperty(7.0)
    xy_speed_end = autoproperty(0.2)
    xy_tol_pos = autoproperty(0.5)
    xy_tol_pos_last = autoproperty(0.06)
    xy_speed_max = autoproperty(20.0)

    rot_accel = autoproperty(0.2)
    rot_speed_end = autoproperty(1.0)
    rot_tol_pos = autoproperty(10.0)
    rot_tol_pos_last = autoproperty(5.0)
    rot_speed_max = autoproperty(16.0)

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

    def updateMotions(self):
        current_goal = self.goals[self.currGoal]
        current_pose = self.drivetrain.getPose()
        self.trap_motion_xy = TrapezoidalMotion(
            start_speed=self.xy_speed_max,
            end_speed=self.xy_speed_end,
            max_speed=self.xy_speed_max,
            accel=self.xy_accel,
            start_position=(
                current_goal.translation() - current_pose.translation()
            ).norm(),
            end_position=0.0,
        )
        self.start_rotation = current_pose.rotation()
        self.trap_motion_rot = TrapezoidalMotion(
            start_speed=self.rot_speed_max,
            end_speed=self.rot_speed_end,
            max_speed=self.rot_speed_max,
            accel=self.rot_accel,
            start_position=0.0,
            end_position=((current_goal.rotation() - self.start_rotation).degrees()),
        )

    def initialize(self):
        self.currGoal = 0
        self.updateMotions()

    def execute(self):
        current_pos = self.drivetrain.getPose()
        translation_error = (
            self.goals[self.currGoal].translation() - current_pos.translation()
        )

        xy_mag = abs(self.trap_motion_xy.calculate(translation_error.norm()))
        vel_xy: Translation2d = translation_error * xy_mag / translation_error.norm()
        vel_rot = self.trap_motion_rot.calculate(
            (current_pos.rotation() - self.start_rotation).degrees()
        )
        print(vel_rot)
        self.drivetrain.driveRaw(
            vel_xy.X(),
            vel_xy.Y(),
            vel_rot,
            True,
        )

        if (
            self.currGoal < len(self.goals) - 1
            and self.isWithinTolerances()
            or self.currGoal == len(self.goals) - 1
            and self.isWithinLastTolerances()
        ):
            self.currGoal += 1

            if self.currGoal < len(self.goals):
                self.updateMotions()

    def end(self, interrupted):
        self.drivetrain.stop()

    def isFinished(self):
        return self.currGoal == len(self.goals)

    def isWithinLastTolerances(self) -> bool:
        return (
            self.trap_motion_xy.getRemainingDistance() <= self.xy_tol_pos_last
            and self.trap_motion_rot.getRemainingDistance() <= self.rot_tol_pos_last
        )

    def isWithinTolerances(self) -> bool:
        return (
            self.trap_motion_xy.getRemainingDistance() <= self.xy_tol_pos
            and self.trap_motion_rot.getRemainingDistance() <= self.rot_tol_pos
        )
