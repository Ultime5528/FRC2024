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
        self._cam = PhotonCamera("mainCamera")
        self._targets: List[PhotonTrackedTarget] = []

        # If sim, we consider we already logged the date.
        self._has_logged_date = RobotBase.isSimulation()
        self._log_timer = Timer()
        self._log_timer.start()

    def periodic(self):
        if self._cam.isConnected():
            self._targets = self._cam.getLatestResult().getTargets()
           # if not self._has_logged_date and self._log_timer.hasElapsed(10.0):
            #    self._log_timer.restart()
             #   print("Retrieving Photonvision date")
              #  try:
              #      ret = os.system("ssh -o ConnectTimeout=1 pi@10.55.28.212 date")
             #       if ret == 0:
               #         self._has_logged_date = True
            #        else:
                      #  print("Returned exit code", ret)
             #   except Exception as e:
              #      print(e)
        else:
            print('camera not connected')
            self._targets = []
          #  self._cam._versionCheck()

    def getTargetDistance(self, target: PhotonTrackedTarget):
        return (target.getPitch()*target.getPitch()+target.getYaw()*target.getYaw())

    def getBestNote(self):
        bestNote = None
        for target in self._targets:
            if bestNote is None or self.getTargetDistance(target) < self.getTargetDistance(bestNote):
                bestNote = target
        return bestNote
