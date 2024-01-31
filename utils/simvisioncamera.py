from typing import List, Callable

from photonlibpy.packet import Packet
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.photonPipelineResult import PhotonPipelineResult, PhotonTrackedTarget
from photonlibpy.multiTargetPNPResult import PNPResult, MultiTargetPNPResult
from ntcore import NetworkTableInstance, NetworkTableEntry, RawPublisher
from wpimath.units import milliseconds


class SimPhotonCamera(PhotonCamera):
    def __init__(self, instance: NetworkTableInstance, camera_name: str):
        super().__init__(instance, camera_name)
        self.latency_millis_entry = instance.getEntry("latencyMillis")
        self.has_target_entry = instance.getEntry("hasTargetEntry")
        self.target_pitch_entry = instance.getEntry("targetPitchEntry")
        self.target_yaw_entry = instance.getEntry("targetYawEntry")
        self.target_area_entry = instance.getEntry("targetAreaEntry")
        self.target_skew_entry = instance.getEntry("targetSkewEntry")
        self.target_pose_entry = instance.getEntry("targetPoseEntry")
        self.raw_bytes_publisher = instance.get_raw_topic("rawBytes").publish("rawBytes")
        self.version_entry = instance.getTable("photonvision").getEntry("version")

    def submit_processed_frame(self, latency, target_list: List[PhotonTrackedTarget],
                               sort_mode: Callable[[PhotonTrackedTarget, PhotonTrackedTarget], bool] = None):
        self.submit_processed_frame(latency, PhotonTargetSortMode.LeftMost(), target_list)

    def submit_processed_frame(self, latency: milliseconds, sort_mode: Callable[[PhotonTrackedTarget, PhotonTrackedTarget], bool],
                               target_list: List[PhotonTrackedTarget]):
        self.latency_millis_entry.setDouble(latency)
        target_list.sort(key=lambda target: sort_mode(target))
        new_result = PhotonPipelineResult(latency, target_list)
        packet = Packet

        self.raw_bytes_publisher.set(packet.getData())

        has_targets = len(new_result.targets) != 0
        self.has_target_entry.setBoolean(has_targets)
        if not has_targets:
            self.target_pitch_entry.setDouble(0.0)
            self.target_yaw_entry.setDouble(0.0)
            self.target_area_entry.setDouble(0.0)
            self.target_pose_entry.setDoubleArray([0.0, 0.0, 0.0, 0, 0, 0, 0])
            self.target_skew_entry.setDouble(0.0)
        else:
            best_target = new_result.get_best_target()
            self.target_pitch_entry.setDouble(best_target.get_pitch())
            self.target_yaw_entry.setDouble(best_target.get_yaw())
            self.target_area_entry.setDouble(best_target.get_area())
            self.target_skew_entry.setDouble(best_target.get_skew())

            transform = best_target.get_best_camera_to_target()
            self.target_pose_entry.setDoubleArray([
                transform.x.to(float), transform.y.to(float), transform.z.to(float),
                transform.rotation.get_quaternion().w, transform.rotation.get_quaternion().x,
                transform.rotation.get_quaternion().y, transform.rotation.get_quaternion().z
            ])
