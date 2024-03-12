import commands2
from commands2.cmd import parallel, deadline, race

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.pickup import PickUp
from commands.pivot.movepivot import MovePivot
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import PrepareAndShoot
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from utils.auto import eitherRedBlue
from utils.safecommand import SafeMixin

from commands.pivot.movepivotcontinuous import MovePivotContinuous
from subsystems.vision import Vision
from commands.vision.alignwithtag2d import AlignWithTag2D


class CenterShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self, drivetrain: Drivetrain, shooter: Shooter, pivot: Pivot, intake: Intake, vision: Vision
    ):
        super().__init__(
            eitherRedBlue(
                ResetPose(drivetrain, pose(15.2029, 5.553, 180)),
                ResetPose(drivetrain, pose(1.3381, 5.553, 0)),
            ),
            ResetPivotDown(pivot),
            race(
                PrepareAndShoot(shooter, pivot, intake),
                MovePivotContinuous(pivot, vision),
                AlignWithTag2D.toSpeaker(drivetrain, vision)
            ),
            deadline(
                PickUp(intake),
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [
                        pose(12.5, 5.553, 180),
                    ],
                    [pose(3.8, 5.553, 0),
                                pose(4.5, 5.553, 0)],
                ),
            ),
            DriveToPoses.fromRedBluePoints(
                drivetrain, [pose(15.2029, 5.553, 180)], [pose(1.3381, 5.553, 0)]
            ),
            race(
                PrepareAndShoot(shooter, pivot, intake),
                MovePivotContinuous(pivot, vision),
                AlignWithTag2D.toSpeaker(drivetrain, vision)
            ),
        )
