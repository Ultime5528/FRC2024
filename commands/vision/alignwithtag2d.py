import math
from typing import Optional

import wpilib
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpimath._controls._controls.controller import PIDController

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def getTagFromID(targets: [PhotonTrackedTarget], _id: int):
    for target in targets:
        if target.getFiducialId() == _id:
            return target
    return None


class AlignWithTag2D(SafeCommand):
    p_align = autoproperty(0.001)
    ff_align = autoproperty(0.001)

    @classmethod
    def toSpeakerRed(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, tag_id=4)
        cmd.setName(cmd.getName() + ".toSpeakerRed")
        return cmd

    @classmethod
    def toSpeakerBlue(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, tag_id=8)
        cmd.setName(cmd.getName() + ".toSpeakerBlue")
        return cmd

    def __init__(self, drivetrain: Drivetrain, tag_id: int):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.tag_id = tag_id
        self.vel_rot = 0

    def execute(self):
        results = self.drivetrain.cam.getLatestResult().getTargets()
        target: PhotonTrackedTarget = getTagFromID(results, self.tag_id)
        if target is not None:
            self.vel_rot = self.p_align * (0 - target.getYaw()) + self.ff_align * (0 - target.getYaw())
            self.drivetrain.drive(0, 0, -self.vel_rot, is_field_relative=True)
        else:
            self.drivetrain.drive(0, 0, 0, is_field_relative=True)

    def end(self, interrupted: bool):
        self.drivetrain.stop()
