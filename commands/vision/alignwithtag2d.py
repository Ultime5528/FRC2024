from typing import Union, Callable, Optional

import wpilib
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpilib.interfaces import GenericHID

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def getTargetWithID(
    targets: [PhotonTrackedTarget], _id: int
) -> Optional[PhotonTrackedTarget]:
    for target in targets:
        if target.getFiducialId() == _id:
            return target
    return None


def getTagIDFromAlliance() -> int:
    alliance = wpilib.DriverStation.getAlliance()
    if alliance == wpilib.DriverStation.Alliance.kRed:
        return 4
    elif (alliance ==
          wpilib.DriverStation.Alliance.kBlue):
        return 8
    else:
        wpilib.reportError("Alliance is invalid")
        return None


class AlignWithTag2D(SafeCommand):
    p = autoproperty(0.01)
    ff = autoproperty(0.01)

    @classmethod
    def toSpeaker(cls, drivetrain: Drivetrain, hid: Optional[GenericHID]):
        cmd = cls(drivetrain, getTagIDFromAlliance, hid)
        cmd.setName(cmd.getName() + ".toSpeaker")
        return cmd

    def __init__(
        self,
        drivetrain: Drivetrain,
        tag_id: Union[int, Callable[[], int]],
        hid: Optional[GenericHID],
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.hid = hid
        self.get_tag_id = tag_id if callable(tag_id) else lambda: tag_id
        self.vel_rot = 0

    def execute(self):
        results = self.drivetrain.cam.getLatestResult().getTargets()
        target: PhotonTrackedTarget = getTargetWithID(results, self.get_tag_id())

        if target is not None:
            self.vel_rot = self.p * (0 - target.getYaw()) + self.ff * (
                0 - target.getYaw()
            )
            self.drivetrain.drive(0, 0, self.vel_rot, is_field_relative=True)
        else:
            self.drivetrain.stop()
            if self.hid:
                self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0.5)

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        if self.hid:
            self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0)
