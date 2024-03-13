from wpilib.interfaces import GenericHID
from wpiutil import SendableBuilder

from utils.safesubsystem import SafeSubsystem


class Controller(SafeSubsystem):
    def __init__(self, hid: GenericHID):
        super().__init__()
        self.hid = hid
        self._current_rumble = 0.0

    def vibrate(self, value: float):
        self._current_rumble = value
        self.hid.setRumble(GenericHID.RumbleType.kBothRumble, value)

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addDoubleProperty("current_rumble", lambda: self._current_rumble, noop)
