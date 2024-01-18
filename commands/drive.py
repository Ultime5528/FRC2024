import math

import commands2.button
from wpimath.filter import SlewRateLimiter
from wpimath.geometry import Rotation2d

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand
from utils.property import autoproperty


def apply_center_distance_deadzone(x_dist, y_dist, deadzone):
    if math.hypot(x_dist, y_dist) <= deadzone:
        return 0.0, 0.0
    else:
        return x_dist, y_dist


class Drive(SafeCommand):
    is_field_relative = autoproperty(True)
    has_rate_limiter = autoproperty(False)
    moving_deadzone = autoproperty(0.1)
    rotation_deadzone = autoproperty(0.8)
    rotate_speed = autoproperty(0.5)

    def __init__(
            self,
            drivetrain: Drivetrain,
            xbox_remote: commands2.button.CommandXboxController,
    ):
        super().__init__()
        self.rot: float = 0.0
        self.addRequirements(drivetrain)
        self.xbox_remote = xbox_remote
        self.drivetrain = drivetrain

        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)
        self.m_rotLimiter_x = SlewRateLimiter(3)
        self.m_rotLimiter_y = SlewRateLimiter(3)
        self.last_angle = 0

    def apply_deadzone(self, value):
        if abs(value) < self.moving_deadzone:
            return 0.0
        else:
            return value

    def execute(self):
        x_speed = self.apply_deadzone(
            self.m_xspeedLimiter.calculate(self.xbox_remote.getLeftY())
            * -1
        )

        y_speed = self.apply_deadzone(
            self.m_yspeedLimiter.calculate(self.xbox_remote.getLeftX())
            * -1
        )

        rot_x, rot_y = apply_center_distance_deadzone(self.xbox_remote.getRightX(), -1 * self.xbox_remote.getRightY(),
                                                      self.rotation_deadzone)

        if not (rot_x == 0 and rot_y == 0):
            self.rot = math.degrees(math.atan2(rot_x, rot_y)) * -1

        rot_speed = (self.drivetrain.getRotation() - Rotation2d.fromDegrees(self.rot)).degrees() * self.rotate_speed

        self.drivetrain.drive(x_speed, y_speed, rot_speed, self.is_field_relative, self.has_rate_limiter)

    def end(self, interrupted: bool) -> None:
        self.drivetrain.drive(0.0, 0.0, 0.0, is_field_relative=False, rate_limiter=False)
