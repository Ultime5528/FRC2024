from typing import Union, Callable, Optional

import wpilib
from commands2.button import CommandXboxController
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpilib.interfaces import GenericHID
from wpimath.filter import SlewRateLimiter

from commands.pivot.movepivot import MovePivot
from subsystems.drivetrain import Drivetrain
from subsystems.pivot import Pivot
from utils.property import autoproperty
from utils.safecommand import SafeCommand
from commands.drivetrain.drive import apply_center_distance_deadzone, properties
from commands.vision.alignwithtag2d import getTargetWithID, getTagIDFromAlliance


class AlignEverything(SafeCommand):
    p = autoproperty(0.01)
    ff = autoproperty(0.01)

    @classmethod
    def toSpeaker(cls, drivetrain: Drivetrain, pivot: Pivot, xbox_remote: CommandXboxController):
        cmd = cls(drivetrain, pivot, getTagIDFromAlliance, xbox_remote)
        cmd.setName(cmd.getName() + ".toSpeaker")
        return cmd

    def __init__(
        self,
        drivetrain: Drivetrain,
        pivot: Pivot,
        tag_id: Union[int, Callable[[], int]],
        xbox_remote: CommandXboxController,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.pivot = pivot
        self.xbox_remote = xbox_remote
        self.hid = xbox_remote.getHID()
        self.get_tag_id = tag_id if callable(tag_id) else lambda: tag_id
        self.vel_rot = 0

        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)

    def execute(self):
        results = self.drivetrain.cam.getLatestResult().getTargets()
        self.target: PhotonTrackedTarget = getTargetWithID(results, self.get_tag_id())

        x_speed, y_speed, _ = apply_center_distance_deadzone(
            self.xbox_remote.getLeftY() * -1,
            self.xbox_remote.getLeftX() * -1,
            properties.moving_deadzone,
        )
        x_speed = self.m_xspeedLimiter.calculate(x_speed)
        y_speed = self.m_yspeedLimiter.calculate(y_speed)

        if target is not None:
            self.vel_rot = self.p * (0 - target.getYaw()) + self.ff * (
                0 - target.getYaw()
            )
            self.drivetrain.drive(x_speed, y_speed, self.vel_rot, is_field_relative=True)
        else:
            self.drivetrain.drive(x_speed, y_speed, 0, is_field_relative=True)
            if self.hid:
                self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0.5)

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        if self.target is not None:
            MovePivot.auto(self.pivot, self.pivot.getInterpolatedPosition(self.target.getPitch())).start()
        if self.hid:
            self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0)
