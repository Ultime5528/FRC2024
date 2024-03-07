import commands2.button
import wpilib
from wpilib.interfaces import GenericHID

from commands.vibrateremote import VibrateRemote
from subsystems.intake import Intake
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class PickUp(SafeCommand):
    delay = autoproperty(0.0)

    def __init__(self, intake: Intake, xbox_remote: commands2.button.CommandXboxController = None):
        super().__init__()
        self.addRequirements(intake)
        self.xbox_remote = xbox_remote
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()

    def execute(self) -> None:
        self.intake.pickUp()
        if self.intake.hasNote():
            self.timer.start()

    def isFinished(self) -> bool:
        return self.intake.hasNote() and self.timer.get() >= self.delay

    def end(self, interrupted: bool) -> None:
        self.timer.stop()
        self.intake.stop()
        if self.xbox_remote is not None:
            VibrateRemote(self.xbox_remote, 3).schedule()
