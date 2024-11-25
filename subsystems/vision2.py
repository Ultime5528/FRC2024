import os
from typing import Optional, List

import wpilib
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpilib import Timer, RobotBase
from wpiutil import Sendable


class Vision2(Sendable):
    def __init__(self):
        super().__init__()
        self._cam = PhotonCamera("noteCamera")
        self._targets: List[PhotonTrackedTarget] = []

        # If sim, we consider we already logged the date.
        self._has_logged_date = RobotBase.isSimulation()
        self._log_timer = Timer()
        self._log_timer.start()

    def periodic(self):
        if self._cam.isConnected():
            self._targets = self._cam.getLatestResult().getTargets()
        else:
            print("camera not connected")
            self._targets = []
            self._cam._versionCheck()

    def getTargetDistance(self, target: PhotonTrackedTarget):
        return target.getPitch()

    def getBestNote(self):
        bestNote = None
        for target in self._targets:
            if bestNote is None or self.getTargetDistance(
                target
            ) < self.getTargetDistance(bestNote):
                bestNote = target
        return bestNote
