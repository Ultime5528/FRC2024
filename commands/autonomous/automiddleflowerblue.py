import commands2
from wpimath.geometry import Pose2d
from commands2 import SequentialCommandGroup
from commands2 import ParallelCommandGroup

from commands.drivedistance import DriveDistance

from commands.charge import Charge
from commands.load import Load
from commands.launch import Launch
from commands.lock import Lock

from subsystems.drivetrain import Drivetrain


from subsystems.catapult import Catapult
from utils.property import autoproperty

from utils.safecommand import SafeMixin


class AutoMiddleFlowerBlue(SequentialCommandGroup, SafeMixin):
    forward_auto_blue = autoproperty(1.75)
    left_auto_blue = autoproperty(0.5)
    auto_blue_speed = autoproperty(0.75)

    def __init__(self, drivetrain: Drivetrain, catapult: Catapult):
        super().__init__(
            Lock(catapult),
            ParallelCommandGroup(
                DriveDistance(drivetrain, Pose2d(self.forward_auto_blue, self.left_auto_blue, 0), self.auto_blue_speed),
                Charge(catapult, 3)
            ),
            Load(catapult),
            commands2.WaitCommand(1.0),
            Launch(catapult)
        )
        self.addRequirements(drivetrain, catapult)
