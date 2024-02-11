import math

from wpimath.controller import PIDController
from wpimath.geometry import Pose2d, Rotation2d

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


class DriveToPos(SafeCommand):
    xy_p = autoproperty(0.35)
    xy_i = autoproperty(0.0)
    xy_d = autoproperty(0.0)
    xy_tol_pos = autoproperty(0.04)
    xy_tol_vel = autoproperty(0.04)

    rot_p = autoproperty(0.0065)
    rot_i = autoproperty(0.0)
    rot_d = autoproperty(0.0)
    rot_tol_pos = autoproperty(0.047)
    rot_tol_vel = autoproperty(0.047)

    max_speed = autoproperty(1.0)

    def __init__(self, drivetrain: Drivetrain, goal: Pose2d):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.goal = goal

    def initialize(self):
        self.pid_x = PIDController(self.xy_p, self.xy_i, self.xy_d)
        self.pid_x.setTolerance(self.xy_tol_pos, self.xy_tol_vel)
        self.pid_x.setSetpoint(self.goal.x)

        self.pid_y = PIDController(self.xy_p, self.xy_i, self.xy_d)
        self.pid_y.setTolerance(self.xy_tol_pos, self.xy_tol_vel)
        self.pid_y.setSetpoint(self.goal.y)

        self.pid_rot = PIDController(self.rot_p, self.rot_i, self.rot_d)
        self.pid_rot.setTolerance(self.rot_tol_pos, self.rot_tol_vel)
        self.pid_rot.enableContinuousInput(-180, 180)
        self.pid_rot.setSetpoint(self.goal.rotation().degrees())

    def execute(self):
        current_pos = self.drivetrain.getPose()
        current_rot = self.drivetrain.getAngle()

        vel_x = self.pid_x.calculate(current_pos.x)
        vel_y = self.pid_y.calculate(current_pos.y)

        speed = math.sqrt(vel_x * vel_x + vel_y * vel_y)
        clamped_speed = clamp(speed, -self.max_speed, self.max_speed)

        new_vel_x = 0
        new_vel_y = 0
        if not math.isclose(speed, 0):
            speed_factor = clamped_speed / speed

            new_vel_x = vel_x * speed_factor
            new_vel_y = vel_y * speed_factor

        self.drivetrain.drive(
            new_vel_x, new_vel_y, -self.pid_rot.calculate(current_rot), True
        )

    def end(self, interrupted):
        self.drivetrain.drive(0, 0, 0, False)

    def isFinished(self):
        return (
            self.pid_x.atSetpoint()
            and self.pid_y.atSetpoint()
            and self.pid_rot.atSetpoint()
        )
