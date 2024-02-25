from typing import Optional, List, Union

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
        self._speaker_target = self.getTargetWithID(getSpeakerTagIDFromAlliance())

    def getTargetWithID(self, _id: int) -> Optional[PhotonTrackedTarget]:
        for target in self._targets:
            if target.getFiducialId() == _id:
                return target
        return None

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        def getSpeakerTagValues():
            if self._speaker_target is not None:
                return self._speaker_target.getPitch(), self._speaker_target.getYaw()

        builder.addFloatProperty("speaker_tag_Y_pos", lambda: getSpeakerTagValues()[0], noop)
