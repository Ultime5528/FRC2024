import math

from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from wpimath.geometry import Transform3d, Pose2d

from alignbase import AlignBase
from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty


def getTagFromID(targets: [PhotonTrackedTarget], _id: int):
    for target in targets:
        if target.getFiducialId() == _id:
            return target
    return None


class AlignWithTag3D(AlignBase):
    align_speed = autoproperty(0.2)
    align_threshold = autoproperty(0.1)

    def __init__(self, drivetrain: Drivetrain, tag_id: int, goal_tag_offset: Pose2d = Pose2d(0, 2, 0)):
        super().__init__(True, drivetrain)
        self.goal = None
        self.has_tag = False
        self.tag_id = tag_id
        self.pos_to_tag = goal_tag_offset

    def initialize(self):
        super().initialize()

    def computeGoal(self) -> Pose2d:
        results = self.drivetrain.cam.getLatestResult().getTargets()
        target: PhotonTrackedTarget = getTagFromID(results, self.tag_id)
        if target is not None:
            self.has_tag = True
            pos = self.drivetrain.getPose()
            camera_to_target: Transform3d = target.getBestCameraToTarget()
            tag_offset = Pose2d(camera_to_target.translation().toTranslation2d(),
                                camera_to_target.rotation().toRotation2d())
            goal = pos + tag_offset - self.pos_to_tag
            self.goal = goal
            return goal
        elif self.goal is not None:
            return self.goal
        else:
            return self.drivetrain.getPose()
