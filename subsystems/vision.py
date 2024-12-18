from typing import Optional, List

from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpiutil import Sendable


class Vision(Sendable):
    def __init__(self, cameraname: str):
        super().__init__()
        self.cameraName = cameraname
        self._cam = PhotonCamera(self.cameraName)
        self._targets: List[PhotonTrackedTarget] = []

    def periodic(self):
        if self._cam.isConnected():
            self._targets = self._cam.getLatestResult().getTargets()
        else:
            self._targets = []
