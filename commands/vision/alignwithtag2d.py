from typing import Union, Callable, Optional

from commands2.button import CommandXboxController
from wpilib import DriverStation
from wpilib.interfaces import GenericHID
from wpimath.filter import SlewRateLimiter

from commands.drivetrain.drive import apply_center_distance_deadzone, properties
from subsystems.drivetrain import Drivetrain
from subsystems.shootervision import getSpeakerTagIDFromAlliance, ShooterVision
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class AlignWithTag2D(SafeCommand):
    p = autoproperty(0.025)
    horizontal_offset = autoproperty(0.0)

    @classmethod
    def toSpeaker(
        cls,
        drivetrain: Drivetrain,
        vision: ShooterVision,
        xbox_remote: Optional[CommandXboxController] = None,
    ):
        cmd = cls(drivetrain, vision, getSpeakerTagIDFromAlliance, xbox_remote)
        cmd.setName(cmd.getName() + ".toSpeaker")
        return cmd

    def __init__(
        self,
        drivetrain: Drivetrain,
        vision: ShooterVision,
        tag_id: Union[int, Callable[[], int]],
        xbox_remote: Optional[CommandXboxController] = None,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.vision = vision
        self.xbox_remote = xbox_remote
        self.hid = xbox_remote.getHID() if xbox_remote else None
        self.get_tag_id = tag_id if callable(tag_id) else lambda: tag_id
        self.vel_rot = 0

        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)

    def execute(self):
        target = self.vision.getTargetWithID(self.get_tag_id())

        if self.xbox_remote:
            x_speed, y_speed, _ = apply_center_distance_deadzone(
                self.xbox_remote.getLeftY() * -1,
                self.xbox_remote.getLeftX() * -1,
                properties.moving_deadzone,
            )
            x_speed = self.m_xspeedLimiter.calculate(x_speed)
            y_speed = self.m_yspeedLimiter.calculate(y_speed)

            if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
                x_speed *= -1
                y_speed *= -1

        else:
            x_speed = 0.0
            y_speed = 0.0

        if target is not None:
            self.vel_rot = self.p * (self.horizontal_offset - target.getYaw())
            self.drivetrain.drive(
                x_speed, y_speed, self.vel_rot, is_field_relative=True
            )
        elif self.hid:
            self.drivetrain.drive(x_speed, y_speed, 0, is_field_relative=True)
            self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 1.0)

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        if self.hid:
            self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0)
