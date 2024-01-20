import math

import commands2.button
from wpimath.filter import SlewRateLimiter

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand
from utils.property import autoproperty


class Drive(SafeCommand):
    is_field_relative = autoproperty(True)
    has_rate_limiter = autoproperty(False)
    deadzone = autoproperty(0.1)

    def __init__(
        self,
        drivetrain: Drivetrain,
        xbox_remote: commands2.button.CommandXboxController,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.xbox_remote = xbox_remote
        self.drivetrain = drivetrain

        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)
        self.m_rotLimiter_x = SlewRateLimiter(3)
        self.m_rotLimiter_y = SlewRateLimiter(3)

    def apply_deadzone(self, value):
        if abs(value) < self.deadzone:
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
        rot_x = self.apply_deadzone(
            self.m_rotLimiter_x.calculate(self.xbox_remote.getRightX())
        )
        rot_y = self.apply_deadzone(
            self.m_rotLimiter_y.calculate(self.xbox_remote.getRightY())
        )
        # TODO Vers lavant cest 0 degres. Lorsquon revien a neutre
        # cest le plus recent angle
        rot = math.atan2(rot_y, rot_x)
        print(f"{rot_x:.2f} {rot_y:.2f} {math.degrees(rot):.2f}")
        self.drivetrain.drive(x_speed, y_speed, rot_x, self.is_field_relative, self.has_rate_limiter)

    def end(self, interrupted: bool) -> None:
        self.drivetrain.drive(0.0, 0.0, 0.0, is_field_relative=False, rate_limiter=False)
