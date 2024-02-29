import commands2
from commands2 import ParallelCommandGroup
from commands2.cmd import race, parallel

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.pickup import PickUp
from commands.pivot.movepivot import MovePivot
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import Shoot
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from utils.auto import eitherRedBlue
from utils.property import autoproperty
from utils.safecommand import SafeMixin


class AutoSpeakerCenterShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    position_pivot = autoproperty(45)

    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake
    ):
        super().__init__(
            eitherRedBlue(
                ResetPose(drivetrain, pose(15.2029, 5.553, 180)),
                ResetPose(drivetrain, pose(1.3381, 5.553, 0)),
            ),
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            Shoot(shooter, pivot, intake),
            race(
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [
                        pose(12.5, 5.553, 180),
                    ],
                    [
                        pose(4.5, 5.553, 0)],
                ),
                PickUp(intake),
            ),
            parallel(
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [pose(15.2029, 5.553, 180)],
                    [pose(1.3381, 5.553, 0)]
                ),
                MovePivot.toSpeakerClose(pivot),
            ),
            Shoot(shooter, pivot, intake),
        )
