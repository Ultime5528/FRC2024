import commands2
from commands2 import ParallelCommandGroup
from commands2.cmd import parallel, sequence
from wpimath.geometry import Pose2d, Rotation2d

from commands.intake.pickup import PickUp
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.drivetrain import Drivetrain
from subsystems.vision import Vision
from utils.property import autoproperty
from utils.safecommand import SafeMixin
from commands.shooter.shoot import Shoot
from commands.pivot.movepivot import MovePivot
from commands.drivetoposes import DriveToPoses
from commands.drivetrain.resetpose import ResetPose


class MegaModeAutonome(SafeMixin, commands2.SequentialCommandGroup):
    position_pivot = autoproperty(45)

    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            ResetPose(drivetrain, Pose2d(15.2029, 5.553, Rotation2d.fromDegrees(180))),
            ResetPivotDown(pivot),
            parallel(
                MovePivotContinuous(pivot, vision),
                sequence(
                    Shoot(shooter, pivot, intake),
                    parallel(
                        PickUp(intake),
                        DriveToPoses(
                            drivetrain,
                            [Pose2d(13.645, 5.553, Rotation2d.fromDegrees(180))],
                        ),
                    ),
                    DriveToPoses(
                        drivetrain,
                        [Pose2d(14.1, 6.772, Rotation2d.fromDegrees(153.36))],
                    ),
                    Shoot(shooter, pivot, intake),
                    parallel(
                        PickUp(intake),
                        DriveToPoses(
                            drivetrain,
                            [Pose2d(13.645, 7.001, Rotation2d.fromDegrees((153.36)))],
                        ),
                    ),
                    Shoot(shooter, pivot, intake),
                    parallel(
                        PickUp(intake),
                        DriveToPoses(
                            drivetrain,
                            [
                                Pose2d(14.1, 4.332, Rotation2d.fromDegrees(-153.51)),
                                Pose2d(13.645, 4.105, Rotation2d.fromDegrees(-153.51)),
                            ],
                        ),
                    ),
                    Shoot(shooter, pivot, intake),
                ),
            ),
        )
