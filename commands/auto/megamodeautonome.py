import commands2
from commands2.cmd import parallel, sequence, race, deadline

from commands.auto.centershoottwiceline import CenterShootTwiceLine
from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.load import Load
from commands.intake.pickup import PickUp
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import PrepareAndShoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.auto import eitherRedBlue
from utils.safecommand import SafeMixin


class MegaModeAutonome(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision: Vision,
    ):
        super().__init__(
            CenterShootTwiceLine(drivetrain, shooter, pivot, intake, vision),
            parallel(
                MovePivotContinuous(pivot, vision),
                PrepareShoot(shooter, pivot),
                sequence(
                    deadline(
                        PickUp(intake),
                        DriveToPoses.fromRedBluePoints(
                            drivetrain,
                            [
                                pose(14.78, 6.8, 180),
                                pose(13.66, 6.8, 153.36),  # 13, 7
                            ],
                            [
                                pose(1.761, 6.8, 0),  # 13, 7
                                pose(2.881, 6.8, 26.64),  # 13, 7
                            ],
                        ),
                    ),
                    DriveToPoses.fromRedBluePoints(
                        drivetrain,
                        [pose(14.78, 6.43, 153.36)],
                        [pose(1.761, 6.43, 26.64)],
                    ),
                    deadline(
                        sequence(WaitShootSpeed(shooter), Load(intake)),
                        AlignWithTag2D.toSpeaker(drivetrain, vision),
                    ),
                ),
            ),
        )
