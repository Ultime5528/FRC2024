from typing import Optional, List

import wpilib
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpiutil import Sendable


def getSpeakerTagIDFromAlliance() -> Optional[int]:
    alliance = wpilib.DriverStation.getAlliance()
    if alliance == wpilib.DriverStation.Alliance.kRed:
        return 4
    elif alliance == wpilib.DriverStation.Alliance.kBlue:
        return 8
    else:
        wpilib.reportError("Alliance is invalid")
        return None


class Vision(Sendable):
    def __init__(self):
        super().__init__()
        self._cam = PhotonCamera("mainCamera")
        self._targets: List[PhotonTrackedTarget] = []
        self._speaker_target: Optional[PhotonTrackedTarget] = None

    def periodic(self):
        self._targets = self._cam.getLatestResult().getTargets()

    def getTargetWithID(self, _id: int) -> Optional[PhotonTrackedTarget]:
        for target in self._targets:
            if target.getFiducialId() == _id:
                return target
        return None

    def initSendable(self, builder):
        def noop(x):
            pass

        def getSpeakerPitch():
            target = self.getTargetWithID(getSpeakerTagIDFromAlliance())
            if target is not None:
                return target.getPitch()
            return 0.0

        def getSpeakerYaw():
            target = self.getTargetWithID(getSpeakerTagIDFromAlliance())
            if target is not None:
                return target.getYaw()
            return 0.0

        builder.addFloatProperty("speaker_y", getSpeakerPitch, noop)
        builder.addFloatProperty("speaker_x", getSpeakerYaw, noop)
