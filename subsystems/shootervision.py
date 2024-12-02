from typing import Optional
import wpilib
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from subsystems.vision import Vision

def getSpeakerTagIDFromAlliance() -> Optional[int]:
    alliance = wpilib.DriverStation.getAlliance()
    if alliance == wpilib.DriverStation.Alliance.kRed:
        return 4
    elif alliance == wpilib.DriverStation.Alliance.kBlue:
        return 7
    else:
        wpilib.reportError("Alliance is invalid")
        return None

class ShooterVision(Vision):
    def __init__(self):
        super().__init__(cameraname='shootingCamera')

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
