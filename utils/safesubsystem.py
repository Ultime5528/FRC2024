from enum import Enum
from typing import List

import commands2
import wpilib
from ntcore import NetworkTableType
from ntcore.util import ntproperty
from wpiutil import SendableBuilder

from utils.fault import Fault, ErrorType
from utils.testcommand import TestCommand


class SubSystemStatus(Enum):
    OK = 0
    WARNING = 1
    ERROR = 2
    RUNNING_TEST = 3


class SafeSubsystem(commands2.Subsystem):
    subsystems: List["SafeSubsystem"] = []
    subsystems_prop = ntproperty(
        "/Diagnostics/SubsystemList", [], type=NetworkTableType.kStringArray
    )
    subsystems_tests: List["SafeSubsystem"] = []
    subsystems_tests_prop = ntproperty(
        "/Diagnostics/SubsystemListTests", [], type=NetworkTableType.kStringArray
    )

    def __init__(self):
        super().__init__()
        SafeSubsystem.subsystems.append(self)
        self.setName(self.__class__.__name__)
        self._subsystem_status = SubSystemStatus.OK
        self._subsystem_status_prop = None
        self._faults = []
        self._faults_prop = None
        self._test_command = None
        self._diagnostics_initialized = False

    @staticmethod
    def setupDiagnostics():
        for subsystem in SafeSubsystem.subsystems:
            subsystem.setupSubsystem()
        ntproperty("/Diagnostics/Ready", True)
        ntproperty("/Diagnostics/IsRunningTests", False)

    def setupSubsystem(self):
        if self not in SafeSubsystem.subsystems_tests:
            SafeSubsystem.subsystems_tests.append(self)
            SafeSubsystem.subsystems_tests_prop.fset(
                None,
                [subsystem.getName() for subsystem in SafeSubsystem.subsystems_tests],
            )

        self._faults_prop = ntproperty(
            "/Diagnostics/Subsystems/" + self.getName() + "/Faults",
            [],
            type=NetworkTableType.kStringArray,
            persistent=True,
        )
        self._faults = self._faults_prop.fget(None)

        self._subsystem_status_prop = ntproperty(
            "/Diagnostics/Subsystems/" + self.getName() + "/Status",
            0,
            persistent=True,
        )

        self._subsystem_status = SubSystemStatus(self._subsystem_status_prop.fget(None))
        if self._test_command:
            wpilib.SmartDashboard.putData(
                "Diagnostics/Tests/Test" + self.getName(), self._test_command
            )

        SafeSubsystem.subsystems_prop.fset(
            None, [subsystem.getName() for subsystem in SafeSubsystem.subsystems]
        )
        self._diagnostics_initialized = True

    def setTestCommand(self, test_command: TestCommand):
        if self not in SafeSubsystem.subsystems_tests:
            SafeSubsystem.subsystems_tests.append(self)

        self._test_command = test_command
        SafeSubsystem.subsystems_tests_prop.fset(
            None, [subsystem.getName() for subsystem in SafeSubsystem.subsystems_tests]
        )

        if self._diagnostics_initialized:
            wpilib.SmartDashboard.putData(
                "Diagnostics/Tests/Test" + self.getName(), self._test_command
            )

    def registerFault(
        self, message: str, severity: ErrorType = ErrorType.ERROR, static=False
    ):
        if not self._diagnostics_initialized:
            return
        fault = Fault(message, static, severity)
        if self._subsystem_status != SubSystemStatus.ERROR:
            if fault.severity == ErrorType.ERROR:
                self._subsystem_status = SubSystemStatus.ERROR
            elif fault.severity == ErrorType.WARNING:
                self._subsystem_status = SubSystemStatus.WARNING

        self._subsystem_status_prop.fset(None, self._subsystem_status.value)
        self._faults = self._faults_prop.fget(None)
        self._faults.append(str(fault))
        self._faults_prop.fset(None, self._faults)

    def clearFaults(self):
        self._subsystem_status = SubSystemStatus.OK
        self._faults = []
        if not self._diagnostics_initialized:
            return
        self._subsystem_status_prop.fset(None, self._subsystem_status.value)
        self._faults_prop.fset(None, self._faults)

    def getSubsystemStatus(self) -> SubSystemStatus:
        return self._subsystem_status

    def setSubsystemStatus(self, status: SubSystemStatus):
        self._subsystem_status = status
        if not self._diagnostics_initialized:
            return
        self._subsystem_status_prop.fset(None, self._subsystem_status.value)

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
