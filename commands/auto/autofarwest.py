import commands2
from commands2 import ParallelCommandGroup, SequentialCommandGroup
from commands2.cmd import race, deadline
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.pickup import PickUp
from commands.pivot.movepivot import MovePivot
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import PrepareAndShoot
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.auto import eitherRedBlue
from utils.safecommand import SafeMixin
from commands.auto.autospeakerampsideshoottwiceline import (
    AutoSpeakerAmpSideShootTwiceLine,
)


class AutoFarWest(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(

            eitherRedBlue(
                ResetPose(
                    drivetrain,
                    Pose2d(15.86, 4.385, Rotation2d.fromDegrees(-120)),
                ),
                ResetPose(
                    drivetrain,
                    Pose2d(0.681, 4.385, Rotation2d.fromDegrees(-60)),
                ),
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(15.59376437, 3.9074655, -120),
                    pose(15.3133199, 3.414677, -120),
                    pose(15.03287561, 2.9218885, -120),
                    pose(14.75243123, 2.4291, -120)
                ],
        [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),


            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(13.13194842, 2.01, -165.4995145),
                    pose(11.51146562, 1.5909, -165.4995145),
                    pose(9.890982808, 1.1718, -165.4995145),
                    pose(8.2705, 0.7527, -165.4995145)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(9.890982808, 1.1718, -120),
                    pose(11.51146562, 1.5909, -120),
                    pose(13.13194842, 2.01, -120),
                    pose(14.75243123, 2.4291, -120)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(13.73780192, 2.166689845, 156.5813689),
                    pose(12.72317262, 1.90427969, 156.5813689),
                    pose(11.70854331, 1.641869535, 156.5813689),
                    pose(10.693914, 1.37945938, 156.5813689)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(10.0880605, 1.641869535, 156.5813689),
                    pose( 9.482207, 1.90427969, 156.5813689),
                    pose(8.8763535, 2.166689845, 156.5813689),
                    pose(8.2705, 2.4291, 156.5813689)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(8.8763535, 2.166689845, -120),
                    pose(9.482207, 1.90427969, -120),
                    pose(10.0880605, 1.641869535, -120),
                    pose(10.693914, 1.37945938, -120)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(11.70854331, 1.641869535, -120),
                    pose(12.72317262, 1.90427969, -120),
                    pose(13.73780192, 2.166689845, -120),
                    pose(14.75243123, 2.4291, -120)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(13.73780192, 2.166689845, 131.6366715),
                    pose(12.72317262, 1.90427969, 131.6366715),
                    pose(11.70854331, 1.641869535, 131.6366715),
                    pose(10.693914, 1.37945938, 131.6366715)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(10.0880605, 2.060969535, 131.6366715),
                    pose(9.482207, 2.74247969, 131.6366715),
                    pose(8.8763535, 3.423989845, 131.6366715),
                    pose(8.2705, 4.1055, 131.6366715)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(8.8763535, 3.423989845, -120),
                    pose(9.482207, 2.74247969, -120),
                    pose(10.0880605, 2.060969535, -120),
                    pose(10.693914, 1.37945938, -120)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            ),

            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose(11.70854331, 1.641869535, -120),
                    pose(12.72317262, 1.90427969, -120),
                    pose(13.73780192, 2.166689845, -120),
                    pose(14.75243123, 2.4291, -120)
                ],
                [pose(1.7885, 7.4583, 0), pose(8.27, 7.4583, 0)],
            )

        )
