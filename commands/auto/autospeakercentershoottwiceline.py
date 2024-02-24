import commands2
from commands2 import ParallelCommandGroup
from wpimath.geometry import Pose2d, Rotation2d

from commands.intake.pickup import PickUp
from commands.pivot.resetpivotdown import ResetPivotDown
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeMixin
from commands.shooter.shoot import ShootQuick
from commands.pivot.movepivot import MovePivot
from commands.drivetopos import DriveToPos


class AutoSpeakerCenterShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    x_goal = autoproperty(1)
    y_goal = autoproperty(0)
    position_pivot = autoproperty(45)

    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake
    ):
        super().__init__(
            ResetPivotDown(pivot),
            MovePivot.toSpeakerClose(pivot),
            ShootQuick(shooter, pivot, intake),
            ParallelCommandGroup(
                DriveToPos(
                    drivetrain,
                    Pose2d(self.x_goal, self.y_goal, Rotation2d.fromDegrees(0)),
                    True,
                ),
                PickUp(intake),
                MovePivot.auto(pivot, self.position_pivot),
            ),
            ShootQuick(shooter, pivot, intake),
        )
