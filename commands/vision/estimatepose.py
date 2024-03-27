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
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.vision = vision

    def execute(self):
        visionEstimatedPose = self.vision.getEstimatedPose()
        drivetrainEstimatedPose = self.drivetrain.getPose()
        drivetrainRot = self.drivetrain.getAngle()

        if visionEstimatedPose is not None:
            if not self.isClose(drivetrainEstimatedPose.x, visionEstimatedPose.x, 0.2):
                self.drivetrain.resetToPose(Pose2d(visionEstimatedPose.x, drivetrainEstimatedPose.y, Rotation2d.fromDegrees(drivetrainRot)))
            if not self.isClose(drivetrainEstimatedPose.y, visionEstimatedPose.y, 0.2):
                self.drivetrain.resetToPose(Pose2d(drivetrainEstimatedPose.x, visionEstimatedPose.y, Rotation2d.fromDegrees(drivetrainRot)))

    def isClose(self, a, b, zone):
        return (a+zone > b and a-zone < b)
