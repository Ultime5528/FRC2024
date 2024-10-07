from enum import Enum
from typing import List

import commands2
import wpilib
from ntcore import NetworkTableType
from ntcore.util import ntproperty
from wpiutil import SendableBuilder

from utils.fault import Fault


class SubSystemStatus(Enum):
    OK = 1,
    WARNING = 2,
    ERROR = 3

class SafeSubsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()
        self.setName(self.__class__.__name__)
        self._faults = []
        self._subsystem_status = SubSystemStatus.OK
        self._faults_prop = ntproperty(
            "/Diagnostics/" + self.__class__.__name__ + "/Faults",
            [],
            type=NetworkTableType.kStringArray,
            persistent=True,
        )

    def registerFault(self, fault: Fault):
        self._faults.append(str(fault))
        self._faults_prop.fset(None, self._faults)

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def currentCommandName():
            cmd = self.getCurrentCommand()
            if cmd:
                return cmd.getName()
            else:
                return "None"

        def defaultCommandName():
            cmd = self.getDefaultCommand()
            if cmd:
                return cmd.getName()
            else:
                return "None"

        def noop(_):
            pass

        builder.setSmartDashboardType("List")
        builder.addStringProperty("Current command", currentCommandName, noop)
        builder.addStringProperty("Default command", defaultCommandName, noop)
