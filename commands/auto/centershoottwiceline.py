import commands2
from commands2.cmd import deadline, race, parallel, sequence

from commands.drivetoposes import DriveToPoses, pose
from commands.drivetrain.resetpose import ResetPose
from commands.intake.alignedpickup import AlignedPickUp
from commands.intake.pickup import PickUp
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.shooter.shoot import PrepareAndShoot
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.shootervision import ShooterVision
from utils.auto import eitherRedBlue
from utils.safecommand import SafeMixin

from subsystems.pickupvision import PickUpVision
from commands.vision.gotonote import GoToNote


class CenterShootTwiceLine(SafeMixin, commands2.SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        shooter: Shooter,
        pivot: Pivot,
        intake: Intake,
        vision_shooter: ShooterVision,
        vision_pickup: PickUpVision,
    ):
        super().__init__(
            eitherRedBlue(
                ResetPose(drivetrain, pose(15.2029, 5.553, 180)),
                ResetPose(drivetrain, pose(1.3381, 5.553, 0)),
            ),
            ResetPivotDown(pivot),
            race(
                PrepareAndShoot(shooter, pivot, intake),
                AlignWithTag2D.toSpeaker(drivetrain, vision_shooter),
            ),
            AlignedPickUp(drivetrain, intake, vision_pickup),
            race(
                MovePivotContinuous(pivot, vision_shooter),
                sequence(
                    DriveToPoses.fromRedBluePoints(
                        drivetrain, [pose(15, 5.553, 180)], [pose(1.5381, 5.553, 0)]
                    ),
                    race(
                        PrepareAndShoot(shooter, pivot, intake),
                        AlignWithTag2D.toSpeaker(drivetrain, vision_shooter),
                    ),
                ),
            ),
        )
