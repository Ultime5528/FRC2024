import commands2.button
from wpilib.interfaces import GenericHID

from utils.safesubsystem import SafeSubsystem


class Controller(SafeSubsystem):
    def __init__(self, xbox_controller: commands2.button.CommandXboxController):
        super().__init__()
        self.xbox_remote = xbox_controller
        self.hid = self.xbox_remote.getHID()

    def vibrate(self, value: float):
        self.hid.setRumble(GenericHID.RumbleType.kBothRumble, value)
