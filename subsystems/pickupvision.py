from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from subsystems.vision import Vision

class PickUpVision(Vision):
    def __init__(self):
        super().__init__(cameraname='noteCamera')

    def getTargetDistance(self, target: PhotonTrackedTarget):
        return target.getPitch()

    def getBestNote(self):
        bestNote = None
        for target in self._targets:
            if bestNote is None or self.getTargetDistance(target) < self.getTargetDistance(bestNote):
                bestNote = target
        return bestNote
