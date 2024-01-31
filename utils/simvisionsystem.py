import math
from typing import List, Optional
from dataclasses import dataclass

import wpilib
from photonlibpy.photonTrackedTarget import PhotonTrackedTarget
from pyfrc.physics.units import units
from wpilib import Field2d
from wpimath.geometry import Pose2d, Transform3d, Pose3d, Rotation3d, Translation3d, Transform2d

from utils.simvisioncamera import SimPhotonCamera


@dataclass
class SimVisionTarget:
    targetId: int
    targetPose: Pose2d
    targetArea: float

class SimVisionSystem:
    def __init__(self, cam_name: str, cam_diag_fov: float, camera_to_robot: Transform3d,
                 max_led_range: float, camera_res_width: int, camera_res_height: int,
                 min_target_area: float):
        self.cam = SimPhotonCamera(, cam_name)
        self.cam_horiz_fox = 0.0
        self.cam_vert_fov = 0.0
        self.max_led_range = max_led_range
        self.camera_res_width = camera_res_width
        self.cameraResHeight = camera_res_height
        self.minTargetArea = min_target_area
        self.cameraToRobot = camera_to_robot
        self.dbgField = Field2d()
        self.dbgRobot = self.dbgField.getRobotObject()
        self.dbgCamera = self.dbgField.GetObject(cam_name + " Camera")
        self.targetList: List[SimVisionTarget] = []

        # Calculate horizontal and vertical FOV
        self.cam_horiz_fox = (cam_diag_fov * camera_res_width) / math.hypot(camera_res_width, camera_res_height)
        self.cam_vert_fov = (cam_diag_fov * camera_res_height) / math.hypot(camera_res_width, camera_res_height)

        wpilib.SmartDashboard.PutData(cam_name + " Sim Field", self.dbgField)

    def addSimVisionTarget(self, target: SimVisionTarget):
        self.targetList.append(target)
        self.dbgField.GetObject("Target " + str(target.targetId)).SetPose(target.targetPose.ToPose2d())

    def clearVisionTargets(self):
        self.targetList.clear()

    def moveCamera(self, newCameraToRobot: Transform3d):
        self.cameraToRobot = newCameraToRobot

    def processFrame2D(self, robotPose: Pose2d):
        self.processFrame3D(Pose3d(robotPose.X(), robotPose.Y(), 0.0, Rotation3d(0, 0, robotPose.rotation().radians())))

    def processFrame3D(self, robotPose: Pose3d):
        camera_pose = robotPose.TransformBy(self.cameraToRobot.inverse())
        self.dbgRobot.SetPose(robotPose.ToPose2d())
        self.dbgCamera.SetPose(camera_pose.ToPose2d())

        visible_target_list = []

        for target in self.targetList:
            cam_to_target_transform = Transform3d(camera_pose, target.targetPose)
            cam_to_target_translation = cam_to_target_transform.translation()

            alt_translation = Translation3d(cam_to_target_translation.X(), -1.0 * cam_to_target_translation.Y(), cam_to_target_translation.Z())
            alt_rotation = cam_to_target_transform.rotation() * -1.0
            cam_to_target_alt_transform = Transform3d(alt_translation, alt_rotation)
            dist = cam_to_target_translation.norm()
            area_pixels = target.targetArea / self.getM2PerPx(dist)
            yaw = math.atan2(cam_to_target_translation.Y(), cam_to_target_translation.X())
            camera_height_off_ground = camera_pose.Z()
            target_height_above_ground = target.targetPose.Z()
            cam_pitch = camera_pose.Rotation().Y()
            transform_along_ground = Transform2d(camera_pose.ToPose2d(), target.targetPose.ToPose2d())
            distance_along_ground = transform_along_ground.translation().norm()
            pitch = math.atan2(target_height_above_ground - camera_height_off_ground, distance_along_ground) - cam_pitch

            if self.camSeeTarget(dist, yaw, pitch, area_pixels):
                visible_target_list.append(
                    PhotonTrackedTarget(math.degrees(yaw),
                                        math.degrees(pitch),
                                        area_pixels,
                                        0.0,
                                        target.targetId,
                                        cam_to_target_transform,
                                        cam_to_target_transform
                    )
                )
        self.cam.submitProcessedFrame(0, visible_target_list)

    def getM2PerPx(self, dist: units.meter_t) -> units.square_meter_t:
        widthMPerPx = 2 * dist * units.math.tan(self.cam_horiz_fox / 2) / self.camera_res_width
        heightMPerPx = 2 * dist * units.math.tan(self.cam_vert_fov / 2) / self.cameraResHeight
        return widthMPerPx * heightMPerPx

    def camSeeTarget(self, dist, yaw, pitch, area: float) -> bool:
        inRange = dist < self.max_led_range
        inHorizAngle = units.math.abs(yaw) < self.cam_horiz_fox / 2
        inVertAngle = units.math.abs(pitch) < self.cam_vert_fov / 2
        targetBigEnough = area > self.minTargetArea
        return inRange and inHorizAngle and inVertAngle and targetBigEnough
