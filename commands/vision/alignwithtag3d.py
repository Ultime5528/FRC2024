import math

from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpimath.geometry import Transform3d

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand


def getTagFromID(targets: [PhotonTrackedTarget], _id: int):
    for target in targets:
        if target.getFiducialId() == _id:
            return target
    return None


class AlignWithTag3D(SafeCommand):
    align_speed = autoproperty(0.2)
    align_threshold = autoproperty(0.1)

    def __init__(self, drivetrain: Drivetrain, tag_id: int, distance_to_tag_meters: float):
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.has_tag = False
        self.tag_id = tag_id
        self.vr: float = None

    def execute(self):
        results = self.drivetrain.cam.getLatestResult().getTargets()
        target: PhotonTrackedTarget = getTagFromID(results, self.tag_id)
        if target is not None:
            self.has_tag = True
            camera_to_target: Transform3d = target.getBestCameraToTarget()
            v_left = min(abs(camera_to_target.y), self.align_speed)
            v_left = math.copysign(v_left, camera_to_target.y)
            v_rot = min(abs(target.getSkew()) - 180, self.align_speed)
            v_rot = math.copysign(v_rot, target.getSkew())
            if v_left <= self.align_threshold and v_rot <= self.align_threshold:
                self.v_forward = min(camera_to_target.x, self.align_speed)
                self.drivetrain.drive(self.v_forward, 0, 0)
            else:
                self.drivetrain.drive(v_left * -1, 0, v_rot * -1)
        else:
            self.has_tag = False

    def isFinished(self) -> bool:
        return self.v_forward <= self.align_threshold or not self.has_tag

    def end(self, interrupted: bool):
        self.drivetrain.stop()
