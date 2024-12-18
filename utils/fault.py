import wpilib
from enum import Enum


class Severity(Enum):
    WARNING = 0
    ERROR = 1


class Fault:
    def __init__(self, message: str, severity: Severity, sticky: bool):
        self.timestamp = wpilib.Timer.getFPGATimestamp()
        self.message = message
        self.sticky = sticky
        self.severity = severity

    def __str__(self):
        return (
            str(self.severity.value)
            + ";"
            + str(self.timestamp)
            + ";"
            + ("1;" if self.sticky else "0;")
            + self.message
        )
