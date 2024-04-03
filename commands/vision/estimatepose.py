from wpimath.geometry import Pose2d, Rotation2d
from subsystems.drivetrain import Drivetrain
from subsystems.vision import Vision
from utils.safecommand import SafeCommand

class EstimatePose(SafeCommand):
    def __init__(
        self,
        drivetrain: Drivetrain,
        vision: Vision,
    ):
        super().__init__()
        self.drivetrain = drivetrain
        self.vision = vision

    def execute(self):
        visionEstimatedPose = self.vision.getEstimatedPose()
        visionEstimatedRot = self.vision.getEstimatedRot()
        drivetrainEstimatedPose = self.drivetrain.getPose()
        drivetrainEstimatedRot = self.drivetrain.getAngle()

        if visionEstimatedPose is not None:
            if not self.isClose(drivetrainEstimatedPose.x, visionEstimatedPose.x, 0.2):
                self.drivetrain.resetToPose(Pose2d(visionEstimatedPose.x, drivetrainEstimatedPose.y, Rotation2d.fromDegrees(drivetrainEstimatedRot)))
            if not self.isClose(drivetrainEstimatedPose.y, visionEstimatedPose.y, 0.2):
                self.drivetrain.resetToPose(Pose2d(drivetrainEstimatedPose.x, visionEstimatedPose.y, Rotation2d.fromDegrees(drivetrainEstimatedRot)))

        if visionEstimatedRot is not None:
            if not self.isClose(drivetrainEstimatedRot, visionEstimatedRot.y_degrees, 5):
                self.drivetrain.resetToPose(Pose2d(drivetrainEstimatedPose.x, drivetrainEstimatedPose.y, Rotation2d(visionEstimatedRot.y_degrees)))

    def isClose(self, a, b, zone):
        return (a+zone > b and a-zone < b)
