import math
from typing import Optional

import wpilib
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def getTagFromID(targets: [PhotonTrackedTarget], _id: int):
    for target in targets:
        if target.getFiducialId() == _id:
            return target
    return None


class AlignWithTag2D(SafeCommand):
    align_speed = autoproperty(0.2)
    align_threshold = autoproperty(0.1)

    def __init__(self, drivetrain: Drivetrain, tag_id: int):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.has_tag = False
        self.tag_id = tag_id
        self.vr: Optional[float] = None
        self.last_vr: Optional[float] = None

    def execute(self):
        results = self.drivetrain.cam.getLatestResult().getTargets()
        target: PhotonTrackedTarget = getTagFromID(results, self.tag_id)
        if target is not None:
            self.has_tag = True
            self.vr = min(abs(target.getYaw()), self.align_speed)
            self.vr = math.copysign(self.vr, target.getYaw() * -1)
            self.last_vr = self.vr
            self.drivetrain.drive(0, 0, self.vr, True)
        elif self.last_vr is not None:
            self.drivetrain.drive(0, 0, self.last_vr, True)
        else:
            self.has_tag = False

    def isFinished(self) -> bool:
        return abs(self.vr) <= self.align_threshold or not self.has_tag

    def end(self, interrupted: bool):
        self.drivetrain.stop()
