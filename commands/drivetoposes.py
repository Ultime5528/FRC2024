import math
from typing import List

import wpilib
from wpimath.geometry import Pose2d, Rotation2d

from subsystems.drivetrain import Drivetrain
from utils.affinecontroller import AffineController
from utils.alignbaseutils import clamp
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class DriveToPoses(SafeCommand):
    xy_p = autoproperty(0.4)
    xy_b = autoproperty(0.08)
    xy_tol_pos = autoproperty(0.5)
    xy_tol_pos_last = autoproperty(0.06)
    xy_tol_vel_last = autoproperty(0.1)

    rot_p = autoproperty(0.008)
    rot_b = autoproperty(0.08)
    rot_tol_pos = autoproperty(10.0)
    rot_tol_pos_last = autoproperty(2.0)
    rot_tol_vel_last = autoproperty(1.0)

    max_speed = autoproperty(1.0)

    def __init__(self, drivetrain: Drivetrain, goals_red_alliance: List[Pose2d]):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.goals = goals_red_alliance

    def initialize(self):
        alliance = wpilib.DriverStation.getAlliance()
        if alliance == wpilib.DriverStation.Alliance.kRed:
            pass
        elif alliance == wpilib.DriverStation.Alliance.kBlue:
            for i in range(len(self.goals)):
                current = self.goals[i]
                # field dimensions: 16.541, 8.211
                new_goal = Pose2d(
                    16.541 - current.x,
                    current.y,
                    Rotation2d.fromDegrees(180.0 - current.rotation().degrees()),
                )
                self.goals[i] = new_goal
        else:
            wpilib.reportError("Alliance is invalid")
        self.currGoal = 0
        currentGoal = self.goals[self.currGoal]

        self.pid_x = AffineController(self.xy_p, self.xy_b)
        self.pid_x.setTolerance(self.xy_tol_pos)
        self.pid_x.setSetpoint(currentGoal.x)

        self.pid_y = AffineController(self.xy_p, self.xy_b)
        self.pid_y.setTolerance(self.xy_tol_pos)
        self.pid_y.setSetpoint(currentGoal.y)

        self.pid_rot = AffineController(self.rot_p, self.rot_b)
        self.pid_rot.setTolerance(self.rot_tol_pos)
        self.pid_rot.enableContinuousInput(-180, 180)
        self.pid_rot.setSetpoint(currentGoal.rotation().degrees())

    def execute(self):
        current_pos = self.drivetrain.getPose()

        vel_x = self.pid_x.calculate(current_pos.x)
        vel_y = self.pid_y.calculate(current_pos.y)
        vel_rot = self.pid_rot.calculate(current_pos.rotation().degrees())

        speed = math.hypot(vel_x, vel_y)

        if not math.isclose(speed, 0):
            clamped_speed = clamp(speed, -self.max_speed, self.max_speed)
            speed_factor = clamped_speed / speed

            new_vel_x = vel_x * speed_factor
            new_vel_y = vel_y * speed_factor

            self.drivetrain.drive(
                new_vel_x,
                new_vel_y,
                vel_rot,
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
                if self.currGoal == len(self.goals) - 1:
                    self.pid_x.setTolerance(self.xy_tol_pos_last, self.xy_tol_vel_last)
                    self.pid_y.setTolerance(self.xy_tol_pos_last, self.xy_tol_vel_last)
                    self.pid_rot.setTolerance(
                        self.rot_tol_pos_last, self.rot_tol_vel_last
                    )

                currentGoal = self.goals[self.currGoal]
                self.pid_x.setSetpoint(currentGoal.x)
                self.pid_y.setSetpoint(currentGoal.y)
                self.pid_rot.setSetpoint(currentGoal.rotation().degrees())

    def end(self, interrupted):
        self.drivetrain.stop()

    def isFinished(self):
        return self.currGoal == len(self.goals)
