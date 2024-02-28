import math

import commands2.button
from wpilib import DriverStation
from wpimath.filter import SlewRateLimiter
from wpimath.geometry import Rotation2d

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def apply_center_distance_deadzone(x_dist, y_dist, deadzone):
    hypot = math.hypot(x_dist, y_dist)
    if hypot <= deadzone:
        return 0.0, 0.0, 0.0
    else:
        return x_dist, y_dist, hypot


def apply_linear_deadzone(_input, deadzone):
    if abs(_input) <= deadzone:
        return 0.0
    else:
        return _input


class DriveField(SafeCommand):
    rotation_deadzone = autoproperty(0.3)
    rotate_speed = autoproperty(0.03)

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

    def initialize(self):
        self.rot = self.drivetrain.getPose().rotation()

    def execute(self):
        x_speed, y_speed, _ = apply_center_distance_deadzone(
            self.xbox_remote.getLeftY() * -1,
            self.xbox_remote.getLeftX() * -1,
            properties.moving_deadzone,
        )
        x_speed = self.m_xspeedLimiter.calculate(x_speed)
        y_speed = self.m_yspeedLimiter.calculate(y_speed)

        rot_x, rot_y, rot_hyp = apply_center_distance_deadzone(
            self.xbox_remote.getRightX(),
            -1 * self.xbox_remote.getRightY(),
            self.rotation_deadzone,
        )

        if not (rot_x == 0 and rot_y == 0):
            self.rot = Rotation2d(math.atan2(rot_x, rot_y)*-1)
            if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
                self.rot = Rotation2d.fromDegrees(180+self.rot.degrees())

        rot_speed = (
            (self.rot - self.drivetrain.getPose().rotation()).degrees()
            * self.rotate_speed
            * rot_hyp
        )

        self.drivetrain.drive(-1 * x_speed if DriverStation.getAlliance() == DriverStation.Alliance.kRed else x_speed, -1 * y_speed if DriverStation.getAlliance() == DriverStation.Alliance.kRed else y_speed, rot_speed, True)

    def end(self, interrupted: bool) -> None:
        self.drivetrain.stop()


class _Properties:
    moving_deadzone = autoproperty(0.1, subtable=DriveField.__name__)


properties = _Properties()
