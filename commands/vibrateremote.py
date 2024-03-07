from wpilib import Timer
from wpilib.interfaces import GenericHID

from utils.safecommand import SafeCommand
import commands2.button


class VibrateRemote(SafeCommand):
    def __init__(self, xbox_remote: commands2.button.CommandXboxController, seconds: float):
        super().__init__()
        self.hid = xbox_remote.getHID()
        self.seconds = seconds
        self.timer = Timer()

    def initialize(self):
        self.timer.reset()
        self.timer.start()

    def execute(self):
        self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0.5)

    def isFinished(self):
        return self.timer.get() >= self.seconds

    def end(self, interrupted: bool):
        self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0)
