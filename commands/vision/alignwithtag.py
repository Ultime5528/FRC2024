import math
from typing import Optional

import wpilib
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def getTagFromID(targets: [PhotonTrackedTarget], id: int):
    for target in targets:
        if target.getFiducialId() == id:
            return target


class AlignWithTag2D(SafeCommand):
    align_speed = autoproperty(0.2)
    align_threshold = autoproperty(0.1)

    def __init__(self, drivetrain: Drivetrain):
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.has_tag = False
        self.tag_id: Optional[int] = None
        self.vr: float = None

    def initialize(self):
        results = self.drivetrain.cam.getLatestResult().getTargets()
        results = results.sort(key=lambda x: abs(x.getYaw()))
        if len(results) is not 0:
            nearest_tag: PhotonTrackedTarget = results[0]
            self.tag_id = nearest_tag.getFiducialId()
            self.has_tag = True
        else:
            self.has_tag = False

    def execute(self):
        # Quits if tag out view
        results = self.drivetrain.cam.getLatestResult().getTargets()
        target: PhotonTrackedTarget = getTagFromID(results, self.tag_id)
        self.vr = min(abs(target.getYaw()), self.align_speed)
        self.vr = math.copysign(self.vr, target.getYaw() * -1)

        self.drivetrain.drive(0, 0, self.vr)

    def isFinished(self) -> bool:
        # Quits if tag out view
        return abs(self.vr) <= self.align_threshold or not self.has_tag

    def end(self, interrupted: bool):
        self.drivetrain.stop()
