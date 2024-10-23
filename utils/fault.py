import wpilib
from enum import Enum


class ErrorType(Enum):
    WARNING = 0
    ERROR = 1


class Fault:
    def __init__(self, message: str, static: bool, severity: ErrorType):
        self.timestamp = wpilib.Timer.getFPGATimestamp()
        self.message = message
        self.static = static
        self.severity = severity

    def __str__(self):
        return (
            str(self.severity.value)
            + ";"
            + str(self.timestamp)
            + ";"
            + ("1;" if self.static else "0;")
            + self.message
        )
