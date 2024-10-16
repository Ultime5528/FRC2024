from wpiutil import SendableBuilder

from utils.safecommand import SafeCommand


class TestCommand(SafeCommand):
    def runsWhenDisabled(self) -> bool:
        return True
