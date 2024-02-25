from commands2 import ParallelCommandGroup
from commands2.button import CommandXboxController

from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.drivetrain import Drivetrain
from subsystems.pivot import Pivot
from subsystems.vision import Vision
from utils.safecommand import SafeMixin


class AlignEverything(SafeMixin, ParallelCommandGroup):
    def __init__(self, drivetrain: Drivetrain, pivot: Pivot, vision: Vision, xbox_remote: CommandXboxController):
        super().__init__(
            AlignWithTag2D.toSpeaker(drivetrain, vision, xbox_remote),
            MovePivotContinuous(pivot, vision)
        )
