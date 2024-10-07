import wpilib
from enum import Enum


class EnumSeverity(Enum):
    WARNING = 1
    ERROR = 2


class Fault:
    def __init__(self, message: str, static: bool, severity: EnumSeverity):
        self.timestamp = wpilib.Timer.getFPGATimestamp()
        self.message = message
        self.static = static
        self.severity = severity

    def __str__(self):
        return self.severity.value+";"+str(self.timestamp)+";"+("1;" if self.static else "0;")+self.message
