from enum import Enum
from typing import List

import commands2
import wpilib
from ntcore import NetworkTableType
from ntcore.util import ntproperty
from wpiutil import SendableBuilder

from utils.fault import Fault, ErrorType


class SubSystemStatus(Enum):
    OK = 0
    WARNING = 1
    ERROR = 2

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
        self._subsystem_status_prop = ntproperty(
            "/Diagnostics/" + self.__class__.__name__ + "/Status",
            0,
            type=NetworkTableType.kInteger,
            persistent=True,
        )

    def registerFault(self, fault: Fault):
        if self._subsystem_status != SubSystemStatus.ERROR:
            if fault.severity == ErrorType.ERROR:
                self._subsystem_status = SubSystemStatus.ERROR
            elif fault.severity == ErrorType.WARNING:
                self._subsystem_status = SubSystemStatus.WARNING

        print(self._subsystem_status.value)
        self._subsystem_status_prop.fset(None, self._subsystem_status.value)
        self._faults.append(str(fault))
        self._faults_prop.fset(None, self._faults)

    def clearFaults(self):
        self._subsystem_status = SubSystemStatus.OK
        self._subsystem_status_prop.fset(None, int(self._subsystem_status))
        self._faults = []
        self._faults_prop.fset(None, self._faults)

    def getSubsystemStatus(self) -> SubSystemStatus:
        return self._subsystem_status

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
