import commands2
from wpimath.geometry import Pose2d, Rotation2d

from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeMixin
from commands.shooter.shoot import ShootQuick
from commands.pivot.movepivot import MovePivot
from commands.drivetopos import DriveToPos


class AutoSpeakerRightShootLine(SafeMixin, commands2.SequentialCommandGroup):
    x_goal = autoproperty(2.5)
    y_goal = autoproperty(-0.25)

    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake
    ):
        super().__init__(
            MovePivot.toSpeakerClose(pivot),
            ShootQuick(shooter, pivot, intake),
            DriveToPos(
                drivetrain,
                Pose2d(self.x_goal, self.y_goal, Rotation2d.fromDegrees(180)),
            ),
        )
