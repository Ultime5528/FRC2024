from typing import Union, Callable

import wpilib
from commands2.button import CommandXboxController
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand
from wpilib.interfaces import GenericHID


def getTagFromID(targets: [PhotonTrackedTarget], _id: int):
    for target in targets:
        if target.getFiducialId() == _id:
            return target
    return None


def getTagIDFromAlliance() -> int:
    alliance = wpilib.DriverStation.getAlliance()
    if alliance is wpilib.DriverStation.Alliance.kRed:
        return 4
    elif alliance is wpilib.DriverStation.Alliance.kBlue:
        return 8


class AlignWithTag2D(SafeCommand):
    p = autoproperty(0.01)
    ff = autoproperty(0.01)

    @classmethod
    def toSpeaker(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, tag_id=getTagIDFromAlliance)
        cmd.setName(cmd.getName() + ".toSpeaker")
        return cmd

    def __init__(self, drivetrain: Drivetrain, tag_id: Union[int, Callable[[], int]], xbox_remote: CommandXboxController):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.xbox_remote = xbox_remote
        self.tag_id = lambda: tag_id if tag_id is int else tag_id
        self.vel_rot = 0

    def execute(self):
        results = self.drivetrain.cam.getLatestResult().getTargets()
        target: PhotonTrackedTarget = getTagFromID(results, self.tag_id())
        if target is not None:
            self.vel_rot = self.p * (0 - target.getYaw()) + self.ff * (0 - target.getYaw())
            self.drivetrain.drive(0, 0, self.vel_rot, is_field_relative=True)
        else:
            self.xbox_remote.getHID().setRumble(GenericHID.RumbleType.kBothRumble, 0.5)
            self.drivetrain.drive(0, 0, 0, is_field_relative=True)

    def end(self, interrupted: bool):
        self.xbox_remote.getHID().setRumble(GenericHID.RumbleType.kBothRumble, 0)
        self.drivetrain.stop()
