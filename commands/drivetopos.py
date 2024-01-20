import math

from wpimath.controller import PIDController
from wpimath.geometry import Pose2d, Rotation2d

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def clamp(x, mini, maxi):
    return max(mini, min(x, maxi))

class DriveToPos(SafeCommand):
    xy_p = autoproperty(0.5)
    xy_i = autoproperty(0.5)
    xy_d = autoproperty(0.5)
    xy_tol_pos = autoproperty(0.5)
    xy_tol_vel = autoproperty(0.5)

    rot_p = autoproperty(0.5)
    rot_i = autoproperty(0.5)
    rot_d = autoproperty(0.5)
    rot_tol_pos = autoproperty(0.5)
    rot_tol_vel = autoproperty(0.5)

    max_speed = autoproperty(0.5)

    def __init__(self, drivetrain: Drivetrain, goal: Pose2d, goalAngle: Rotation2d):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.goal = goal
        self.angle = goalAngle

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
        self.pid_rot.setSetpoint(self.angle.degrees())

    def execute(self):
        current_pos = self.drivetrain.getPose()

        vel_x = self.pid_x.calculate(current_pos.x)
        vel_y = self.pid_y.calculate(current_pos.y)

        speed = math.sqrt(vel_x*vel_x + vel_y*vel_y)
        clamped_speed = clamp(speed, -self.max_speed, self.max_speed)

        if clamped_speed >= 0.001:
            scale_factor = clamped_speed/speed

            new_vel_x = scale_factor*vel_x
            new_vel_y = scale_factor*vel_y

        self.drivetrain.drive(,
                              ,
                              -self.pid_rot.calculate(self.drivetrain.getRotation().degrees()),
                              True
        )

    def end(self, interrupted):
        self.drivetrain.drive(0, 0, 0, False)

    def isFinished(self):
        return self.pid_x.atSetpoint() and self.pid_y.atSetpoint() and self.pid_rot.atSetpoint()
