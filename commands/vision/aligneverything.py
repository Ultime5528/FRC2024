from typing import Union, Callable, Optional

import wpilib
from commands2 import ParallelCommandGroup
from commands2.button import CommandXboxController
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpilib.interfaces import GenericHID
from wpimath.filter import SlewRateLimiter

from commands.pivot.continuousmovepivot import ContinuousMovePivot
from commands.pivot.movepivot import MovePivot
from subsystems.drivetrain import Drivetrain
from subsystems.pivot import Pivot
from utils.property import autoproperty
from utils.safecommand import SafeCommand, SafeMixin
from commands.drivetrain.drive import apply_center_distance_deadzone, properties
from commands.vision.alignwithtag2d import getTargetWithID, getTagIDFromAlliance
from commands.shooter.prepareshoot import NoReqPivot


class AlignEverything(ParallelCommandGroup, SafeMixin):
    def __init__(self, drivetrain: Drivetrain, pivot: Pivot, xbox_remote: CommandXboxController):
        super().__init__(
            _AlignEverything.toSpeaker(drivetrain, pivot, xbox_remote),
            ContinuousMovePivot(pivot)
        )
        self.addRequirements(drivetrain, pivot)


class _AlignEverything(SafeCommand):
    p = autoproperty(0.01)
    ff = autoproperty(0.01)

    @classmethod
    def toSpeaker(cls, drivetrain: Drivetrain, pivot: NoReqPivot, xbox_remote: CommandXboxController):
        cmd = cls(drivetrain, pivot, getTagIDFromAlliance, xbox_remote)
        cmd.setName(cmd.getName() + ".toSpeaker")
        return cmd

    def __init__(
            self,
            drivetrain: Drivetrain,
            pivot: NoReqPivot,
            tag_id: Union[int, Callable[[], int]],
            xbox_remote: CommandXboxController,
    ):
        super().__init__()
        self.addRequirements(drivetrain, pivot)
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

        if self.target is not None:
            self.vel_rot = self.p * (0 - self.target.getYaw()) + self.ff * (
                    0 - self.target.getYaw()
            )
            self.pivot.setInterpolatorPosition(self.target.getPitch())
            self.drivetrain.drive(x_speed, y_speed, self.vel_rot, is_field_relative=True)
        else:
            self.drivetrain.drive(x_speed, y_speed, 0, is_field_relative=True)
            if self.hid:
                self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0.5)

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        if self.hid:
            self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0)
